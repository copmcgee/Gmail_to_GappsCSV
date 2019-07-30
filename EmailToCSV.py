from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import base64

SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'

def main():
   
	store = file.Storage('token.json')
	creds = store.get()
	if not creds or creds.invalid:
		flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
		creds = tools.run_flow(flow, store)
	service = build('gmail', 'v1', http=creds.authorize(Http()))
	
    
    # Call the Gmail API to fetch INBOX
	results = service.users().messages().list(userId='me',labelIds = ['INBOX']).execute()
	#messages = results.get('messages', [])
	
	message_id = results['messages'][3]['id']
	
	message = service.users().messages().get(userId='me', id=message_id).execute()
	print(message['snippet'])
	for part in message['payload']['parts']:
            if part['filename']:
                if 'data' in part['body']:
                    data = part['body']['data']
                else:
                    att_id = part['body']['attachmentId']
                    att = service.users().messages().attachments().get(userId='me', messageId=message_id, id=att_id).execute()
                    data = att['data']
                file_data = base64.urlsafe_b64decode(data.encode('UTF-8'))
                print(file_data)

if __name__ == '__main__':
	main()