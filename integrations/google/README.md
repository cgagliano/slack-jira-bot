# Google API Authentication Automation

This module provides automated authentication for Google APIs, eliminating the need for manual intervention when authenticating with Google services.

## Overview

The solution implements a token management system that securely stores and automatically refreshes OAuth2 tokens, allowing the application to interact with Google APIs seamlessly without requiring users to manually visit authorization URLs.

## Components

- **TokenManager**: Manages OAuth2 tokens, including storage, validation, and refresh
- **Modified Google_handler**: Uses the TokenManager for authentication
- **Setup Script**: One-time setup for initial authentication
- **Test Script**: Verifies the authentication flow works correctly

## Setup Instructions

### 1. Initial Authentication (One-time Setup)

Before using the automated authentication, you need to perform a one-time setup to obtain the initial tokens:

```bash
# Run the setup script
python -m integrations.google.setup_auth
```

This will:
1. Open a browser window for you to authenticate with Google
2. Request the necessary permissions
3. Save the tokens securely for future use

### 2. Testing the Authentication

After the initial setup, you can verify that the automated authentication is working correctly:

```bash
# Run the test script
python -m integrations.google.test_auth
```

This will:
1. Test the TokenManager functionality
2. Test the Gmail authentication
3. Verify that no manual intervention is required

## Usage

Once set up, the application will automatically handle authentication with Google APIs. The `Google_handler` class has been modified to use the TokenManager, so no changes are needed in how you use the existing methods.

Example:

```python
from integrations.google.google import Google_handler

# Create Google handler
google_handler = Google_handler()

# Authenticate with Gmail (now uses stored tokens)
service = google_handler.gmail_authenticate()

# Use the service as before
message = google_handler.create_gmail_message(
    sender_alias='support@example.com',
    to='recipient@example.com',
    subject='Test Email',
    message_text='This is a test email'
)
google_handler.send_gmail(service, 'me', message)
```

## Token Management

Tokens are stored securely in the `integrations/google/tokens/` directory. The TokenManager handles:

- Token validation
- Automatic token refresh when expired
- Secure storage of tokens

## Troubleshooting

If you encounter authentication issues:

1. Check that the token file exists in the `tokens` directory
2. Run the test script to verify the authentication flow
3. If needed, run the setup script again to obtain new tokens

## Security Considerations

- Token files contain sensitive information and should be protected
- The `tokens` directory is added to `.gitignore` to prevent accidental commits
- File permissions are set to be readable only by the application user