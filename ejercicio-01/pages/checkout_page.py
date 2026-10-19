"""Checkout de invitado. Cada paso espera el panel que OpenCart carga por AJAX."""

from __future__ import annotations

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as expected

from pages.base_page import BasePage


class CheckoutPage(BasePage):
    GUEST_OPTION = (By.CSS_SELECTOR, "input[name='account'][value='guest']")
    ACCOUNT_CONTINUE = (By.ID, "button-account")
    FIRST_NAME = (By.ID, "input-payment-firstname")
    LAST_NAME = (By.ID, "input-payment-lastname")
    EMAIL = (By.ID, "input-payment-email")
    TELEPHONE = (By.ID, "input-payment-telephone")
    ADDRESS = (By.ID, "input-payment-address-1")
    CITY = (By.ID, "input-payment-city")
    POSTCODE = (By.ID, "input-payment-postcode")
    COUNTRY = (By.ID, "input-payment-country")
    ZONE = (By.ID, "input-payment-zone")
    SAME_ADDRESS = (By.CSS_SELECTOR, "#collapse-payment-address input[name='shipping_address']")
    GUEST_CONTINUE = (By.ID, "button-guest")
    SHIPPING_CONTINUE = (By.ID, "button-shipping-method")
    AGREE = (By.CSS_SELECTOR, "#collapse-payment-method input[name='agree']")
    PAYMENT_CONTINUE = (By.ID, "button-payment-method")
    CONFIRM = (By.ID, "button-confirm")
    CONFIRM_PRODUCTS = (By.CSS_SELECTOR, "#collapse-checkout-confirm table a")
    BILLING_ERRORS = (
        By.CSS_SELECTOR,
        "#collapse-payment-address .text-danger, #collapse-payment-address .alert-danger",
    )
    PAYMENT_ERRORS = (
        By.CSS_SELECTOR,
        "#collapse-payment-method .text-danger, #collapse-payment-method .alert-danger",
    )

    def continue_as_guest(self) -> None:
        self.wait.until(expected.element_to_be_clickable(self.GUEST_OPTION))
        self.click(self.GUEST_OPTION)
        if not self.driver.find_element(*self.GUEST_OPTION).is_selected():
            raise AssertionError("No quedo seleccionada la opcion Guest Checkout.")
        self.click(self.ACCOUNT_CONTINUE)
        self.wait_panel_open("collapse-payment-address")

    def fill_billing(self, guest: dict) -> None:
        self.fill(self.FIRST_NAME, guest["first_name"])
        self.fill(self.LAST_NAME, guest["last_name"])
        self.fill(self.EMAIL, guest["email"])
        self.fill(self.TELEPHONE, guest["telephone"])
        self.fill(self.ADDRESS, guest["address_1"])
        self.fill(self.CITY, guest["city"])
        self.fill(self.POSTCODE, guest["postcode"])
        self.select_visible_text(self.COUNTRY, guest["country"])
        self.select_visible_text(self.ZONE, guest["zone"])
        if self.driver.find_elements(*self.SAME_ADDRESS):
            self._ensure_selected(self.SAME_ADDRESS)

    def continue_billing(self) -> str:
        self.click(self.GUEST_CONTINUE)

        def _advanced(_driver: WebDriver) -> str | bool:
            self.raise_if_validation_errors(self.BILLING_ERRORS)
            if self.panel_is_open("collapse-shipping-method"):
                return "shipping"
            if self.panel_is_open("collapse-payment-method"):
                return "payment"
            return False

        try:
            opened = self.wait.until(_advanced)
        except TimeoutException as exc:
            raise AssertionError("La facturacion no abrio ni envio ni pago.") from exc
        return str(opened)

    def accept_flat_shipping(self, method_value: str) -> str:
        if method_value != "flat.flat":
            raise ValueError("Esta demo se valida con el envio flat.flat.")
        method = (By.CSS_SELECTOR, f"input[name='shipping_method'][value='{method_value}']")
        self.wait.until(expected.presence_of_element_located(method))
        self._ensure_selected(method)
        description = " ".join(
            self.driver.find_element(By.ID, "collapse-shipping-method").text.split()
        )
        self.click(self.SHIPPING_CONTINUE)
        self.wait_panel_open("collapse-payment-method")
        return description

    def pay_cash_on_delivery(self, method_value: str) -> None:
        self._select_payment(method_value)
        self._ensure_selected(self.AGREE)
        self.click(self.PAYMENT_CONTINUE)
        self.wait_panel_open("collapse-checkout-confirm", self.PAYMENT_ERRORS)

    def submit_empty_billing(self) -> list[str]:
        self.click(self.GUEST_CONTINUE)
        self.wait.until(lambda driver: len(self._visible_errors(self.BILLING_ERRORS)) > 0)
        return self._visible_errors(self.BILLING_ERRORS)

    def continue_without_accepting_terms(self, method_value: str) -> str:
        self._select_payment(method_value)
        self._ensure_cleared(self.AGREE)
        self.click(self.PAYMENT_CONTINUE)
        alert = self.wait.until(expected.visibility_of_element_located(self.PAYMENT_ERRORS))
        return " ".join(alert.text.split())

    def _select_payment(self, method_value: str) -> None:
        if method_value not in {"cod", "bank_transfer"}:
            raise ValueError("Metodo de pago no contemplado por la suite.")
        method = (By.CSS_SELECTOR, f"input[name='payment_method'][value='{method_value}']")
        self.wait.until(expected.element_to_be_clickable(method))
        self._ensure_selected(method)

    def confirmation_product_names(self) -> list[str]:
        self.wait.until(expected.visibility_of_element_located(self.CONFIRM))
        names: list[str] = []
        for text in self.visible_texts(self.CONFIRM_PRODUCTS):
            if text and text not in names:
                names.append(text)
        return names

    def confirmation_text(self) -> str:
        panel = self.driver.find_element(By.ID, "collapse-checkout-confirm")
        return " ".join(panel.text.split())

    def confirm_order(self) -> None:
        self.click(self.CONFIRM)
        self.wait_until_url_contains("route=checkout/success")

    def _ensure_selected(self, locator: tuple[str, str]) -> None:
        element = self.wait.until(expected.presence_of_element_located(locator))
        if not element.is_selected():
            self.click(locator)
        element = self.driver.find_element(*locator)
        if not element.is_selected():
            raise AssertionError(f"No quedo seleccionado el control {locator}.")

    def _ensure_cleared(self, locator: tuple[str, str]) -> None:
        element = self.wait.until(expected.presence_of_element_located(locator))
        if element.is_selected():
            self.click(locator)
        element = self.driver.find_element(*locator)
        if element.is_selected():
            raise AssertionError(f"El control siguio marcado: {locator}.")

    def _visible_errors(self, locator: tuple[str, str]) -> list[str]:
        return [
            " ".join(element.text.split())
            for element in self.driver.find_elements(*locator)
            if element.text.strip()
        ]
