Ejercicio 02 - API PetStore
Documentación: https://petstore.swagger.io/
Base de la API: https://petstore.swagger.io/v2
Herramienta: Cypress.io

Este ejercicio vive en la carpeta ejercicio-02. El ejercicio 01, la compra
en OpenCart, está al mismo nivel. Los dos se ejecutan y se empaquetan
desde la carpeta raíz, con un solo script y un solo zip.

La suite crea una mascota, la consulta por id, le cambia el nombre y el
estado a sold, la busca entre las vendidas y comprueba que un id inexistente
responde 404.


1. Requisitos
   - Windows 10 o superior, macOS o Linux
   - Node.js 20 o superior (en esta máquina se ejecutó con 24.15)
   - Conexión a internet. La API es la demo pública de Swagger
   - No hace falta Java. Karate era la otra herramienta deseable, pero pide
     Java y en esta máquina no está instalado


2. Ejecución recomendada en Windows

   Abrir PowerShell en esta carpeta y correr:

   powershell -ExecutionPolicy Bypass -File .\scripts\ejecutar.ps1

   El script instala Cypress si falta, lanza las pruebas y genera
   reports\report.html. La primera vez Cypress descarga su navegador:
   puede tardar varios minutos. Las siguientes son cortas.

   Para correr los dos ejercicios juntos, usar el script de la carpeta raíz:

   powershell -ExecutionPolicy Bypass -File .\ejecutar.ps1


3. Ejecución manual

   npm install
   npx cypress run
   node .\scripts\informe.js


4. Resultado y evidencia

   reports\report.html
   reports\cypress-results.json
   reports\evidencia\01-alta.json
   reports\evidencia\02-consulta-por-id.json
   reports\evidencia\03-actualizacion.json
   reports\evidencia\04-busqueda-por-estado.json
   reports\evidencia\05-id-inexistente.json

   Lo esperado son 5 passed. La corrida registrada del 2026-10-18
   terminó así, en unos 2 segundos, con Cypress 15.21.1.


5. Qué valida la prueba

   - CP-01. POST /pet. Crea la mascota con un id aleatorio, nombre,
     foto y estado available. Espera HTTP 200 y el mismo id.
   - CP-02. GET /pet/{id}. La mascota recién creada se lee por id,
     con el mismo nombre y estado available.
   - CP-03. PUT /pet. Cambia el nombre y el estado a sold. Después
     vuelve a leer por id para comprobar que el cambio quedó guardado.
   - CP-04. GET /pet/findByStatus?status=sold. La mascota modificada
     aparece en esa lista, con el nombre nuevo y estado sold.
   - CP-05. GET /pet/404404404. Un id que no existe responde 404
     y el mensaje "Pet not found". No forma parte de los cuatro pasos
     del enunciado: cierra el negativo para no dar por buena cualquier
     consulta.

   El id cambia en cada corrida para no pisar la mascota de otra persona
   en la demo compartida. Al terminar, la suite borra esa mascota.
   La evidencia queda en los JSON.


6. Empaquetar los dos ejercicios

   Desde la carpeta raíz del repositorio:

   powershell -ExecutionPolicy Bypass -File .\empaquetar.ps1

   Crea un solo zip, QA-BP-ejercicios-qa.zip.


7. Repositorio público

   La URL que se pega en los comentarios de los dos enunciados es la del
   repositorio completo, no la de esta carpeta sola:

   https://github.com/sopitacasera/QA-Tentativo
