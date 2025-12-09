import os
import gspread
import base64
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from oauth2client.service_account import ServiceAccountCredentials
from integrations.google.token_manager import TokenManager
from logger import log

class Google_handler:

    def __init__(self):
        self.gmail_credentials_filepath = self.concatenate_file_path("gmail_credentials.json")
        self.gsheets_credentials_filepath = self.concatenate_file_path("gsheets_credentials.json")
        self.token_manager = TokenManager(self.gmail_credentials_filepath)
        
    
    def concatenate_file_path(self, filename):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(current_dir, filename)
    
    def google_sheets_authenticate(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        credentials_path = os.path.join(current_dir, self.gsheets_credentials_filepath)
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        # print("CREDENTIALS:", credentials_path)
        creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)
        client = gspread.authorize(creds)
        
        return client
        
    def gmail_authenticate(self):
        """
        Authenticate with Gmail API using stored tokens.
        
        Returns:
            service: Authenticated Gmail API service
            
        Raises:
            Exception: If authentication fails
        """
        try:
            # Set environment variable for local testing if needed
            os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"  # needed for HTTP localhost
            
            # Get credentials from token manager
            scopes = ['https://www.googleapis.com/auth/gmail.send']
            creds = self.token_manager.get_credentials(scopes)
            
            # Build and return the Gmail service
            return build('gmail', 'v1', credentials=creds)
        except Exception as e:
            log.log(f"Gmail authentication failed: {str(e)}")
            raise Exception(f"Failed to authenticate with Gmail: {str(e)}")

    def create_gmail_message(self, sender_alias, to, subject, message_text):
        message = MIMEText(message_text)
        message['to'] = to
        message['from'] = sender_alias  # This must be a verified alias in Gmail
        message['subject'] = subject

        raw = base64.urlsafe_b64encode(message.as_bytes())
        return {'raw': raw.decode()}

    def send_gmail(self, service, sender, message_body):
        try:
            sent_message = service.users().messages().send(userId=sender, body=message_body).execute()
            print(f'Message Id: {sent_message["id"]}')
            return sent_message
        except Exception as error:
            print(f'An error occurred: {error}')
            return None