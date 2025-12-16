from slack_sdk.socket_mode import SocketModeClient
from slack_sdk.web import WebClient
from slack_sdk.socket_mode.response import SocketModeResponse
from slack_sdk.socket_mode.request import SocketModeRequest
from threading import Event, Thread
# from app.models.JiraTicket import JiraTicket
from helpers.formatter import Formatter
from integrations.slack.slack import SlackBot
from integrations.google.google import Google_handler
from app.reporter import Reporter
from integrations.jira.jira_handler import Jira_Handler
from pprint import pprint
# from typing import List, Dict, Any
from config import config
from logger import log
import traceback
import json

def slackbot_listener(client: SocketModeClient, req: SocketModeRequest) -> None:
	"""
	Handles incoming Slack events and determines if they should be queued for processing.
	Filters out events not sent by the designated monitoring bot.
	Args:
		client (SocketModeClient): Slack client instance.
		req (SocketModeRequest): Incoming Slack event payload.
	"""
	channel_dict = {
		'C0997D35KA7': 'serve-ai-idea',
		'C097CTAP4Q7': 'serve-ai-support',
		'C08LSADUE58': 'bot-testing',
		'C098ZBUGS07': 'serve-ai-issue',
		'C0A2Q6D3B4H': 'serve-ai-thumbs-up-down'
	}
	# Responds to Slack
	response = SocketModeResponse(envelope_id=req.envelope_id)
	client.send_socket_mode_response(response)
	
	print("Slack event...")

	try:
		print("EVENT PAYLOAD:")
		pprint(req.payload)
		channel = channel_dict[req.payload['event']['channel']]
		message_timestamp = req.payload['event']['ts']
		print("MESSAGE TIMESTAMP:", message_timestamp)
	except KeyError as e:
		print("Message in unknown channel. Channel ID:", e)
		print("PAYLOAD:")
		pprint(req.payload)
		return
	except Exception as e:
		print("UNHANDLED ERROR:", e.__str__())	
		print("PAYLOAD:")
		pprint(req.payload)
		return

	try:
		feedback_message_content = formatter.parse_slack_payload(channel, req.payload)
		print('CONTENT:')
		pprint(feedback_message_content)
	except Exception as e:
		print("UNHANDLED ERROR:", e.__str__())	
		print("PAYLOAD:")
		pprint(req.payload)
		return
		
	if feedback_message_content:
		try:
			jira_issue_key = reporter.submit_jira_ticket(payload=feedback_message_content)
			print("Jira issue created with key:", jira_issue_key)
			reply_content = "Jira Issue Key: " + jira_issue_key
		except Exception as e:
			reply_content = "There was an error submitting the Jira ticket: " + e.__str__()
			print("ERROR SUBMITTING JIRA TICKET:", traceback.format_exc())

		slackbot.reply_to_alert(ts=message_timestamp, content=reply_content)


slackbot = SlackBot()
formatter = Formatter()
reporter = Reporter()
slack_client = slackbot.client
slack_client.socket_mode_request_listeners.append(slackbot_listener)
slack_client.connect()

log.log("BOT IS LISTENING!")

Event().wait()
