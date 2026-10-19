"""Construccion del navegador. Selenium Manager resuelve el driver; no se versiona el binario."""

from __future__ import annotations

import logging

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions

from config.settings import Settings


LOGGER = logging.getLogger(__name__)


def build_driver(settings: Settings):
    if settings.browser == "edge":
        options = EdgeOptions()
        driver = webdriver.Edge(options=_apply_common_options(options, settings))
    else:
        options = ChromeOptions()
        driver = webdriver.Chrome(options=_apply_common_options(options, settings))

    driver.set_page_load_timeout(settings.timeout_seconds * 2)
    driver.implicitly_wait(0)
    LOGGER.info(
        "Navegador %s listo. headless=%s timeout=%ss",
        settings.browser,
        settings.headless,
        settings.timeout_seconds,
    )
    return driver


def _apply_common_options(options, settings: Settings):
    if settings.headless:
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
    else:
        options.add_argument("--start-maximized")

    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-extensions")
    options.add_argument("--no-first-run")
    options.add_argument("--no-default-browser-check")
    options.page_load_strategy = "normal"
    return options
