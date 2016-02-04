"""
This utility cretae jira tickets from help form
"""
from jira.client import JIRA
import base64

def create_ticket(first, last, email, topics, subject, question):
    f=open('.access','r')
    A=f.readlines()
    f.close()
    my_string_u=A[0].strip()
    my_string_p=A[1].strip()
    """
    This function creates the ticket coming form the help form
    """

    jira = JIRA(
        server="https://opensource.ncsa.illinois.edu/jira/",
        basic_auth=(base64.b64decode(my_string_u).decode(), base64.b64decode(my_string_p).decode()))

    body = """
    *ACTION ITEMS*
    - Please ASSIGN this ticket if it is unassigned.
    - PLEASE SEND AN EMAIL TO  *%s* to reply to this ticket
    - COPY the answer in the comments section and ideally further communication. 
    - PLEASE close this ticket when resolved 
    
    
    *Name*: %s %s
    
    *Email*: %s
    
    *Topics*:
    %s
    
    *Question*:
    %s

    """ % (email, first, last, email, topics, question)

    issue = {
        'project' : {'key': 'DESRELEASE'},
        'issuetype': {'name': 'Task'},
        'summary': 'Q: %s' % subject,
        'description' : body,
        #'reporter' : {'name': 'desdm-wufoo'},
        }
    jira.create_issue(fields=issue)
