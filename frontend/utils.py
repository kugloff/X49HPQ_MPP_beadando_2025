import requests

BASE_URL = "http://127.0.0.1:8000"

def get_items():
    try:
        response = requests.get(f"{BASE_URL}/items/")
        return response.json() if response.status_code == 200 else []
    except:
        return []

def create_item(name: str, description: str):
    try:
        response = requests.post(f"{BASE_URL}/items/", json={"name": name, "description": description})
        return response.status_code
    except:
        return None