"""Home y resultados de busqueda."""

from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expected

from pages.base_page import BasePage


class HomePage(BasePage):
    SEARCH_INPUT = (By.CSS_SELECTOR, "#search input[name='search']")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "#search button")
    NO_RESULTS = (
        By.XPATH,
        "//p[contains(., 'There is no product that matches the search criteria')]",
    )

    def search(self, term: str) -> None:
        self.fill(self.SEARCH_INPUT, term)
        self.click(self.SEARCH_BUTTON)
        self.wait_until_url_contains("route=product/search")
        if self.driver.find_elements(*self.NO_RESULTS):
            raise AssertionError(f"La busqueda no devolvio resultados para '{term}'.")

    def open_product(self, name: str) -> None:
        if "'" in name or '"' in name:
            raise ValueError("El nombre de producto no puede incluir comillas.")
        locator = (
            By.XPATH,
            (
                "//div[contains(@class,'product-layout')]"
                f"//h4/a[normalize-space()='{name}']"
            ),
        )
        self.click(locator)
        self.wait.until(expected.visibility_of_element_located((By.ID, "button-cart")))
