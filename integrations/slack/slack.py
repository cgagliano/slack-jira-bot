from slack_sdk.socket_mode import SocketModeClient
from slack_sdk.web import WebClient
from slack_sdk.socket_mode.response import SocketModeResponse
from slack_sdk.socket_mode.request import SocketModeRequest
from slack_sdk.errors import SlackApiError
# from typing import List, Dict, Any
from logger import log
from config import config

class SlackBot:
	
	def __init__(self) -> None:
		"""
		Initializes the SlackBot instance by setting up a Slack SocketModeClient.
		"""
		self.client = self.initialize_client()
		
	def initialize_client(self) -> SocketModeClient:
		"""
		Initializes and returns a SocketModeClient for Slack integration.

		Returns:
			SocketModeClient: A configured Slack client for socket-based communication.
		"""

	
		client = SocketModeClient(
			app_token=config.SLACK_APP_TOKEN,
			web_client=WebClient(token=config.SLACK_BOT_TOKEN) 
		)
		
		return client
	
	def listener(self, client: SocketModeClient, req: SocketModeRequest) -> None:
		"""
		Handles incoming Slack events and responds to the envelope.
		Meant to be connected as the Slack event listener callback.

		Args:
			client (SocketModeClient): The active Slack client instance.
			req (SocketModeRequest): The incoming event request to process.
		"""
	
		# Responds to Slack
		response = SocketModeResponse(envelope_id=req.envelope_id)
		client.send_socket_mode_response(response)
	
		log("INCOMING PAYLOAD", req.payload)

	def reply_to_alert(ts: str, content: str) -> None:
		"""
		Sends a reply to a specific Slack thread timestamp (ts) in the appropriate channel.

		Args:
			ts (str): The thread timestamp to reply to.
			content (str): The message content to send.
		"""
		
		channel = config.BOT_TESTING_SLACK_CHANNEL_ID if config.TEST_RUN else config.SLACK_CHANNEL_ID
		
		log(f"REPLYING TO CHANNEL: {channel}")

		client = WebClient(token=config.SLACK_BOT_TOKEN)

		try:
			result = client.chat_postMessage(
				channel=channel,
				text=content,
				thread_ts=ts
			)
	
			if result["ok"]: 
				log("Reply sent successfuly")
			else:
				log(f"Issue replying to thread! {str(result)}", "error")
		
		except SlackApiError as e:
			log(f"Error: {e}")