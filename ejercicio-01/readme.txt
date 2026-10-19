Ejercicio 01 - Guest Checkout en OpenCart
Tienda: http://opencart.abstracta.us/
Framework: Selenium WebDriver + Python + pytest

Este ejercicio vive en la carpeta ejercicio-01. El ejercicio 02, la API
de PetStore, está al mismo nivel. Los dos se ejecutan y se empaquetan
desde la carpeta raíz, con un solo script y un solo zip.

La suite agrega MacBook e iPhone, abre el carrito, completa el checkout
como invitado y comprueba el mensaje "Your order has been placed!".
Además frena dos compras que no deben existir: facturación vacía y pago
sin aceptar los términos. Esas dos no crean orden.
El criterio, los defectos y la recomendación están en conclusiones.txt.


1. Requisitos
   - Windows 10 o superior, macOS o Linux
   - Python 3.11 o superior (en esta máquina se ejecutó con 3.14)
   - Google Chrome instalado. Microsoft Edge también sirve con BROWSER=edge
   - Conexión a internet. La prueba compra en la demo pública del enunciado
   - No hace falta descargar ChromeDriver: Selenium Manager lo resuelve


2. Ejecución recomendada en Windows

   Abrir PowerShell en la carpeta del proyecto y correr:

   powershell -ExecutionPolicy Bypass -File .\scripts\ejecutar.ps1

   El script crea .venv, instala requirements.txt y lanza pytest.
   Al terminar, el código de salida es el de pytest: 0 es aprobado.


3. Ejecución manual

   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   python -m pytest

   En macOS o Linux el intérprete del entorno es .venv/bin/python.


4. Ver el navegador o esconderlo

   Por defecto Chrome se abre en pantalla, para que se pueda seguir el flujo.
   Para ejecutarlo sin ventana:

   $env:HEADLESS = "true"
   python -m pytest

   La evidencia que viaja en reports\ se generó con HEADLESS=true.
   Otras variables, todas opcionales:

   BROWSER=chrome|edge
   TIMEOUT_SECONDS=30
   BASE_URL=http://opencart.abstracta.us/

   BASE_URL solo se acepta si el host es opencart.abstracta.us.
   La suite confirma una compra real y no debe apuntar a otra tienda.


5. Resultado y evidencia

   reports\report.html     informe HTML autocontenido, con las capturas
   reports\junit.xml       resultado en JUnit
   reports\execution.log   traza de cada paso
   reports\evidence\01-carrito.png
   reports\evidence\02-confirmacion-de-orden.png
   reports\evidence\03-orden-colocada.png
   reports\evidence\04-facturacion-vacia.png
   reports\evidence\05-sin-aceptar-terminos.png

   Abrir report.html en el navegador. Lo esperado son 3 passed.
   La corrida registrada terminó así el 2026-10-18, en 76.72 segundos.
   El informe abre con el resultado del ejercicio y el nombre de cada caso.
   Hay que abrir la fila para ver las capturas.


6. Qué valida la prueba

   - Busca y abre MacBook, lo agrega y espera el aviso Success.
   - Busca y abre iPhone, lo agrega y espera 2 item(s) en el minicart.
   - Entra a Shopping Cart y comprueba los dos productos con cantidad 1.
   - Elige Guest Checkout.
   - Completa la facturación con datos sintéticos. La dirección de entrega
     queda igual a la de facturación.
   - Acepta Flat Shipping Rate.
   - Paga con Cash On Delivery y marca Terms & Conditions.
   - Comprueba los dos productos en el paso Confirm Order.
   - Confirma y exige el título exacto "Your order has been placed!".
   - Con la facturación vacía, exige los mensajes de campos obligatorios
     y comprueba que no existe una orden.
   - Sin marcar Terms & Conditions, exige el aviso de la tienda y comprueba
     que no se abre la confirmación ni se coloca la orden.

   Los datos viven en data\guest_checkout.json. El correo se genera en cada
   corrida con el dominio example.com. No hay claves ni datos personales.


7. Por qué esos dos productos

   MacBook e iPhone no piden opciones obligatorias.
   Apple Cinema 30" y Canon EOS 5D sí las piden: agregarlos desde el listado
   no arma este flujo. La suite rechaza esos dos nombres a propósito.


8. Empaquetar los dos ejercicios

   Desde la carpeta raíz del repositorio, no desde esta:

   powershell -ExecutionPolicy Bypass -File .\empaquetar.ps1

   Crea un solo zip, QA-BP-ejercicios-qa.zip, con el ejercicio 01 y el 02.
   No incluye .venv ni node_modules.


9. Repositorio público

   La URL que se pega en los dos enunciados es la de la carpeta raíz:

   https://github.com/sopitacasera/QA-Tentativo
