# Ejercicio 01 - Guest Checkout E2E - OpenCart Abstracta

Prueba funcional de punta a punta del enunciado QA-BP sobre
[http://opencart.abstracta.us/](http://opencart.abstracta.us/).

Agrega **MacBook** e **iPhone**, revisa el carrito, cierra la compra como
invitado y exige el texto `Your order has been placed!`.

Otras dos pruebas comprueban que la tienda frena una facturación vacía y un
pago sin aceptar los términos. Esas no crean orden.

La guía de ejecución que pide el enunciado está en `readme.txt`.
El criterio de un QA senior sobre esta demo, los defectos y la recomendación
de salida están en `conclusiones.txt`.

## Ejecutar

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\ejecutar.ps1
```

Chrome queda visible. Para no abrir ventana: `$env:HEADLESS = "true"`.

El informe queda en `reports/report.html`.

## Diseño

- Selenium WebDriver, pytest y Page Object Model.
- Esperas explícitas. La espera implícita está en cero.
- Datos de facturación fuera del código, en `data/guest_checkout.json`.
- Correo sintético nuevo en cada corrida, dominio `example.com`.
- La URL solo se acepta si el host es `opencart.abstracta.us`.
- Capturas del carrito, de la confirmación y de la orden colocada.

## Última ejecución registrada

18 de octubre de 2026. Resultado: **3 passed** en 76.72 s, Chrome headless.
El flujo del enunciado pasa. Para una tienda real, la recomendación es no
liberar hasta corregir el stock y el desglose del envío. Detalle en
`conclusiones.txt`.
