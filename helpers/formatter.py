class Formatter:

    @staticmethod
    def sanitize_string(string):
        print("SANITIZING STRING...")
        return string.replace("“", "\"").replace("”", "\"")

    @staticmethod
    def extract_email_from_slack_payload(payload):
        print("EXTRACTING EMAIL...")
        for element in payload['event']['blocks'][0]['elements'][0]['elements']:
            # print("ELEMENT:", element)
            if element['type'] == "link":
                return element['text']

    @staticmethod 
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
                'click_type': 'idea',
                'ticket_type': 'Task'
            }

        if channel == 'serve-ai-issue':
            feedback_origin = payload['event']['attachments'][0]['blocks'][1]['text']['text']
            feedback_origin_array = feedback_origin.split('\n')
            name = feedback_origin_array[0].replace("*Submitted by:* ", '')
            email = feedback_origin_array[1].replace("*Email:* <mailto:", '')[:-2].split('|')[0]
            organization = feedback_origin_array[2].replace("*Organization:* ", '')
            user_id = feedback_origin_array[3].replace("*User ID:* ", '')
            timestamp = feedback_origin_array[4].replace("*Timestamp:* ", '')
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
                'click_type': 'issue',
                'ticket_type': 'Bug'
            }

        if channel == 'serve-ai-thumbs-up-down':
            try:
                feedback_pos_neg = payload['event']['blocks'][0]['text']['text']
                feedback_source = payload['event']['blocks'][1]['text']['text']
                feedback_name = feedback_source.split('*')[2][1:-1]
                feedback_email = feedback_source.split('\n')[1].split('*')[2].split('|')[1][:-1]
                feedback_organization = feedback_source.split('\n')[2].split('*')[2][1:]
                feedback_origin = feedback_source.split('\n')[4].split('*')[2][1:]
                feedback_timestamp = feedback_source.split('\n')[5].split('*')[2][1:]
                feedback_request = payload['event']['text'].split(feedback_name)[1][2:]
                feedback_message = payload['event']['blocks'][4]['text']['text'].split('```')[1][1:-1]

            except Exception as e:
                print("ERROR PARSING FEEDBACK PAYLOAD:", e.__str__())
                print("PAYLOAD:", payload)
                print("Message could not be parsed. Likely not a feedback message.")
                return
            
            payload_dict = {
                'name': feedback_name,
                'email': feedback_email,
                'organization': feedback_organization,
                'request': feedback_request,
                'feedback': feedback_message,
                'origin': feedback_origin,
                'issue_type': feedback_pos_neg,
                'timestamp': feedback_timestamp,
                'click_type': 'thumbsdown',
                'ticket_type': 'Bug' if 'thumbsdown' in feedback_pos_neg.lower() else None
            }


        elif channel == 'bot-testing':
            print(payload)
            return f"Message successfully received from bot-testing: {payload['event']['text']}"

        try:
            return payload_dict
        except NameError as e:
            print("ERROR: No payload_dict found!")
            return
	
    