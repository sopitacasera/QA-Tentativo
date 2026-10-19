"""Configuracion de ejecucion. Los valores salen del entorno, con defaults seguros."""

from __future__ import annotations

import os
from dataclasses import dataclass
from urllib.parse import urlparse


DEFAULT_BASE_URL = "http://opencart.abstracta.us/"
DEFAULT_ALLOWED_HOST = "opencart.abstracta.us"


@dataclass(frozen=True)
class Settings:
    base_url: str
    browser: str
    headless: bool
    timeout_seconds: int

    @property
    def cart_url(self) -> str:
        return f"{self.base_url}index.php?route=checkout/cart"

    @property
    def checkout_url(self) -> str:
        return f"{self.base_url}index.php?route=checkout/checkout"

    @staticmethod
    def load() -> "Settings":
        base_url = os.getenv("BASE_URL", DEFAULT_BASE_URL).strip()
        if not base_url.endswith("/"):
            base_url = f"{base_url}/"

        parsed = urlparse(base_url)
        if parsed.scheme not in {"http", "https"} or not parsed.hostname:
            raise ValueError("BASE_URL debe ser una URL http o https absoluta.")

        allowed_host = os.getenv("ALLOWED_HOST", DEFAULT_ALLOWED_HOST).strip().lower()
        if parsed.hostname.lower() != allowed_host:
            raise ValueError(
                "BASE_URL apunta a un host distinto del permitido. "
                "Esta suite confirma compras reales en la demo del enunciado. "
                f"Host recibido: {parsed.hostname}. Host permitido: {allowed_host}."
            )

        browser = os.getenv("BROWSER", "chrome").strip().lower()
        if browser not in {"chrome", "edge"}:
            raise ValueError("BROWSER debe ser chrome o edge.")

        headless = os.getenv("HEADLESS", "false").strip().lower() in {"1", "true", "yes"}

        raw_timeout = os.getenv("TIMEOUT_SECONDS", "30").strip()
        try:
            timeout_seconds = int(raw_timeout)
        except ValueError as exc:
            raise ValueError("TIMEOUT_SECONDS debe ser un entero.") from exc
        if timeout_seconds < 5 or timeout_seconds > 120:
            raise ValueError("TIMEOUT_SECONDS debe estar entre 5 y 120.")

        return Settings(
            base_url=base_url,
            browser=browser,
            headless=headless,
            timeout_seconds=timeout_seconds,
        )
