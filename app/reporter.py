from slack_sdk.socket_mode import SocketModeClient
from slack_sdk.web import WebClient
from slack_sdk.socket_mode.response import SocketModeResponse
from slack_sdk.socket_mode.request import SocketModeRequest
from threading import Event, Thread
from integrations.slack.slack import SlackBot
from integrations.google.google import Google_handler
from integrations.google.templates.mail import customer_issue_template
from pprint import pprint
from integrations.jira.jira_handler import Jira_Handler
from app.models.JiraTicket import JiraTicket
from typing import List, Dict, Any
from config import config
from logger import log

class Reporter:
    
    def __init__(self):
        self.gh = Google_handler()
        self.jh = Jira_Handler()

    def slackbot_listener(client: SocketModeClient, req: SocketModeRequest) -> None:
        """
        Handles incoming Slack events and determines if they should be queued for processing.
        Filters out events not sent by the designated monitoring bot.

        Args:
            client (SocketModeClient): Slack client instance.
            req (SocketModeRequest): Incoming Slack event payload.
        """
        # Responds to Slack
        response = SocketModeResponse(envelope_id=req.envelope_id)
        client.send_socket_mode_response(response)
        
        print("Slack event...")
            
    def get_slackbot_client(self):
        slackbot = SlackBot()
        slack_client = slackbot.client
        return slack_client
        
    def begin_slackbot_listen(self, client):
        client.socket_mode_request_listeners.append(self.slackbot_listener)
        client.connect()

        log.log("BOT IS LISTENING!")

        Event().wait()
        
        
    def email_issue(self, recipient_name, recipient_email, body, subject="Issue received by Genetica", sender_alias="support@getgenetica.com"):
        service = self.gh.gmail_authenticate()
        message_text = customer_issue_template.format(recipient_name=recipient_name, body=body)
        sender_alias = 'support@getgenetica.com'  # must be an alias of authenticated account
        # recipient = 'client@example.com'
        # subject = 'Hello from Genetica'
        # body = 'This is a test email from our support alias.'
        # print(f"Recipient email before creating message: {recipient_email}")

        message = self.gh.create_gmail_message(sender_alias=sender_alias, to=recipient_email, subject=subject, message_text=message_text)
        self.gh.send_gmail(service, 'me', message)
        
    def add_to_google_sheets(self, name, email, organization, issue, status="New"):
        service = self.gh.google_sheets_authenticate()
        sheet = service.open("Tickets").sheet1
        sheet.append_row([organization, name, email, issue, status])
        
    def submit_jira_ticket(self, payload):
        name = payload['name']
        email = payload['email']
        request = payload['request']
        feedback = payload['feedback']
        organization = payload['organization']
        ticket_type = payload['ticket_type']
        origin = payload['origin']

        timestamp = payload['timestamp']
        ticket_payload, ticket_url = JiraTicket.format_ser_jira_ticket(
            issue_type=ticket_type,
            request=request,
            feedback=feedback,
            name=name,
            email=email,
            organization=organization,
            origin=origin,
            timestamp=timestamp
        )
        # print("TICKET PAYLOAD")
        # pprint(ticket_payload)
        issue_key = self.jh.post_jira_ticket(ticket_payload, ticket_url)
        return issue_key
    
