from config import config

class JiraTicket:
    def __init__(self):
        pass
    
    @staticmethod
    def format_ser_jira_ticket(**details):
        url = f"{config.JIRA_BASE_URL}/rest/api/3/issue"
                
        if details['click_type'] == 'thumbsdown':
            body = f"""From: {details['name']} - {details['email']}
            Organization: {details['organization']}
            User Request: {details['request']}
            User Feedback: {details['feedback']}
            Feedback Origin: {details['origin']}
            Submitted at: {details['timestamp']}
            """
        elif details['click_type'] == 'issue':
            body = f"""From: {details['name']} - {details['email']}
            Organization: {details['organization']}
            Issue Type: {details['issue_type']}
            Issue Urgency: {details['issue_urgency']}
            Issue Description: {details['issue_description']}
            Issue ID: {details['issue_id']}
            Submitted at: {details['timestamp']}
            """
        elif details['click_type'] == 'idea':
            body = f"""From: {details['name']} - {details['email']}
            Organization: {details['organization']}
            Idea Description: {details['text']}
            Submitted at: {details['timestamp']}
            """
        
        # TEST DATA
        # body = "TEST BODY"
    
        # Payload to be sent to Jira.
        payload = {
            "fields": {
                "project": {"key": "SER"},
                "issuetype": {"name": details['ticket_type']},
                "summary": f"Auto Generated {details['click_type']} Ticket from {details['organization']}",
                "description": {
                                "type": "doc",
                                "version": 1,
                                "content": [
                                    {
                                    "type": "paragraph",
                                    "content": [
                                        {
                                        "type": "text",
                                        "text": body
                                    }
                                    ]
                                    }
                                ]
                            },
            }
        }
        
        # # TEST DATA
        # payload = {
		# 	"fields": {
		# 		"project": {"key": "SER"},
		# 		"issuetype": {"name": "Bug"},
		# 		"summary": "TEST TEST TEST SUMMARY SUMMARY SUMMARY",
		# 		"description": {
		# 						"type": "doc",
		# 						"version": 1,
		# 						"content": [
		# 							{
		# 							"type": "paragraph",
		# 							"content": [
		# 								{
		# 								"type": "text",
		# 								"text": "TEST TEXT TEST TEXT TEST TEXT ",
		# 								"marks": [
		# 									{
		# 									"type": "link",
		# 									"attrs": {"href": "www.serveitup.ai"}
		# 									}
		# 									]
		# 								},
		# 								{
		# 								"type": "text",
		# 								"text": "TEST DESCRIPTION TEST DESCRIPTION TEST DESCRIPTION "
		# 							}
		# 							]
		# 							}
		# 						]
		# 					},
		# 	}
		# }
        
        return payload, url
    
# Payload to be sent to Jira.
# payload = {
# 			"fields": {
# 				"project": {"key": "SER"},
# 				"issuetype": {"name": "Bug"},
# 				"summary": "TEST TEST TEST SUMMARY SUMMARY SUMMARY",
# 				"description": {
# 								"type": "doc",
# 								"version": 1,
# 								"content": [
# 									{
# 									"type": "paragraph",
# 									"content": [
# 										{
# 										"type": "text",
# 										"text": "TEST TEXT TEST TEXT TEST TEXT ",
# 										"marks": [
# 											{
# 											"type": "link",
# 											"attrs": {"href": "www.serveitup.ai"}
# 											}
# 											]
# 										},
# 										{
# 										"type": "text",
# 										"text": "TEST DESCRIPTION TEST DESCRIPTION TEST DESCRIPTION "
# 									}
# 									]
# 									}
# 								]
# 							},
# 			}
# 		}