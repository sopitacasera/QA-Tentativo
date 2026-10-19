"""Acciones comunes. Solo esperas explicitas: la espera implicita queda en cero."""

from __future__ import annotations

from selenium.common.exceptions import (
    ElementClickInterceptedException,
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait


class BasePage:
    def __init__(self, driver: WebDriver, timeout_seconds: int) -> None:
        self.driver = driver
        self.timeout_seconds = timeout_seconds
        self.wait = WebDriverWait(driver, timeout_seconds)

    def open(self, url: str) -> None:
        self.driver.get(url)

    def click(self, locator: tuple[str, str]) -> None:
        element = self.wait.until(EC.element_to_be_clickable(locator))
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});",
            element,
        )
        try:
            element.click()
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].click();", element)

    def fill(self, locator: tuple[str, str], value: str) -> None:
        element = self.wait.until(EC.visibility_of_element_located(locator))
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});",
            element,
        )
        element.clear()
        element.send_keys(value)

    def select_visible_text(self, locator: tuple[str, str], visible_text: str) -> None:
        self.wait.until(lambda driver: self._option_is_present(driver, locator, visible_text))
        element = self.wait.until(EC.element_to_be_clickable(locator))
        Select(element).select_by_visible_text(visible_text)

    def text_of(self, locator: tuple[str, str]) -> str:
        element = self.wait.until(EC.visibility_of_element_located(locator))
        return " ".join(element.text.split())

    def wait_until_text(self, locator: tuple[str, str], text: str) -> None:
        self.wait.until(EC.text_to_be_present_in_element(locator, text))

    def wait_cart_item_count(self, count: int) -> str:
        locator = (By.ID, "cart-total")

        def _matches(driver: WebDriver) -> bool:
            text = " ".join(driver.find_element(*locator).text.split())
            return text.startswith(f"{count} item")

        self.wait.until(_matches)
        return self.text_of(locator)

    def wait_until_url_contains(self, fragment: str) -> None:
        self.wait.until(EC.url_contains(fragment))

    def visible_texts(self, locator: tuple[str, str]) -> list[str]:
        self.wait.until(EC.presence_of_element_located(locator))
        return [" ".join(element.text.split()) for element in self.driver.find_elements(*locator)]

    def raise_if_validation_errors(self, locator: tuple[str, str]) -> None:
        messages = [
            " ".join(element.text.split())
            for element in self.driver.find_elements(*locator)
            if element.text.strip()
        ]
        if messages:
            raise AssertionError(
                "La tienda rechazo el formulario: " + "; ".join(messages)
            )

    @staticmethod
    def _option_is_present(driver: WebDriver, locator: tuple[str, str], visible_text: str) -> bool:
        try:
            select = Select(driver.find_element(*locator))
        except StaleElementReferenceException:
            return False
        return any(option.text.strip() == visible_text for option in select.options)

    def panel_is_open(self, panel_id: str) -> bool:
        try:
            panel = self.driver.find_element(By.ID, panel_id)
            classes = f" {panel.get_attribute('class') or ''} "
            return " in " in classes
        except (StaleElementReferenceException, NoSuchElementException):
            return False

    def wait_panel_open(self, panel_id: str, error_locator: tuple[str, str] | None = None) -> None:
        def _opened(driver: WebDriver) -> bool:
            if error_locator is not None:
                self.raise_if_validation_errors(error_locator)
            return self.panel_is_open(panel_id)

        try:
            self.wait.until(_opened)
        except TimeoutException as exc:
            raise AssertionError(
                f"El paso del checkout no abrio el panel '{panel_id}'."
            ) from exc
