# Gmail-Jira Automation

A comprehensive automation system for handling customer feedback, issues, and ideas through Slack, Gmail, and Jira integration.

## Overview

This project provides an automated workflow for processing customer feedback received through Slack channels. The system:

1. Listens for messages in designated Slack channels
2. Parses and categorizes incoming messages (ideas, issues, support requests)
3. Creates Jira tickets for tracking and data recording
4. Sends confirmation emails to customers

The application is designed to streamline customer support operations and ensure that all customer communications are properly tracked, responded to, and resolved.

## System Architecture

The application follows a modular architecture with clear separation of concerns:

```
├── app/                    # Core application logic
│   ├── app.py              # Main application entry point
│   ├── reporter.py         # Handles reporting and integration coordination
│   └── models/             # Data models
│       └── JiraTicket.py   # Jira ticket formatting
├── config/                 # Configuration management
│   └── config.py           # Environment variables and configuration
├── integrations/           # External service integrations
│   ├── google/             # Google API integration (Gmail)
│   ├── jira/               # Jira API integration
│   └── slack/              # Slack API integration
└── logger/                 # Logging utilities
    └── log.py              # Centralized logging
```

## Features

### Slack Integration

- Real-time monitoring of designated Slack channels
- Automatic parsing of structured messages
- Support for different message formats (ideas, issues, support requests)
- Channel-specific processing logic

### Google Integration

- **Gmail**: Automated email responses to customers
- Secure token management with automatic refresh
- Support for service account authentication

### Jira Integration

- Automatic ticket creation based on message type
- Custom ticket formatting with customer information
- Data recording for reporting and analysis
- Sprint management capabilities
- Status tracking and updates
- Comment management

## Setup and Configuration

### Prerequisites

- Python 3.7+
- Slack App with Socket Mode enabled
- Google API credentials
- Jira API access
- Environment variables configured

### Environment Variables

Create a `.env` file in the project root with the following variables:

```
# Slack Configuration
SLACK_BOT_TOKEN=xoxb-your-token
SLACK_APP_TOKEN=xapp-your-token
SLACK_CHANNEL_ID=C0123456789
BOT_TESTING_SLACK_CHANNEL_ID=C9876543210

# Jira Configuration
JIRA_EMAIL=your-jira-email@example.com
JIRA_API_TOKEN=your-jira-api-token
JIRA_BASE_URL=https://your-domain.atlassian.net
JIRA_PROJECT_KEY=YOUR_PROJECT

# Google API Configuration
# (Credentials are stored in json files)

# Other Services
OPEN_AI_API_KEY=your-openai-key
LANGWATCH_API_KEY=your-langwatch-key
QDRANT_API_KEY=your-qdrant-key
QDRANT_CLUSTER_URL=your-qdrant-url
```

### Google API Setup

1. Run the setup script to authenticate with Google:
   ```bash
   python -m integrations.google.setup_auth
   ```

2. Verify the authentication is working:
   ```bash
   python -m integrations.google.test_auth
   ```

### Running the Application

Start the application with:

```bash
python -m app.app
```

The application will connect to Slack and begin listening for events in the configured channels.

## Message Processing Flow

1. **Slack Event Reception**: The application listens for messages in configured Slack channels
2. **Message Parsing**: Extracts structured data from the message format
3. **Jira Ticket Creation**: Creates a Jira ticket with the extracted information
4. **Email Confirmation**: Sends an email to the customer confirming receipt
5. **Data Recording**: Records the information in Jira for tracking and analysis

## Channel-Specific Processing

The application handles different types of messages based on the Slack channel:

- **serve-ai-idea**: Processes customer ideas and feature requests
- **serve-ai-issue**: Processes bug reports and technical issues
- **serve-ai-support**: Processes general support requests
- **bot-testing**: Used for testing the bot functionality

## Future Enhancements

- **Enhanced Analytics**: Integration with data visualization tools
- **Automated Triage**: AI-powered categorization and prioritization of issues
- **Customer Portal**: Web interface for customers to track their submissions
- **SLA Monitoring**: Tracking and alerting for Service Level Agreement (SLA) response time commitments
- **Integration with Additional Services**: Support for more communication channels
- **Automated Resolution**: AI-assisted resolution suggestions for common issues
- **Feedback Collection**: Automated follow-up for customer satisfaction