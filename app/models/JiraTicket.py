from config import config

class JiraTicket:
    def __init__(self):
        pass
    
    @staticmethod
    def format_ser_jira_ticket(issue_type, request, feedback, name, email, origin, organization, timestamp):
        url = f"{config.JIRA_BASE_URL}/rest/api/3/issue"
                
        # log(f"Jira ticket summary: {summary}")
        
        body = f"""From: {name} - {email}
        Organization: {organization}
        User Request: {request}
        User Feedback: {feedback}
        Feedback Origin: {origin}
        Submitted at: {timestamp}
        """
        
        # TEST DATA
        # body = "TEST BODY"
    
        # Payload to be sent to Jira.
        payload = {
            "fields": {
                "project": {"key": "SER"},
                "issuetype": {"name": issue_type},
                "summary": "AI Generated Ticket from " + organization,
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