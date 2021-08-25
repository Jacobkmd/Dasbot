import dasbot
#from atlassian import Confluence, Jira

from flask import Flask, request, abort
import logging
logging.basicConfig(filename='webhook.log')


app = Flask(__name__)

@app.route('/')
def index():
    return "Hello world!"


@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        
        json = request.get_json()
        logging.info(json)

        jirakey = json['issue']['key']
        print(jirakey)

        if json['issue']['fields']['status']['id'] == '3':
            print("Vi endrer status på " + jirakey)
            dasbot.jira.set_issue_status_by_transition_id(jirakey, '31')
       
        return 'success', 200
    else:
        logging.error('Webhook uten "POST"')
        

if __name__ == '__main__':
    
    app.run(debug=True, port=5000, host='127.0.0.1')