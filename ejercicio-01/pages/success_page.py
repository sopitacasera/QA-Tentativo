"""Pagina de confirmacion de la orden."""

from __future__ import annotations

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class SuccessPage(BasePage):
    HEADING = (By.CSS_SELECTOR, "#content h1")
    CONTENT = (By.CSS_SELECTOR, "#content")

    def heading(self) -> str:
        self.wait_until_url_contains("route=checkout/success")
        return self.text_of(self.HEADING)

    def message(self) -> str:
        return self.text_of(self.CONTENT)
