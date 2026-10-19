"""Ficha de producto."""

from __future__ import annotations

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class ProductPage(BasePage):
    TITLE = (By.CSS_SELECTOR, "#content h1")
    ADD_TO_CART = (By.ID, "button-cart")
    SUCCESS_ALERT = (By.CSS_SELECTOR, ".alert-success")

    def name(self) -> str:
        return self.text_of(self.TITLE)

    def add_to_cart(self) -> str:
        self.click(self.ADD_TO_CART)
        return self.text_of(self.SUCCESS_ALERT)
