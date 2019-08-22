import gspread
from oauth2client.service_account import ServiceAccountCredentials

# use creds to creat a lient to interact woth the Google Drive API
SCOPE = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

creds = ServiceAccountCredentials.from_json_keyfile_name('Email add CSV.json', SCOPE)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
sheet = client.open('Paysheet 2019-2020').sheet1

# Extract and print all of the values
list_of_hashes = sheet.get_all_records()
print(list_of_hashes)

#sheet.update_acell('B2', "UPDATED Cell")
#row = ["i'm", 'inserting','a', 'new', 'row']
#sheet.append_row(row)