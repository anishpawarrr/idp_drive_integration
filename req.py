import requests

url = "http://localhost:7071/api/scandrive/scan"

data = {
    "purchase_orders": "1fvSJtTIhUhwOmZhOne6zZS0zErXRYO99",
    "invoices": "1hEPABYsy7PYRcWXz5NVc7Xwp4Kg0DPao"
}

response = requests.post(url, json=data)

print(response)
print(response.json())