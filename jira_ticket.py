"""
This utility cretae jira tickets from help form
"""
from jira.client import JIRA
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import formataddr
import smtplib
import urllib

def send_email():
    subject="New Ticket in DESRELEASE"
    toemail = 'mcarras2@illinois.edu'
    fromemail = 'devnull@ncsa.illinois.edu'
    s = smtplib.SMTP('smtp.ncsa.illinois.edu')
    text = "https://opensource.ncsa.illinois.edu/jira/projects/DESRELEASE"
    MP1 = MIMEText(text, 'plain')
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = formataddr((str(Header('DESRELEASE JIRA', 'utf-8')), fromemail))
    msg['To'] = toemail
    msg.attach(MP1)
    s.sendmail(fromemail, toemail, msg.as_string())
    s.quit()

def send_email_desdm():
    subject="New Ticket in DESHELP"
    toemail = 'mcarras2@illinois.edu'
    fromemail = 'devnull@ncsa.illinois.edu'
    s = smtplib.SMTP('smtp.ncsa.illinois.edu')
    text = "https://opensource.ncsa.illinois.edu/jira/projects/DESHELP"
    MP1 = MIMEText(text, 'plain')
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = formataddr((str(Header('DESHELP JIRA', 'utf-8')), fromemail))
    msg['To'] = toemail
    msg.attach(MP1)
    s.sendmail(fromemail, toemail, msg.as_string())
    s.quit()

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
    send_email()

def create_ticket_desdm(first, last, email, username, topics, question):
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
    PLEASE SEND AN EMAIL TO %s when
    ticket is resolved and CONFIRM that it was done 
    in the comments section of the ticket
    ------------------------------
    
    *Name*: %s %s
    
    *Email*: %s

    *Username* (if entered) : %s
    
    *Quick help checkboxes*:
    %s
    
    *Extra information*:
    %s

    """ % (email, first, last, email, username, topics, question)

    issue = {
        'project' : {'key': 'DESHELP'},
        'issuetype': {'name': 'Task'},
        'summary': 'Help with DESDM account',
        'description' : body,
        'reporter' : {'name': 'desdm-wufoo'},
        }
    jira.create_issue(fields=issue)
    send_email_desdm()
