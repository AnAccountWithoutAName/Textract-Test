import requests
from bs4 import BeautifulSoup
import base64
from google.oauth2.credentials import Credentials
from email.message import EmailMessage
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pprint
from email.mime.text import MIMEText
from datetime import datetime as dt
from datetime import date




url = "https://pypi.org/project/amazon-textract-textractor/#history" 

def Convert_to_datetime(string):
    return dt.strptime(string,"%Y-%m-%dT%H:%M:%S")
def Convert_to_string(datetime):
    return datetime.strftime('%b-%d-%Y')
    



def ExtractNewVersions():
    html = requests.get(url).text
    soup = BeautifulSoup(html,'html.parser')
    req_date = date(2024,2,26)
    message = []
    #for i in soup.find_all("p",class_ = "release__version-date"):
    for i in soup.find_all("p", class_ = "release__version-date"):
        current_date_str = i.time.attrs["datetime"].replace("+0000","")
        current_date = Convert_to_datetime(current_date_str).date()
        if current_date > req_date:
            message.append(f"{i.previous_sibling.previous_sibling.text.replace(' ','').rstrip()}   released on   {Convert_to_string(current_date)}")
    return message

        
        
def Send_email(content):
    
    SCOPES = ["https://www.googleapis.com/auth/gmail.readonly","https://www.googleapis.com/auth/gmail.compose"]
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    try:
        service = build("gmail","v1",credentials=  creds)



        message = MIMEText(content)

        message["To"] = "siddharth14122001@gmail.com"
        message["From"] = "home14122001@gmail.com"
        message["Subject"] = "New versions of Textractor available"

        message_encoded = base64.urlsafe_b64encode(message.as_bytes()).decode()

        create_message = {"raw": message_encoded}
        send_message = (service.users().messages().send(userId = "me", body = create_message).execute())
    except HttpError as Error:
        print(f"An error occurred: {Error}")
        send_message = None
    return send_message

def main():
    list_of_updates = ExtractNewVersions()
    if list_of_updates:
        composed_message = "The following updates are available after the specified date:\n" + "".join(list_of_updates)
        Send_email(composed_message)
                            
        



if __name__ == "__main__":
    main()
    













