import csv
import os

import gspread
from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials

# Environment
load_dotenv()
CREDENTIALS = os.getenv('GOOGLE_CREDENTIALS')
SHEET = os.getenv('GOOGLESHEET_ID')

def get_sheet_instance(sheet_id):
    scope = ["https://spreadsheets.google.com/feeds",
             "https://www.googleapis.com/auth/spreadsheets",
             "https://www.googleapis.com/auth/drive.file",
             "https://www.googleapis.com/auth/drive"]

    credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS + '.json', scope)
    client = gspread.authorize(credentials)
    return client.open_by_key(sheet_id)

def upload_to_sheets(sh, data_path):
    with open(data_path, 'r') as f:
        csv_file = list(csv.reader(f))

    cols = str(len(csv_file[0]))
    rows = str(len(csv_file))

    try:
        sh.add_worksheet(title=worksheet_name, rows=rows, cols=cols)
    except:
        print("Worksheet {} already exists".format(worksheet_name))

    sh.values_update(
        worksheet_name,
        params={'valueInputOption': 'USER_ENTERED'},
        body={'values': csv_file}
    )

