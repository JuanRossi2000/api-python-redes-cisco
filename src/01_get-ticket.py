import json
import requests
import getpass
api_url = "http://localhost:58000/api/v1/ticket"

headers = {
    "content-type": "application/json"
}

body_json = {
    "username": "cisco",
    "password": getpass.getpass("Contraseña del controlador: ")
}

resp = requests.post(api_url, json.dumps(body_json), headers=headers)

print("Ticket request status: ", resp.status_code)
response_json = resp.json()
print (response_json)
serviceTicket = response_json["response"]["serviceTicket"]

print("The service ticket number is: ", serviceTicket) 