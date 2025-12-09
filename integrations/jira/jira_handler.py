from typing import Optional, Dict, Any
# from app.models.JiraTicket import JiraTicket
from logger import log
import requests
from config import config
import json
import re

class Jira_Handler:
    
    def __init__(self) -> None:
        """
        Initializes the Jira handler with authentication and configuration values
        loaded from environment variables.
        """
        self.jira_domain = config.JIRA_BASE_URL
        self.jira_email = config.JIRA_EMAIL
        self.jira_api_token = config.JIRA_API_TOKEN
        self.project_key = config.JIRA_PROJECT_KEY 
        self.auth = (self.jira_email, self.jira_api_token)
        
    def post_jira_ticket(
        self,
        payload: Dict[str, Any],
        url: str,
        headers: Dict[str, str] = {"Content-Type": "application/json"}
    ) -> Optional[str]:
        """
        Attempts to create a Jira issue using the provided payload and URL.
        Retries the request if it fails.

        Args:
            payload (Dict[str, Any]): The issue data to be sent to Jira.
            url (str): The API endpoint for issue creation.
            headers (Dict[str, str], optional): HTTP headers for the request.

        Returns:
            Optional[str]: The key of the created issue if successful, otherwise None.
        """
        
        issue_key = None
        for retries in range(config.API_RETRIES):
            try:
                response = requests.post(url, json=payload, headers=headers, auth=self.auth)

                if response.status_code == 201:
                    issue_key = response.json().get("key")
                    print(f"Jira issue created: {issue_key}")
                    break
                else:
                    print(f"Jira issue creation failed: {response.text}")

            except requests.exceptions.RequestException as e:
                    print(f"Jira API error while creating issue: {e}", "error")
        
        return issue_key

    def add_jira_issue_to_sprint(self, sprint_id: int, issue_key: str) -> None:
        """
        Adds a Jira issue to a specific sprint using the Agile API.

        Args:
            sprint_id (int): The ID of the sprint.
            issue_key (str): The Jira issue key (e.g., "BUG-123").
        """
        sprint_url = f"{config.JIRA_BASE_URL}/rest/agile/1.0/sprint/{sprint_id}/issue"
        sprint_payload = {"issues": [issue_key]}
        sprint_response = requests.post(sprint_url, json=sprint_payload, auth=self.auth)
        
        if sprint_response.status_code == 204:
            log(f"Added issue {issue_key} to Sprint {sprint_id}")
        else:
            log(f"Failed to add issue to Sprint: {sprint_response.text}")

    def post_jira_comment(
        self,
        payload: Dict[str, Any],
        url: str,
        headers: Dict[str, str] = {"Content-Type": "application/json"}
    ) -> bool:
        """
        Posts a comment to a Jira issue.

        Args:
            payload (Dict[str, Any]): The comment body in JSON format.
            url (str): The Jira comment API endpoint.
            headers (Dict[str, str], optional): HTTP headers for the request.

        Returns:
            bool: True if successful, False otherwise.
        """
        
        # print("URL:", url)
        # print("PAYLOAD:", payload)

        response = requests.post(url, headers=headers, auth=self.auth, data=json.dumps(payload))

        if response.status_code == 201:
            log("Jira comment added successfully!")
            return True
        else:
            log(f"Failed to add Jira comment: {response.status_code} - {response.text}")
            return False

    def get_sprint_issues(self, sprint_id: int) -> list:
        """
        Fetches all issues for a given sprint using pagination.

        Args:
            sprint_id (int): The sprint ID to query.

        Returns:
            list: A list of issue objects returned by Jira.
        """
        url = f"{config.JIRA_BASE_URL}/rest/agile/1.0/sprint/{sprint_id}/issue"
        response = requests.get(url, auth=(config.JIRA_EMAIL, config.JIRA_API_TOKEN))
        
        return response.json()["issues"]


    def extract_json_from_automatic_jira_comment(self, jira_comment_string: str) -> Optional[dict]:
        """
        Attempts to extract a JSON object from a Jira comment string.

        Args:
            jira_comment_string (str): The raw comment string.

        Returns:
            Optional[dict]: The extracted JSON dictionary if found, otherwise None.
        """
        log("Searching for JSON in comment...")
        curr_char = jira_comment_string[0]
        while curr_char != '{':
            try:
                jira_comment_string = jira_comment_string[1:]
                curr_char = jira_comment_string[0]
            except IndexError:
                log("No JSON found")
                return None
        
        jira_comment_string = jira_comment_string.replace('\n', '').replace('\t', '')
        try:
            parsed = json.loads(jira_comment_string)
        #	log(parsed["trace_id"])  # Or anything else you want to access
        except json.JSONDecodeError as e:
            # print("JSON parsing failed:", e)
            return None
        
        return(parsed)
    
    def search_jira_backlog(self, search_term: str) -> Optional[str]:
        """
        Searches Jira backlog issues by a trace ID or keyword in the summary.

        Args:
            search_term (str): The term to search for in issue summaries.

        Returns:
            Optional[str]: The issue key of the first match, or None.
        """

        jql = f'project = {self.project_key} AND status in ("To Do", "Backlog", "In Progress", "Needs Validation", "Needs Review", "Waiting for Deploy", "Won\'t do", "Blocked", "Done", "Waiting on further details") AND summary ~ "{search_term}"'

        url = f"{self.jira_domain}/rest/api/2/search"
        params = {
            "jql": jql,
            "maxResults": 10,
            "fields": "summary,status"
        }

        response = requests.get(
            url,
            params=params,
            auth=self.auth,
            headers={"Accept": "application/json"}
        )

        log(f"Searching for Jira ticket for trace {search_term}")
        
        try:
            if response.status_code == 200:
                issues = response.json().get("issues", [])
                return issues[0]["key"]
            else:
                log("Error searching for matches:", response.status_code, response.text)
                return None
            
        except IndexError:
            log(f"No Jira matches found for {search_term}")
            return None
        
        except KeyError:
            log(f"No Jira matches found for {search_term}")
            return None
        
    def get_sprint_issues(self, sprint_id):
        issues = []
        start = 0
        max_results = 100
        while True:
            url = f"{config.JIRA_BASE_URL}/rest/agile/1.0/sprint/{sprint_id}/issue"
            params = {"startAt": start, "maxResults": max_results}
            response = requests.get(url, auth=(config.JIRA_EMAIL, config.JIRA_API_TOKEN), params=params)
        
            if response.status_code != 200:
                log.error(f"Failed to get issues for sprint {sprint_id}: {response.text}")
                break
        
            page = response.json()
            issues.extend(page.get("issues", []))
        
            if start + max_results >= page.get("total", 0):
                break
        
            start += max_results
        
        return issues


    def extract_json_from_automatic_jira_comment(self, jira_comment_string):
        jira_comment_string = jira_comment_string.replace("pertnent", "pertinent").replace('\n', '').replace('\t', '').replace('\\{', '{')
        curr_char = jira_comment_string[0]
        while curr_char != '{':
            try:
                jira_comment_string = jira_comment_string[1:]
                curr_char = jira_comment_string[0]
            except IndexError:
                # print("No JSON found")
                return None
        
        curr_char = jira_comment_string[-1]
        while curr_char != '}':
            try:
                jira_comment_string = jira_comment_string[:-1]
                curr_char = jira_comment_string[-1]
            except IndexError:
                # print("No JSON found")
                return None
        
        
        try:
            parsed = json.loads(jira_comment_string)
        except json.JSONDecodeError as e:
            # log("No JSON Found:", e)
            return None
        
        return(parsed)

    def comment_hunter(self, sprint_id: int) -> Dict[str, list]:
        """
        Collects comments from all issues in a sprint and classifies them by whether
        JSON was found in the comments.

        Args:
            sprint_id (int): The sprint ID to scan.

        Returns:
            Dict[str, list]: A dictionary with keys "json_found", "no_json_found", and "no_comment_found".
        """
        jira_issues = self.get_sprint_issues(sprint_id)

        issue_types = {
            "json_found": [],
            "no_json_found": [],
            "no_comment_found": []
        }

        for issue in jira_issues:
            issue_obj = {
                'key': issue["key"], 
                'trace': re.search("trace_.{12}", issue["fields"]["summary"])[0], 
                "description": issue["fields"]["description"], 
                'comments': [], 
                'json_obj': None }
            
            if issue["fields"]["comment"]['comments']:
                for comment in issue["fields"]["comment"]['comments']:
                    issue_obj['comments'].append(comment)
                    if self.extract_json_from_automatic_jira_comment(str(comment['body'])):
                        issue_obj['json_obj'] = self.extract_json_from_automatic_jira_comment(str(comment['body']))
                        issue_types["json_found"].append(issue_obj)
                    else:
                        issue_types["no_json_found"].append(issue_obj)
            else:
                issue_types["no_comment_found"].append(issue_obj)
                
        return issue_types
        
    def output_comment_hunter(self, issues_objects: dict) -> None:
        """
        Placeholder for a function that would process or output the structured result
        from `comment_hunter`.

        Args:
            issues_objects (dict): The result from comment_hunter, containing comment metadata.
        """
        pass
   
    def delete_jira_comment(self, issue_key: str, comment_id: str) -> bool:
        """
        Deletes a comment from a specific Jira issue.

        Args:
            issue_key (str): The key of the issue (e.g., "FLORA-1234").
            comment_id (str): The ID of the comment to delete.

        Returns:
            bool: True if deletion was successful, False otherwise.
        """
        url = f"{self.jira_domain}/rest/api/3/issue/{issue_key}/comment/{comment_id}"
        response = requests.delete(url=url, auth=self.auth)
        
        if response.status_code == 204:
            log("Comment deleted successfully.")
            return True
        else:
            log(f"Failed to delete comment: {response.status_code} - {response.text}")
            return False
   
    def update_ticket_status(self, issue_key: str, status_name: str) -> None:
        """
            Updates the status of a specific Jira issue.
            
            Args:
            issue_key (str): The key of the issue (e.g., "FLORA-1234").
            status_name (str): The legible name of the status we're changing the issue into.

            To-Do:
                Check response for error handling and return purposes
        """
        status_dict = {
            "Needs Review": "2",
            "Waiting for Deploy": "3",
            "Won't Do": "4",
            "Blocked": "5",
            "Needs Validation": "6",
            "To Do": "11",
            "In Progress": "21",
            "Done": "31",
            "Waiting on further details": "32"
        }
        
        payload = {
            "transition": {
                "id": status_dict[status_name]
            }
        }

        response = requests.post(f"{self.jira_domain}/rest/api/3/issue/{issue_key}/transitions", headers={"Content-Type": "application/json"}, auth=self.auth, data=json.dumps(payload))
        
        def get_jira_boards():
            url = f"{config.JIRA_BASE_URL}/rest/agile/1.0/board"
            response = requests.get(url, auth=self.auth)
            if response.status_code == 200:
                boards = response.json().get("values", [])
                return boards
            else:
                print(f"Failed to get boards: {response.text}")
                return []