
import csv
import getpass
from pathlib import Path

import requests

BASE_URL = "http://localhost:58000/api/v1"

password = getpass.getpass("Contrasena del controlador: ")

respuesta = requests.post(
    f"{BASE_URL}/ticket",
    json={"username": "cisco", "password": password},
    timeout=20
)
respuesta.raise_for_status()

token = respuesta.json()["response"]["serviceTicket"]
headers = {"X-Auth-Token": token}

def consultar(endpoint):
    respuesta = requests.get(
        f"{BASE_URL}/{endpoint}",
        headers=headers,
        timeout=20
    )
    respuesta.raise_for_status()
    return respuesta.json()["response"]


dispositivos = consultar("network-device")
hosts = consultar("host")

inventario = []

for equipo in dispositivos:
    if equipo.get("collectionStatus") != "Managed":
        continue

    inventario.append({
        "Categoria": "Red",
        "Nombre": equipo.get("hostname", "N/D"),
        "IPv4": equipo.get("managementIpAddress", "N/D"),
        "Modelo": equipo.get("platformId", "N/D"),
        "MAC": equipo.get("macAddress", ""),
    })

vistos = set()

for host in hosts:
    clave = (
        host.get("hostName"),
        host.get("hostIp"),
        host.get("hostMac")
    )

    if clave in vistos:
        continue

    vistos.add(clave)

    inventario.append({
        "Categoria": "Host",
        "Nombre": host.get("hostName", "N/D"),
        "IPv4": host.get("hostIp", "N/D"),
        "Modelo": "",
        "MAC": host.get("hostMac", ""),
    })

carpeta = Path(__file__).resolve().parent.parent / "resultados"
carpeta.mkdir(exist_ok=True)

archivo = carpeta / "inventario_grupo14.csv"

columnas = ["Categoria", "Nombre", "IPv4", "Modelo", "MAC"]

with open(archivo, "w", newline="", encoding="utf-8-sig") as f:
    escritor = csv.DictWriter(f, fieldnames=columnas)
    escritor.writeheader()
    escritor.writerows(inventario)

print("\nInventario exportado correctamente.")
print(f"Dispositivos administrados: {sum(x['Categoria'] == 'Red' for x in inventario)}")
print(f"Hosts unicos: {len(vistos)}")
print(f"Total de registros: {len(inventario)}")
print(f"Archivo generado: {archivo}")
