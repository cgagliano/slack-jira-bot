#!/usr/bin/env python3
"""
Setup script for Google API authentication.

This script performs the initial OAuth2 flow to obtain tokens for Google APIs.
It should be run once to set up authentication, after which the application
can use the stored tokens for automated authentication.

Usage:
    python -m integrations.google.setup_auth

"""

import os
import argparse
from google_auth_oauthlib.flow import InstalledAppFlow
from integrations.google.token_manager import TokenManager
from logger import log

def setup_gmail_auth(credentials_path, scopes):
    """
    Perform the initial OAuth2 flow for Gmail authentication.
    
    Args:
        credentials_path (str): Path to the credentials JSON file
        scopes (list): List of OAuth scopes to request
        
    Returns:
        bool: True if authentication was successful, False otherwise
    """
    try:
        log.log(f"Starting Gmail authentication setup with credentials: {credentials_path}")
        
        # Set environment variable for local testing
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"  # needed for HTTP localhost
        
        # Create the flow using client secrets file
        flow = InstalledAppFlow.from_client_secrets_file(
            credentials_path,
            scopes=scopes
        )
        
        # Run the OAuth flow with a local server
        log.log("Opening browser for authentication. Please follow the prompts...")
        credentials = flow.run_local_server(port=0)
        
        # Create token manager and save credentials
        token_manager = TokenManager(credentials_path)
        token_manager.save_credentials(credentials)
        
        log.log("Authentication successful! Tokens have been saved.")
        log.log(f"Token stored at: {token_manager.token_path}")
        return True
        
    except Exception as e:
        log.log(f"Error during authentication setup: {str(e)}")
        return False

def main():
    """Main function to run the authentication setup."""
    parser = argparse.ArgumentParser(description="Set up Google API authentication")
    parser.add_argument(
        "--service", 
        choices=["gmail", "sheets"], 
        default="gmail",
        help="Google service to authenticate (default: gmail)"
    )
    args = parser.parse_args()
    
    # Get the directory of this script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    if args.service == "gmail":
        credentials_path = os.path.join(current_dir, "gmail_credentials.json")
        scopes = ['https://www.googleapis.com/auth/gmail.send']
        
        if setup_gmail_auth(credentials_path, scopes):
            print("\n✅ Gmail authentication setup completed successfully!")
            print("\nYou can now use the application without manual authentication.")
        else:
            print("\n❌ Gmail authentication setup failed.")
            print("\nPlease check the logs and try again.")
    
    elif args.service == "sheets":
        print("\nℹ️ Google Sheets is already using service account authentication.")
        print("No setup is required for Google Sheets.")

if __name__ == "__main__":
    main()