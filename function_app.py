import azure.functions as func
import logging
import os
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from PyPDF2 import PdfReader
from json import loads, dumps
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import io
import os


app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="scandrive")
def scandrive(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )

@app.route(route="scandrive/scan", methods=['POST'])
def scan_drive(req: func.HttpRequest) -> func.HttpResponse:
    request = req.get_json()
    creds = Credentials.from_service_account_file('client_secrets.json')

    service = build('drive', 'v3', credentials=creds)
    logging.warning("service done")
    folder_dict = {
        'purchase_orders': request['purchase_orders'],
        'invoices': request['invoices']
    }

    scanned_folder_dict = {
        'scanned_POs':'14z_LSXbYjZNluTJ_n_FZwaaDJN51W3gc',
        'scanned_invoices':'13N5GXgyXKzX5gW2wr1uaQaio0_0WVJje'
    }

    logging.warning("folder dict done")
    results = service.files().list(q=f"'{folder_dict['purchase_orders']}' in parents").execute()
    logging.warning("res 1")

    items_purchase_orders = results.get('files', [])
    # items_purchase_orders = filter_pdf_items(items_purchase_orders)
    logging.warning("po items")

    results = service.files().list(q=f"'{folder_dict['invoices']}' in parents").execute()
    logging.warning("res 2")

    items_invoices = results.get('files', [])
    # items_invoices = filter_pdf_items(items_invoices)
    logging.warning("inv items")

    def download_file(file_id, mime_type):
        request = None
        fh = io.BytesIO()
        
        # Check if the file is a Google Docs Editors file
        if mime_type.startswith('application/vnd.google-apps.'):
            # Choose a compatible export MIME type
            if mime_type == 'application/vnd.google-apps.document':
                export_mime_type = 'application/pdf'  # Export Google Docs as PDF
                request = service.files().export_media(fileId=file_id, mimeType=export_mime_type)
            # Add more conditions for other Google Docs Editors types if necessary
        else:
            # For binary files, use the get_media method
            request = service.files().get_media(fileId=file_id)
        
        if request:
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
            fh.seek(0)

            with open('temp.pdf', 'wb') as f:
                f.write(fh.read())
            return 1
        else:
            return None

    def move_file_to_folder(service, file_id, new_parent_id):
        """Move a file to a new folder by changing its parent."""
        # Retrieve the existing parents to remove
        print("moving file")
        file = service.files().get(fileId=file_id, fields='parents').execute()
        previous_parents = ",".join(file.get('parents'))
        # Move the file to the new folder
        service.files().update(
            fileId=file_id,
            addParents=new_parent_id,
            removeParents=previous_parents,
            fields='id, parents'
        ).execute()
        

    def read_files_from_folder(items, scanned_folder):
        for item in items:
            f = download_file(item['id'], item['mimeType'])
            if f == 1:
                with open('temp.pdf', 'rb') as f:
                    reader = PdfReader(f)
                    text = ""
                    for page in reader.pages:
                        text += page.extract_text()

                    """  text should act as a payload   """
                    print(text)
                    move_file_to_folder(service, item['id'], scanned_folder)
                    
                

    read_files_from_folder(items_purchase_orders, scanned_folder_dict['scanned_POs'])
    read_files_from_folder(items_invoices, scanned_folder_dict['scanned_invoices'])
    dumps({'status': 'success'})
    
    return dumps({'status': 'success'})
    
