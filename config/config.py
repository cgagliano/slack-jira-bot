import os
from dotenv import load_dotenv

load_dotenv()

TEST_RUN = False

# Loads all necessary environment variables
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")
SLACK_CHANNEL_ID = os.getenv("SLACK_CHANNEL_ID")
BOT_TESTING_SLACK_CHANNEL_ID = os.getenv("BOT_TESTING_SLACK_CHANNEL_ID")

assert SLACK_BOT_TOKEN, "SLACK_BOT_TOKEN is missing!"
assert SLACK_APP_TOKEN, "SLACK_APP_TOKEN is missing!"
assert SLACK_CHANNEL_ID, "SLACK_CHANNEL_ID is missing!"
assert BOT_TESTING_SLACK_CHANNEL_ID, "BOT_TESTING_SLACK_CHANNEL_ID is missing!"

JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")
JIRA_SERVE_PROJECT_KEY = os.getenv("JIRA_SERVE_PROJECT_KEY")

assert JIRA_EMAIL, "JIRA_EMAIL is missing!"
assert JIRA_API_TOKEN, "JIRA_API_TOKEN is missing!"
assert JIRA_BASE_URL, "JIRA_BASE_URL is missing!"
assert JIRA_SERVE_PROJECT_KEY, "JIRA_SERVE_PROJECT_KEY is missing!"

OPEN_AI_API_KEY = os.getenv("OPEN_AI_API_KEY")
assert OPEN_AI_API_KEY, "OPEN_AI_API_KEY is missing!"

LANGWATCH_API_KEY = os.getenv("LANGWATCH_API_KEY")
assert LANGWATCH_API_KEY, "LANGWATCH_API_KEY is missing!"

QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_CLUSTER_URL = os.getenv("QDRANT_CLUSTER_URL")
assert QDRANT_API_KEY, "QDRANT_API_KEY is missing!"
assert QDRANT_CLUSTER_URL, "QDRANT_CLUSTER_URL is missing!"

QDRANT_COLLECTION_NAME = "llm_analysis_seeds"

TRACE_DICT_FILEPATH = './trace_dict.p'
LLM_ANALYSIS_RECORDS_FILEPPATH = "./llm_analysis_records.txt"
QDRANT_ANALYSIS_RECORDS_FILEPPATH = "./qdrant_analysis_records.txt"

BOT_ID_DICT = {
    "B085MFUKA23" : "LANGWATCH_MONITORING_BOT_ID",
    "B0A27RDM345" : "SERVE_AI_THUMBS_UP_DOWN_BOT_ID",
    "B08E3T07534" : "REPLY_BOT_ID",
    "B098ZBZR00P" : "SERVE_AI_ISSUE_BOT_ID",
    "B099D2QLWRJ" : "SERVE_AI_IDEA_BOT_ID",
    "B098H7BR800" : "SERVE_AI_SUPPORT_BOT_ID"
}

CHANNEL_ID_DICT = {
    'C08LSADUE58': 'bot-testing',
    'C0997D35KA7': 'serve-ai-idea',
    'C098ZBUGS07': 'serve-ai-issue',
    'C0A2Q6D3B4H': 'serve-ai-thumbs-up-down'
	}

JIRA_ASSIGNEE_ID_DICT = {
    'Project Manager' : '712020:0030d7be-dc83-4379-9c1b-bdd118f87465',
    'QA Team' : '712020:9ca42d1e-a23e-4afd-b55b-35f2b4ab3aab'
}


PRIMARY_LLM_MODEL = "gpt-4.1"
SECONDARY_LLM_MODEL = "gpt-4o"

JIRA_ISSUE_URL_TEMPLATE = "https://get-genetica.atlassian.net/browse/{issue}"
PIKE_SPRINT_ID = "31"
BUG_TRIAGE_SPRINT_ID = "103"
BUG_INTAKE_SPRINT_ID = "102"

API_RETRIES = 3
