import gspread
from oauth2client.service_account import ServiceAccountCredentials
from settings import GOOGLE_SHEET_ID

scope = ["https://spreadsheets.google.com/feeds"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)


def get_sheet_rows():
    sheet = client.open_by_key(GOOGLE_SHEET_ID).sheet1
    return sheet.get_all_records()
