from slack_sdk.socket_mode import SocketModeClient
from slack_sdk.web import WebClient
from slack_sdk.socket_mode.response import SocketModeResponse
from slack_sdk.socket_mode.request import SocketModeRequest
from threading import Event, Thread
# from app.models.JiraTicket import JiraTicket
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

def sanitize_string(string):
	print("SANITIZING STRING...")
	return string.replace("“", "\"").replace("”", "\"")

def extract_email_from_slack_payload(payload):
	print("EXTRACTING EMAIL...")
	for element in payload['event']['blocks'][0]['elements'][0]['elements']:
		# print("ELEMENT:", element)
		if element['type'] == "link":
			return element['text']
		
def parse_slack_payload(channel, payload):
	print('CHANNEL:', channel)
	if channel == 'serve-ai-idea':
		payload_origin = payload['event']['blocks'][1]['text']['text']
		payload_origin_array = payload_origin.split('\n')
		name = payload_origin_array[0].replace("*Submitted by:* ", '')
		email = payload_origin_array[1].replace("*Email:* <mailto:", '')[:-2].split('|')[0]
		organization = payload_origin_array[2].replace("*Organization:* ", '')
		user_id = payload_origin_array[3].replace("*User ID:* ", '')
		timestamp = payload_origin_array[4].replace("*Timestamp:* ", '')
		event_text = payload['event']['text'].replace(f'New idea from {name}: ', '')
		payload_dict = {
			'name': name,
			'email': email,
			'organization': organization,
			'user_id': user_id,
			'timestamp': timestamp,
			'text': event_text,
			'ticket_type': 'Task'
		}

	if channel == 'serve-ai-issue':
		payload_origin = payload['event']['attachments'][0]['blocks'][1]['text']['text']
		payload_origin_array = payload_origin.split('\n')
		name = payload_origin_array[0].replace("*Submitted by:* ", '')
		email = payload_origin_array[1].replace("*Email:* <mailto:", '')[:-2].split('|')[0]
		organization = payload_origin_array[2].replace("*Organization:* ", '')
		user_id = payload_origin_array[3].replace("*User ID:* ", '')
		timestamp = payload_origin_array[4].replace("*Timestamp:* ", '')
		issue_type = payload['event']['attachments'][0]['blocks'][3]['text']['text'].split('\n')[1].split(' ')[1]
		issue_urgency = payload['event']['attachments'][0]['blocks'][4]['text']['text'].split('\n')[1].split(' ')[1:][0]
		issue_description = payload['event']['attachments'][0]['blocks'][5]['text']['text'].split('```\n')[1][:-4]
		issue_id = payload['event']['attachments'][0]['blocks'][7]['elements'][0]['text'].split(' ')[-1][1:-1]

		payload_dict = {
			'name': name,
			'email': email,
			'organization': organization,
			'user_id': user_id,
			'timestamp': timestamp,
			'issue_type': issue_type,
			'issue_urgency': issue_urgency,
			'issue_description': issue_description,
			'issue_id': issue_id,
			'ticket_type': 'Bug'
		}		


	elif channel == 'bot-testing':
		return f"Message successfully received from bot-testing: {payload['event']['text']}"

	try:
		return payload_dict
	except NameError as e:
		print("ERROR: No payload_dict found!")
		return
	

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
		'C098ZBUGS07': 'serve-ai-issue'
	}
	# Responds to Slack
	response = SocketModeResponse(envelope_id=req.envelope_id)
	client.send_socket_mode_response(response)
	
	print("Slack event...")

	try:
		# print("EVENT PAYLOAD:")
		# pprint(req.payload)
		channel = channel_dict[req.payload['event']['channel']]
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
		event_content = parse_slack_payload(channel, req.payload)
		print('CONTENT:')
		pprint(event_content)
	except Exception as e:
		print("UNHANDLED ERROR:", e.__str__())	
		print("PAYLOAD:")
		pprint(req.payload)
		return
		
	r = Reporter()
	# r.submit_jira_ticket("SER", event_content)
	r.email_issue(recipient_name=event_content['name'], recipient_email=event_content['email'], body=event_content['text'])




slackbot = SlackBot()
slack_client = slackbot.client
slack_client.socket_mode_request_listeners.append(slackbot_listener)
slack_client.connect()

log.log("BOT IS LISTENING!")

Event().wait()
