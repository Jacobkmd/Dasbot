import config
import htmlparser

import datetime
import smtplib
from email.mime.text import MIMEText
from atlassian import Confluence, Jira


class Dispatcher:
    
    def __init__(self, team, dispatcher):
        self.team = team    
        self.dispatcher = dispatcher

    def __str__(self):
        return f'{self.team} {self.dispatcher}'


def send_email(to, subject, body, sender=None):

    if sender is None:
        sender_email = config.mail_username
    else:
        sender_email = sender
        
    msg = MIMEText(body)
    msg["From"] = sender_email
    msg["To"] = to
    msg["Subject"] = subject 

    with smtplib.SMTP_SSL(host=config.mail_host, port=config.mail_port) as server:
        server.login(user=config.mail_username, password=config.mail_password)
        server.sendmail(sender_email, to, msg.as_string())
        server.quit()


confluence = Confluence(
    url=config.confluence_url,
    username=config.confluence_username,
    password=config.confluence_password)


jira = Jira( 
    url=config.jira_url,
    username=config.jira_username,
    password=config.jira_password)


def update_confluence_calender_page(confluence_id, unit):

    if unit == "w":
        unit = datetime.date.today().isocalendar()[1]
    else:
        unit = datetime.datetime.today().day

    confluence_content = confluence.get_page_by_id(confluence_id, expand="body.storage") 
 
    html = confluence_content["body"]["storage"]["value"]
    title = confluence_content["title"]

    column = htmlparser.find_column_number(html, str(unit))
    row = htmlparser.find_row_number(html, column, "B")
    dispatcher = htmlparser.get_cell_value(html, 0, row)

    print("Dagens bamse er den " + str(datetime.datetime.today()) + " er " + dispatchers)

    html = htmlparser.remove_highlightclass(html)
    html = htmlparser.add_highlightclass(html, column)

    confluence.update_page(confluence_id, title, html)

    return dispatcher


def update_confluence_summary_page(confluence_id, dispatchers):
    html = ('<p>Sist oppdatert ' +  str(datetime.datetime.today()) + '</p>'
            '<table class="wrapped"><tbody><tr><th>Team</th><th>Bamse</th></tr>')
    
    for dispatcher in dispatchers:
        html += '<tr><td>' + dispatcher.team + '</td><td>' + dispatcher.dispatcher + '</td></tr>'
    
    html += '</tbody></table>'

    title = confluence.get_page_by_id(confluence_id)["title"]
 
    confluence.update_page(confluence_id, title, html)