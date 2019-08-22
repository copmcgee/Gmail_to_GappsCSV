from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import base64
import datetime as dt
import Conf

store_dir = "c:/cisco/"
today = dt.datetime.today().date()
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'



def Get_Attachments(message, service): #Downloads attachment and adds date
	for part in message['payload']['parts']:
		if part['filename']:			
			attachment = service.users().messages().attachments().get(userId='Me', messageId=message['id'], id=part['body']['attachmentId']).execute()
			file_data = base64.urlsafe_b64decode(attachment['data'].encode('UTF-8'))
			path = ''.join([store_dir, '.'.join([str(today), part['filename']])]) #join date to filename, then to storepath
			f = open(path, 'wb')
			f.write(file_data)
			f.close()







def main():
   
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


	

					
					




if __name__ == '__main__':
	main()
