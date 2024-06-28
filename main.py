import os
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from PyPDF2 import PdfReader

# Load credentials from the 'client_secrets.json' file
creds = Credentials.from_service_account_file('client_secrets.json')

# Build the service
service = build('drive', 'v3', credentials=creds)

# Specify the IDs of the directories
dir_ids = ['1fvSJtTIhUhwOmZhOne6zZS0zErXRYO99', '1hEPABYsy7PYRcWXz5NVc7Xwp4Kg0DPao']

folder_dict = {
    'purchase_orders': '1fvSJtTIhUhwOmZhOne6zZS0zErXRYO99',
    'invoices': '1hEPABYsy7PYRcWXz5NVc7Xwp4Kg0DPao'
}

def get_files_from_folder(folder_name):
    folder_id = folder_dict[folder_name]
    results = service.files().list(q=f"'{folder_id}' in parents").execute()
    items = results.get('files', [])
    return items

def read_files_from_folder(items):
    for item in items:
        request = service.files().get_media(fileId=item['id'])
        fh = open(os.path.join('docs', item['name']), 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
        fh.close()
        fh = open(os.path.join('docs', item['name']), 'rb')
        fh.seek(0)
        pdf = PdfReader(fh) 
        content = """"""
        for i in range(len(pdf.pages)):
            content += pdf.pages[i].extract_text()
        print(content)
        fh.close()
        os.remove(os.path.join('docs', item['name']))

items = get_files_from_folder('purchase_orders')
read_files_from_folder(items)

