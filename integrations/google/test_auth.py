#!/usr/bin/env python3
"""
Test script for Google API authentication.

This script tests the automated authentication flow for Google APIs.
It verifies that the TokenManager and modified Google_handler classes
work correctly together.

Usage:
    python -m integrations.google.test_auth

"""

import os
import argparse
from integrations.google.google import Google_handler
from integrations.google.token_manager import TokenManager
from logger import log

def test_token_manager(credentials_path):
    """
    Test the TokenManager class.
    
    Args:
        credentials_path (str): Path to the credentials JSON file
        
    Returns:
        bool: True if test passed, False otherwise
    """
    try:
        log.log(f"Testing TokenManager with credentials: {credentials_path}")
        
        # Create token manager
        token_manager = TokenManager(credentials_path)
        
        # Check if token exists
        if token_manager.token_exists():
            log.log("✅ Token file exists")
        else:
            log.log("❌ Token file does not exist. Please run setup_auth.py first")
            return False
        
        # Load token
        token_data = token_manager.load_token()
        if token_data:
            log.log("✅ Token loaded successfully")
        else:
            log.log("❌ Failed to load token")
            return False
        
        # Get credentials
        try:
            creds = token_manager.get_credentials()
            log.log("✅ Credentials obtained successfully")
            
            # Check if token was refreshed
            if creds.valid:
                log.log("✅ Credentials are valid")
            else:
                log.log("❌ Credentials are not valid")
                return False
                
            return True
        except Exception as e:
            log.log(f"❌ Failed to get credentials: {str(e)}")
            return False
            
    except Exception as e:
        log.log(f"❌ TokenManager test failed: {str(e)}")
        return False

def test_gmail_authentication():
    """
    Test Gmail authentication using the modified Google_handler.
    
    Returns:
        bool: True if test passed, False otherwise
    """
    try:
        log.log("Testing Gmail authentication")
        
        # Create Google handler
        google_handler = Google_handler()
        
        # Authenticate with Gmail
        try:
            service = google_handler.gmail_authenticate()
            log.log("✅ Gmail authentication successful")
            
            # Test a simple API call to verify the service works
            profile = service.users().getProfile(userId='me').execute()
            log.log(f"✅ Gmail API call successful. Email address: {profile.get('emailAddress')}")
            
            return True
        except Exception as e:
            log.log(f"❌ Gmail authentication failed: {str(e)}")
            return False
            
    except Exception as e:
        log.log(f"❌ Gmail authentication test failed: {str(e)}")
        return False

def main():
    """Main function to run the authentication tests."""
    parser = argparse.ArgumentParser(description="Test Google API authentication")
    parser.add_argument(
        "--service", 
        choices=["gmail", "all"], 
        default="all",
        help="Google service to test (default: all)"
    )
    args = parser.parse_args()
    
    # Get the directory of this script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    credentials_path = os.path.join(current_dir, "gmail_credentials.json")
    
    # Test TokenManager
    token_manager_test = test_token_manager(credentials_path)
    
    # Test Gmail authentication if requested or if testing all services
    if args.service in ["gmail", "all"]:
        gmail_test = test_gmail_authentication()
    else:
        gmail_test = True  # Skip test
    
    # Print summary
    print("\n=== Test Summary ===")
    print(f"TokenManager: {'✅ PASSED' if token_manager_test else '❌ FAILED'}")
    if args.service in ["gmail", "all"]:
        print(f"Gmail Authentication: {'✅ PASSED' if gmail_test else '❌ FAILED'}")
    
    # Overall result
    if token_manager_test and gmail_test:
        print("\n✅ All tests passed! The automated authentication is working correctly.")
    else:
        print("\n❌ Some tests failed. Please check the logs for details.")

if __name__ == "__main__":
    main()