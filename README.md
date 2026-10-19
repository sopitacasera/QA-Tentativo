# Ejercicios QA-BP

Un solo repositorio y un solo paquete para los dos enunciados.

| Carpeta | Enunciado | Herramienta |
| --- | --- | --- |
| `ejercicio-01` | Compra como invitado en OpenCart | Selenium |
| `ejercicio-02` | API PetStore: alta, consulta, actualización y búsqueda | Cypress |

La URL que se pega en los comentarios de los dos ejercicios es:

https://github.com/sopitacasera/QA-Tentativo

No hace falta una URL por carpeta.

## Ejecutar los dos

Desde esta carpeta:

```powershell
powershell -ExecutionPolicy Bypass -File .\ejecutar.ps1
```

Eso corre primero la compra y después la API. La compra abre Chrome y
crea una orden real en la demo. La API crea una mascota y la borra al final.

Cada ejercicio también se puede correr solo:

```powershell
powershell -ExecutionPolicy Bypass -File .\ejercicio-01\scripts\ejecutar.ps1
powershell -ExecutionPolicy Bypass -File .\ejercicio-02\scripts\ejecutar.ps1
```

## Un solo zip

```powershell
powershell -ExecutionPolicy Bypass -File .\empaquetar.ps1
```

Crea `QA-BP-ejercicios-qa.zip` junto a esta carpeta. Adentro van las dos
carpetas, con su `readme.txt`, su `conclusiones.txt` y sus reportes.
No incluye `.venv` ni `node_modules`.

## Dónde está cada resultado

- Ejercicio 01: `ejercicio-01/reports/report.html` y `ejercicio-01/conclusiones.txt`
- Ejercicio 02: `ejercicio-02/reports/report.html` y `ejercicio-02/conclusiones.txt`

El paso a paso de cada uno está en el `readme.txt` de su carpeta.
