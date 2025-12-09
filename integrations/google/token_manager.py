import os
import json
import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from logger import log

class TokenManager:
    """
    Manages OAuth2 tokens for Google APIs, including storage, validation, and refresh.
    """
    
    def __init__(self, credentials_path):
        """
        Initialize the TokenManager with the path to the credentials file.
        
        Args:
            credentials_path (str): Path to the credentials JSON file
        """
        self.credentials_path = credentials_path
        self.token_dir = self._get_token_dir()
        self.token_path = self._get_token_path()
        
        # Create token directory if it doesn't exist
        os.makedirs(self.token_dir, exist_ok=True)
    
    def _get_token_dir(self):
        """Get the directory where tokens will be stored."""
        dir_path = os.path.dirname(self.credentials_path)
        return os.path.join(dir_path, 'tokens')
    
    def _get_token_path(self):
        """Get the path where the token file will be stored."""
        # Extract filename from credentials path (e.g., gmail_credentials.json -> gmail_token.json)
        cred_filename = os.path.basename(self.credentials_path)
        token_filename = cred_filename.replace('credentials', 'token')
        return os.path.join(self.token_dir, token_filename)
    
    def token_exists(self):
        """Check if a token file exists."""
        return os.path.exists(self.token_path)
    
    def load_token(self):
        """
        Load token from file.
        
        Returns:
            dict: The token data or None if file doesn't exist
        """
        if not self.token_exists():
            return None
            
        try:
            with open(self.token_path, 'r') as token_file:
                return json.load(token_file)
        except (json.JSONDecodeError, IOError) as e:
            log.log(f"Error loading token: {str(e)}")
            return None
    
    def save_token(self, token_data):
        """
        Save token data to file.
        
        Args:
            token_data (dict): Token data to save
        """
        try:
            with open(self.token_path, 'w') as token_file:
                json.dump(token_data, token_file, indent=2)
            
            # Set appropriate file permissions (readable only by owner)
            os.chmod(self.token_path, 0o600)
            
            log.log(f"Token saved successfully to {self.token_path}")
        except IOError as e:
            log.log(f"Error saving token: {str(e)}")
    
    def get_credentials(self, scopes=None):
        """
        Get valid credentials for Google API access.
        
        This method checks for existing tokens, validates them, and refreshes if necessary.
        If no valid token exists, it raises an exception indicating setup is required.
        
        Args:
            scopes (list, optional): List of scopes required. Defaults to None.
        
        Returns:
            Credentials: Valid Google OAuth2 credentials
            
        Raises:
            Exception: If no valid token exists and setup is required
        """
        token_data = self.load_token()
        
        if not token_data:
            raise Exception(
                "No token found. Please run the setup script to authenticate: "
                "python -m integrations.google.setup_auth"
            )
        
        # Create credentials from token data
        creds = Credentials.from_authorized_user_info(token_data)
        
        # Check if token is expired and can be refreshed
        if creds.expired and creds.refresh_token:
            try:
                log.log("Token expired. Refreshing...")
                creds.refresh(Request())
                
                # Save the refreshed token
                token_data = {
                    'token': creds.token,
                    'refresh_token': creds.refresh_token,
                    'token_uri': creds.token_uri,
                    'client_id': creds.client_id,
                    'client_secret': creds.client_secret,
                    'scopes': creds.scopes,
                    'expiry': creds.expiry.isoformat()
                }
                self.save_token(token_data)
                log.log("Token refreshed successfully")
            except Exception as e:
                log.log(f"Error refreshing token: {str(e)}")
                raise Exception(f"Failed to refresh token: {str(e)}")
        
        return creds
    
    def save_credentials(self, credentials):
        """
        Save credentials obtained from OAuth2 flow.
        
        Args:
            credentials (Credentials): Google OAuth2 credentials
        """
        token_data = {
            'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes,
            'expiry': credentials.expiry.isoformat() if credentials.expiry else None
        }
        self.save_token(token_data)