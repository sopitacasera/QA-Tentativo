"""Carrito de compras."""

from __future__ import annotations

import logging

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expected
from selenium.webdriver.support.ui import WebDriverWait

from pages.base_page import BasePage


LOGGER = logging.getLogger(__name__)


class CartPage(BasePage):
    HEADER_CART = (By.CSS_SELECTOR, "a[title='Shopping Cart']")
    PRODUCT_LINKS = (By.CSS_SELECTOR, "#content .table-responsive tbody td.text-left a")
    CHECKOUT = (By.CSS_SELECTOR, "#content a[href*='route=checkout/checkout']")
    PRODUCT_ROWS = (By.CSS_SELECTOR, "#content .table-responsive tbody tr")

    def open_from_header(self) -> None:
        link = self.wait.until(expected.visibility_of_element_located(self.HEADER_CART))
        href = link.get_attribute("href") or ""
        self.click(self.HEADER_CART)
        if not self._reached_cart(5) and href:
            LOGGER.warning("El clic en Shopping Cart no navego. Se sigue el mismo enlace.")
            self.open(href)
        self.wait_until_url_contains("checkout/cart")
        try:
            self.wait.until(lambda driver: len(driver.find_elements(*self.PRODUCT_ROWS)) > 0)
        except TimeoutException as exc:
            raise AssertionError("El carrito abrio, pero no mostro productos.") from exc

    def _reached_cart(self, seconds: int) -> bool:
        try:
            WebDriverWait(self.driver, seconds).until(expected.url_contains("checkout/cart"))
            return True
        except TimeoutException:
            return False

    def product_names(self) -> list[str]:
        names: list[str] = []
        for text in self.visible_texts(self.PRODUCT_LINKS):
            if text and text not in names:
                names.append(text)
        return names

    def quantity_of(self, product_name: str) -> str:
        for row in self.driver.find_elements(*self.PRODUCT_ROWS):
            links = row.find_elements(By.CSS_SELECTOR, "td.text-left a")
            if any(link.text.strip() == product_name for link in links):
                quantity = row.find_element(By.CSS_SELECTOR, "input[name^='quantity']")
                return (quantity.get_attribute("value") or "").strip()
        raise AssertionError(f"{product_name} no aparece en el carrito.")

    def go_to_checkout(self) -> None:
        self.click(self.CHECKOUT)
        self.wait_until_url_contains("route=checkout/checkout")
