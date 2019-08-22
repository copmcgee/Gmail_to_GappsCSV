from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import base64
#import datetime as dt
from time import sleep
from selenium import webdriver
from bs4 import BeautifulSoup as BSoup
from selenium.common.exceptions import UnexpectedAlertPresentException
import Conf

store_dir = "c:/users/st01529/Desktop"
#today = dt.datetime.today().date()
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'


def Get_Payslip():
	options = webdriver.FirefoxOptions()  #sets headless mode
	options.add_argument('--headless')
	browser = webdriver.Firefox() #(options=options)
	browser.get("https://secure.mopt.com.au/ConnX/")

	username = browser.find_element_by_id("ctl00_cphMainContent_txtUserName")
	password = browser.find_element_by_id("ctl00_cphMainContent_txtPassword")
	submit = browser.find_element_by_id("ctl00_cphMainContent_cbLogin")

	username.send_keys(Conf.user)
	password.send_keys(Conf.password)

	submit.click()  # login
	sleep(2)
	try: # for silly password expiring alert
		alert = browser.switch_to_alert()
		alert.dismiss()

	except UnexpectedAlertPresentException:
		pass
		
	browser.get('https://secure.mopt.com.au/ConnX/frmPayAdvices.aspx')
	sleep(2)

	bs_obj = BSoup(browser.page_source, 'html.parser') #Get most recent payslip
	table = bs_obj.find('table', id="ctl00_cphMainContent_rgGrid_ctl00").find('tbody').find('a')
		
	browser.get("https://secure.mopt.com.au/ConnX/" + table['href'])

	#TODO pull data from PDF in browser
	

	#browser.close()


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
			if item['name'] == 'From' and item['value'] == Conf.MOPT_email: # ['name':'From'] in headrs that has ['value': 'myemail']
				Get_Payslip()


	

					
					




if __name__ == '__main__':
	main()
