import json
import requests
import getpass
api_url = "http://localhost:58000/api/v1/host"

headers={"X-Auth-Token": getpass.getpass("Ingrese el token: ")}

resp = requests.get(api_url, headers=headers, verify=False)

print("Request status: ", resp.status_code)

response_json = resp.json()

hosts = response_json["response"]

hosts_unicos = []
vistos = set()

for host in hosts:
    clave = (
        host.get("hostName"),
        host.get("hostIp"),
        host.get("hostMac")
    )

    if clave not in vistos:
        vistos.add(clave)
        hosts_unicos.append(host)

print(f"\nTotal de hosts unicos: {len(hosts_unicos)}\n")

print(f"{'Host':<25} {'IPv4':<18} {'MAC':<20} {'Interfaz'}")
print("-" * 85)

for host in sorted(hosts_unicos, key=lambda h: h.get("hostName") or ""):
    print(
        f"{host.get('hostName') or 'N/D':<25} "
        f"{host.get('hostIp') or 'N/D':<18} "
        f"{host.get('hostMac') or 'N/D':<20} "
        f"{host.get('connectedInterfaceName') or 'N/D'}"
    )
