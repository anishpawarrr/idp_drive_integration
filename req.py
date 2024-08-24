import requests

url = "http://localhost:7071/api/scandrive/scan?"
url = "https://idpdriveintegration.azurewebsites.net/api/scandrive/scan?"
data = {
    'stepData' : {
        "purchase_orders": "1fvSJtTIhUhwOmZhOne6zZS0zErXRYO99",
        "invoices": "1hEPABYsy7PYRcWXz5NVc7Xwp4Kg0DPao",
        'scanned_POs':'14z_LSXbYjZNluTJ_n_FZwaaDJN51W3gc',
        'scanned_invoices':'13N5GXgyXKzX5gW2wr1uaQaio0_0WVJje'
    },
    'flow' : {},
    'index' : 0,
    'errors' : []
}

response = requests.post(url, json=data)

print(response)
print(response.json())