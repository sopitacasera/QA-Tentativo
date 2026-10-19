"""Compra de punta a punta como invitado en la demo OpenCart del enunciado."""

from __future__ import annotations

import logging

import pytest

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.home_page import HomePage
from pages.product_page import ProductPage
from pages.success_page import SuccessPage


LOGGER = logging.getLogger(__name__)


def _agregar_productos(driver, settings, names: list[str]) -> None:
    home = HomePage(driver, settings.timeout_seconds)
    product_page = ProductPage(driver, settings.timeout_seconds)
    home.open(settings.base_url)
    for index, name in enumerate(names, start=1):
        LOGGER.info("Agregar producto %s de %s: %s", index, len(names), name)
        home.search(name)
        home.open_product(name)
        assert product_page.name() == name, f"La ficha abierta no es {name}."
        message = product_page.add_to_cart()
        assert "Success" in message and name in message, (
            f"La tienda no confirmo que {name} entro al carrito. Mensaje: {message}"
        )
        summary = product_page.wait_cart_item_count(index)
        LOGGER.info("Resumen del minicart: %s", summary)


def _iniciar_guest_checkout(driver, settings):
    cart = CartPage(driver, settings.timeout_seconds)
    cart.open_from_header()
    cart.go_to_checkout()
    checkout = CheckoutPage(driver, settings.timeout_seconds)
    checkout.continue_as_guest()
    return cart, checkout


@pytest.mark.e2e
def test_guest_checkout_confirma_la_compra_de_dos_productos(driver, settings, guest, evidence):
    """Agrega dos productos, revisa el carrito y cierra la compra como invitado.

    El oraculo del enunciado es el titulo "Your order has been placed!".
    La prueba tambien exige los dos productos en el carrito y en la confirmacion,
    con cantidad 1, para no dar por buena una orden vacia o incompleta.
    """
    products = guest["products"]
    LOGGER.info("Abrir la tienda %s", settings.base_url)
    _agregar_productos(driver, settings, products)

    cart = CartPage(driver, settings.timeout_seconds)
    LOGGER.info("Abrir el carrito desde el encabezado")
    cart.open_from_header()
    evidence.capture(driver, "01-carrito")

    assert set(cart.product_names()) == set(products), (
        f"El carrito no contiene exactamente los dos productos. Vio: {cart.product_names()}"
    )
    for name in products:
        quantity = cart.quantity_of(name)
        assert quantity == "1", f"La cantidad de {name} debia ser 1 y fue {quantity}."

    LOGGER.info("Iniciar checkout como invitado. Correo sintetico: %s", guest["email"])
    cart.go_to_checkout()
    checkout = CheckoutPage(driver, settings.timeout_seconds)
    checkout.continue_as_guest()
    checkout.fill_billing(guest)
    checkout.continue_billing()

    shipping = checkout.accept_flat_shipping(guest["shipping_method"])
    LOGGER.info("Envio ofrecido: %s", shipping)

    checkout.pay_cash_on_delivery(guest["payment_method"])
    confirmed = checkout.confirmation_product_names()
    LOGGER.info("Resumen antes de confirmar: %s", checkout.confirmation_text())
    evidence.capture(driver, "02-confirmacion-de-orden")
    assert set(confirmed) == set(products), (
        f"La confirmacion no lista los dos productos. Vio: {confirmed}"
    )

    checkout.confirm_order()
    success = SuccessPage(driver, settings.timeout_seconds)
    heading = success.heading()
    body = success.message()
    evidence.capture(driver, "03-orden-colocada")
    LOGGER.info("Resultado final: %s", heading)

    assert heading == guest["expected_confirmation"], (
        f"La confirmacion final fue '{heading}'."
    )
    assert "Your order has been successfully processed!" in body
    assert "checkout/success" in driver.current_url


@pytest.mark.e2e
def test_facturacion_vacia_no_deja_avanzar_ni_coloca_la_orden(driver, settings, guest, evidence):
    """Negativo de frontera: sin datos obligatorios no hay envio ni orden.

    Usa un solo producto. El riesgo de este caso es el formulario, no la
    cantidad de items que ya cubre el flujo del enunciado.
    """
    _agregar_productos(driver, settings, [guest["products"][0]])
    _cart, checkout = _iniciar_guest_checkout(driver, settings)
    errors = checkout.submit_empty_billing()
    evidence.capture(driver, "04-facturacion-vacia")
    joined = " ".join(errors)
    LOGGER.info("Errores de facturacion vacia: %s", joined)

    assert "First Name must be between 1 and 32 characters!" in joined
    assert "E-Mail address does not appear to be valid!" in joined
    assert "checkout/success" not in driver.current_url
    assert not checkout.panel_is_open("collapse-shipping-method")


@pytest.mark.e2e
def test_sin_aceptar_terminos_no_coloca_la_orden(driver, settings, guest, evidence):
    """Negativo de regla de negocio: sin Terms & Conditions no se confirma.

    Recorre invitado, envio y pago, y se detiene antes de Confirm Order.
    """
    _agregar_productos(driver, settings, [guest["products"][1]])
    _cart, checkout = _iniciar_guest_checkout(driver, settings)
    checkout.fill_billing(guest)
    if checkout.continue_billing() == "shipping":
        checkout.accept_flat_shipping(guest["shipping_method"])
    message = checkout.continue_without_accepting_terms(guest["payment_method"])
    evidence.capture(driver, "05-sin-aceptar-terminos")
    LOGGER.info("Respuesta al omitir terminos: %s", message)

    assert "You must agree to the" in message
    assert "Terms" in message
    assert "checkout/success" not in driver.current_url
    assert not checkout.panel_is_open("collapse-checkout-confirm")
