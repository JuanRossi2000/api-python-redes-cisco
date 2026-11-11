# TP4 Integrador — Redes de Computadoras (3643)

## Grupo 14 — Scripts Python y API REST de Cisco Packet Tracer

Este repositorio parte de los scripts suministrados por la cátedra y agrega un script desarrollado por el Grupo 14. El objetivo es consultar la API REST Northbound del **Cisco Network Controller** de Packet Tracer, presentar inventarios de dispositivos y hosts, y exportar la información a un archivo CSV.

El controlador se utiliza en una topología dual stack (IPv4/IPv6) con cuatro routers internos Cisco ISR 4331, dos switches multicapa Cisco 3650 y cinco switches de acceso Cisco 2960. El router ISP simulado pertenece a la red externa y no se incluye entre los dispositivos administrados.

## Archivos del proyecto

| Archivo | Descripción |
| `src/01_get-ticket.py` | Solicita un ticket de autenticación a la API. La contraseña se ingresa desde la terminal. |
| `src/02_get-network-device.py` | Consulta `/api/v1/network-device` y muestra los equipos en estado `Managed`, con nombre, modelo e IP de gestión. Solicita el ticket por terminal. |
| `src/03_get-host.py` | Consulta `/api/v1/host`, elimina registros duplicados para la presentación y lista nombre, IPv4, MAC e interfaz de conexión. Solicita el ticket por terminal. |
| `src/04_tabulate.py` | Se autentica y presenta tablas de equipos y hosts utilizando la biblioteca `tabulate`. |
| **`src/05_exportar_inventario.py`** | **Script propio del Grupo 14.** Consulta dispositivos y hosts, filtra los equipos `Managed`, elimina hosts duplicados y genera un CSV consolidado. |
| `requirements.txt` | Dependencias de Python utilizadas por los scripts. |
| `.gitignore` | Exclusiones de archivos locales, credenciales y entornos virtuales. |

1. `01_get-ticket.py` solicita la contraseña del controlador y obtiene un serviceTicket temporal.
2. `02_get-network-device.py` y `03_get-host.py` solicitan ese ticket por terminal. Si expiró, generar uno nuevo con el primer script.
3. `04_tabulate.py` y `05_exportar_inventario.py` realizan su propia autenticación solicitando la contraseña por terminal.
4. Los scripts están preparados para ejecutarse con el usuario de ejemplo `cisco`. Si el usuario del controlador es otro, debe adaptarse el campo `username` en los scripts correspondientes.

## Script propio: exportación de inventario a CSV

El archivo `src/05_exportar_inventario.py`

Su procedimiento es:

1. Solicitar la contraseña y obtener un ticket de autenticación mediante `POST /api/v1/ticket`.
2. Consultar los equipos mediante `GET /api/v1/network-device`.
3. Consultar los hosts mediante `GET /api/v1/host`.
4. Conservar únicamente los dispositivos de red con estado `Managed`; de este modo, el ISP externo no se incorpora al inventario administrado.
5. Eliminar los registros duplicados de hosts comparando nombre, IPv4 y MAC.
6. Crear la carpeta `resultados`, si no existe, y generar `resultados/inventario_grupo14.csv`.

**Columnas del CSV:** `Categoria`, `Nombre`, `IPv4`, `Modelo` y `MAC`.