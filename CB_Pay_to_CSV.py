import os
import datetime as dt
import re
import requests
import pdftotext
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import base64
import Conf

dl_dir = os.listdir('/home/ryan/Downloads')

today = dt.datetime.today().date()
two_weeks_ago = (today - dt.timedelta(days=13))


def Upload_to_Gsheets(Paysheet_row):
    # use creds to creat a lient to interact woth the Google Drive API
    SCOPE = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

    creds = ServiceAccountCredentials.from_json_keyfile_name('Email add CSV.json', SCOPE)
    client = gspread.authorize(creds)

    # Find a workbook by name and open the first sheet
    sheet = client.open('Paysheet 2019-2020').sheet1

    # Extract and print all of the values of payslip date col
    datelist = sheet.col_values(1)
    if Paysheet_row[0] in datelist:
        print('already uploaded')
    
    elif Paysheet_row[0] not in datelist:
        sheet.append_row(Paysheet_row)
        print(f"adding new row for date {Paysheet_row[0]}")


def Get_Paysheet_info(file):
    with open(f'/home/ryan/Downloads/{file}', 'rb') as file:
        pdf = pdftotext.PDF(file)

    paysheet_pdf = pdf[0].split()

    # for num,thing in enumerate(paysheet_pdf):
    #     print(num, thing)

    Legend ={ "Date": 21, "PeriodStart": 28, "PeriodFinish": 30, "Gross": 33, "Tax":  60, "Net": 43,
    "Hours": 53,"Rate": 24,  "SuperAdd": 65, "SuperTotal": 66, "TotalTax": 61, "YTD": 56}
    
    pay_info_list =[paysheet_pdf[item] for item in Legend.values()]
    
    return pay_info_list


def Get_Attachments(message, service): #Downloads attachment and adds date
	
	for part in message['payload']['parts']:
		if part['filename']:			
			attachment = service.users().messages().attachments().get(userId='Me', messageId=message['id'], id=part['body']['attachmentId']).execute()
			file_data = base64.urlsafe_b64decode(attachment['data'].encode('UTF-8'))
			path = ''.join([store_dir, '.'.join([str(today), part['filename']])]) #join date to filename, then to storepath
			f = open(path, 'wb')
			f.write(file_data)
			f.close()


def Get_Email():
    SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'

    #Check for store creds, otherwise you have to auth them
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('gmail', 'v1', http=creds.authorize(Http()))
	    
	# Call the Gmail API to fetch INBOX
    results = service.users().messages().list(userId='me',labelIds = ['INBOX']).execute()
    messagesID = results.get('messages', []) #returns Dict with {'id': 'value', 'threadId': 'value'} of inbox messages
	
	
	
    for message in messagesID[:15]: #sorts through messages via thier ID
        msg = service.users().messages().get(userId='me', id=message['id']).execute()
        headrs = msg['payload']['headers'] #headers include to, from, subject, date and more

        for item in headrs:
            if item['name'] == 'From' and item['value'] == Conf.CB_email: # ['name':'From'] in headrs that has ['value': 'myemail']
                Get_Attachments(msg, service)
                return True

def Check_Online():
    try:
        if requests.get('https://google.com').ok:
            print("You're Online")
    except:
        print("You're Offline")
        os._exit(1)

def main():
    Check_Online()

    file_exists = bool(False)

    for file in dl_dir:
            
        try:
            match = re.match(r'^(\d\d\d\d)-(\d\d)-(\d\d)', file)
        except ValueError as ValErr:
            continue
    
        if match != None: 
            filedate = dt.datetime.strptime(file[:10], '%Y-%m-%d')
            if today > filedate.date() and filedate.date() > two_weeks_ago:
                # if file exists, pipe name to pdf to text
                Upload_to_Gsheets(Get_Paysheet_info(file))
            
                file_exists = True
                break
            else:
                continue
        
    if file_exists:
        pass
    else:
        print("checking Email")
        if Get_Email() == True:
            print("Got Attachment")
            main()
        else:
            print("No payslip email found")



if __name__ == '__main__':
	main()