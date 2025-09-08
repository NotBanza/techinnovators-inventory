import requests
import json

BASE_URL = "https://oracleapex.com/ords/inventory_systems/inventory2" # Your correct base URL

def get_employee_checkouts(employee_id):
    url = f"{BASE_URL}/checkout/{employee_id}"
    requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
    try:
        response = requests.get(url, timeout=20, verify=False)
        response.raise_for_status()
        return response.json().get('items', [])
    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}") # For debugging
        return None # Return None on error

def return_item(booking_id):
    url = f"{BASE_URL}/returns"
    headers = {'Content-Type': 'application/json'}
    data = {"booking_id": int(booking_id)}
    requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
    try:
        response = requests.post(url, json=data, headers=headers, timeout=20, verify=False)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}") # For debugging
        return {"status": "error", "message": str(e)}