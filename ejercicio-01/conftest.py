"""Fixtures de la suite. El navegador se crea y se cierra en cada prueba."""

from __future__ import annotations

import base64
import json
import logging
from html import escape
from pathlib import Path
from uuid import uuid4

import pytest
from pytest_html import extras as html_extras

from config.settings import Settings
from utils.driver_factory import build_driver


ROOT = Path(__file__).resolve().parent
DATA_FILE = ROOT / "data" / "guest_checkout.json"
EVIDENCE_DIR = ROOT / "reports" / "evidence"
PRODUCTS_WITH_REQUIRED_OPTIONS = {"Canon EOS 5D", 'Apple Cinema 30"'}

EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)

LOGGER = logging.getLogger(__name__)

CASE_NAMES = {
    "test_guest_checkout_confirma_la_compra_de_dos_productos": (
        "CP-01 Compra de dos productos como invitado"
    ),
    "test_facturacion_vacia_no_deja_avanzar_ni_coloca_la_orden": (
        "CP-02 Facturación vacía no coloca la orden"
    ),
    "test_sin_aceptar_terminos_no_coloca_la_orden": (
        "CP-03 Sin aceptar términos no coloca la orden"
    ),
}


class Evidence:
    def __init__(self, folder: Path) -> None:
        self.folder = folder
        self.paths: list[Path] = []

    def capture(self, driver, name: str) -> Path:
        safe = "".join(char if char.isalnum() or char in "-_" else "-" for char in name)
        path = self.folder / f"{safe}.png"
        driver.save_screenshot(str(path))
        self.paths.append(path)
        LOGGER.info("Evidencia guardada: %s", path.name)
        return path


@pytest.fixture
def settings() -> Settings:
    return Settings.load()


@pytest.fixture
def driver(settings: Settings):
    browser = build_driver(settings)
    yield browser
    browser.quit()


@pytest.fixture
def guest() -> dict:
    payload = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    products = payload.get("products", [])
    if len(products) != 2:
        raise AssertionError("guest_checkout.json debe declarar exactamente dos productos.")
    blocked = sorted(set(products) & PRODUCTS_WITH_REQUIRED_OPTIONS)
    if blocked:
        raise AssertionError(
            "Estos productos exigen opciones obligatorias y no sirven para este flujo: "
            + ", ".join(blocked)
        )
    payload["email"] = f"qa.guest.{uuid4().hex[:12]}@example.com"
    return payload


@pytest.fixture
def evidence() -> Evidence:
    return Evidence(EVIDENCE_DIR)


def pytest_metadata(metadata, config):
    settings = Settings.load()
    mode = "sin ventana" if settings.headless else "visible"
    useful = {
        "Ejercicio": "QA-BP - Guest Checkout E2E",
        "Tienda": settings.base_url,
        "Navegador": f"{settings.browser} ({mode})",
        "Python": metadata.get("Python", ""),
        "Plataforma": metadata.get("Platform", ""),
        "Pytest": metadata.get("Packages", {}).get("pytest", ""),
    }
    metadata.clear()
    metadata.update(useful)


def pytest_html_report_title(report):
    report.title = "OpenCart - Guest Checkout E2E"


def pytest_html_results_summary(prefix, summary, postfix, session):
    prefix.append(
        """
        <div class="verdict">
          <h2>Resultado del ejercicio</h2>
          <p><strong>Listo para entregar.</strong>
          CP-01 recorre el enunciado hasta el texto
          "Your order has been placed!".</p>
          <p>CP-02 y CP-03 comprueban que la tienda no coloca la orden
          si la facturación va vacía o si no se aceptan los términos.</p>
          <p>Los defectos de stock y del desglose de envío están en
          conclusiones.txt. No fallan esta suite: el enunciado pide
          completar la compra.</p>
          <p>Abre cada fila para ver las capturas.</p>
        </div>
        """
    )


def pytest_html_results_table_header(cells):
    cells.insert(1, "<th>Caso</th>")


def pytest_html_results_table_row(report, cells):
    test_name = report.nodeid.split("::")[-1]
    label = CASE_NAMES.get(test_name, test_name)
    cells.insert(1, f'<td class="col-caso">{escape(label)}</td>')


def _embedded_png(path: Path):
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return html_extras.png(encoded, name=path.stem)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when != "call":
        return

    attached = []
    evidence = item.funcargs.get("evidence")
    if evidence is not None:
        for path in evidence.paths:
            if path.exists():
                attached.append(_embedded_png(path))

    if report.failed:
        browser = item.funcargs.get("driver")
        if browser is not None:
            failure = EVIDENCE_DIR / "99-fallo.png"
            try:
                browser.save_screenshot(str(failure))
                attached.append(_embedded_png(failure))
            except Exception:
                LOGGER.exception("No se pudo capturar la pantalla del fallo.")

    if attached:
        report.extras = [*getattr(report, "extras", []), *attached]
