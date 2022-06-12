import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import httplib2
import googleapiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload,MediaFileUpload
import os
import time

def getStudents():

	scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

	creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)

	client = gspread.authorize(creds)

	#os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/kabirmoghe/Desktop/essayApp/creds.json'
	os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'creds.json'
	drive = googleapiclient.discovery.build('drive','v3')

	service = drive.files().list(fields='files(id, name, mimeType, parents)').execute()['files']

	driveInfo = pd.DataFrame(service)

	driveInfo = driveInfo[(driveInfo["parents"].isnull() == False)]
	driveInfo["parents"] = driveInfo["parents"].apply(lambda val: val[0])

	students = list(driveInfo[driveInfo["parents"] == '1EncvaZIVEUXKWWbqq0-0JrcH2abJwV-g']['name'])

	return students

def downloadFiles(name):

	begin = time.time()

	print("Setting Up")

	scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

	creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)

	client = gspread.authorize(creds)

	os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'creds.json'
	drive = googleapiclient.discovery.build('drive','v3')

	service = drive.files().list(fields='files(id, name, mimeType,parents)').execute()['files']

	driveInfo = pd.DataFrame(service)

	driveInfo = driveInfo[(driveInfo["parents"].isnull() == False)]
	driveInfo["parents"] = driveInfo["parents"].apply(lambda val: val[0])

	students = list(driveInfo[driveInfo["parents"] == '1EncvaZIVEUXKWWbqq0-0JrcH2abJwV-g']['name'])

	# Student Specific

	df = driveInfo[driveInfo["name"].str.contains(name)]  

	# Docs

	docs = df[df["mimeType"] == "application/vnd.google-apps.document"]

	docIds = list(docs['id'])
	docNames = list(docs['name'])
	    
	# Makes parent directory for student

	print("Creating Directories")


	if name not in os.listdir():
	    os.mkdir(name)

	    os.mkdir("{}/Drafts".format(name))
	    os.mkdir("{}/Sheets".format(name))

	# Docs

	print("Creating Docs")

	docStart = time.time()

	currentDocs = os.listdir("{}/Drafts".format(name))
	currentDocs = [doc.split('.docx')[0] for doc in currentDocs]     

	for i in range(len(docIds)):
	    
	    docName = docNames[i]
	    
	    if docName not in currentDocs:
	        
	        print("Downloading {}".format(docName))
	    
	        doc = drive.files().export_media(fileId = docIds[i], mimeType = "application/vnd.openxmlformats-officedocument.wordprocessingml.document").execute()

	        with open("{}/Drafts/{}.docx".format(name, docName), "wb") as f:
	            f.write(doc)
	    else:
	        print("Skipping {}".format(docName))
	        
	docEnd = time.time()
	        
	print("Docs Time: {}".format(round(docEnd-docStart, 1)))
	        
	# Sheets
	    
	print("Creating Sheets")

	sheetStart = time.time()

	sheets = df[df["mimeType"] == "application/vnd.google-apps.spreadsheet"]

	sheetNames = list(sheets['name'])

	currentSheets = os.listdir("{}/Sheets".format(name))
	currentSheets = [sheet.split('.csv')[0] for sheet in currentSheets]                      

	for sheetName in sheetNames:
	    
	    if sheetName not in currentSheets:

	        sheet = client.open(sheetName).sheet1

	        print("Downloading {}".format(sheetName))

	        df = pd.DataFrame(sheet.get_all_records())

	        df.to_csv("{}/Sheets/{}.csv".format(name, sheetName))
	    else:
	        print("Skipping {}".format(sheetName))
	    
	sheetEnd = time.time()
	        
	print("Sheets Time: {}".format(round(sheetEnd-sheetStart, 1)))
	    
	print("Finished Connecting and Downloading")

	end = time.time()

	total = round(end-begin, 1)

	print("Total: {} seconds".format(total))
