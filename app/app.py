from app.reporter import Reporter

def main():
	reporter = Reporter()
	slackbot_client = reporter.get_slackbot_client()
	reporter.begin_slackbot_listen(slackbot_client)

if __name__ == "__main__":
	main()