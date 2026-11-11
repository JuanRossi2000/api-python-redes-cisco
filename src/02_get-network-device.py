import json
import requests
import getpass
api_url = "http://localhost:58000/api/v1/network-device"

headers={"X-Auth-Token": getpass.getpass("Ingrese el token: ")}

resp = requests.get(api_url, headers=headers)

print("Request status: ", resp.status_code)

response_json = resp.json()

networkDevices = response_json["response"]

administrados = [
    equipo for equipo in networkDevices
    if equipo.get("collectionStatus") == "Managed"
    and equipo.get("hostname")
]

print(f"\nTotal de equipos administrados: {len(administrados)}\n")

print(f"{'Equipo':<18} {'Modelo':<12} {'IP de gestion'}")
print("-" * 50)

for equipo in administrados:
    print(
        f"{equipo['hostname']:<18} "
        f"{equipo.get('platformId', 'N/D'):<12} "
        f"{equipo.get('managementIpAddress', 'N/D')}"
    )


