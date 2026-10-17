"""
Bitbucket Bot to integrate Bitbucket's webhook with Google Chat (Spaces)
"""

import html
import json
import os
import requests

from flask import Flask, request


app = Flask(__name__)

class Message():
    '''
    Initialize message object to prepare template for GChat bot

    '''
    def __init__(self, url, event):
        self.author        = event['pullRequest']['author']['user']['emailAddress']
        self.pr_event_key  = event['eventKey']
        self.pr_id         = event['pullRequest']['id']
        self.pr_version    = event['pullRequest']['version']
        self.pr_title      = event['pullRequest']['title']
        self.pr_state      = event['pullRequest']['state']
        self.pr_link       = event['pullRequest']['links']['self'][0]['href']
        self.pr_repository = event['pullRequest']['fromRef']['repository']['name']
        self.pr_project    = event['pullRequest']['fromRef']['repository']['project']['key']
        self.url           = url


    @staticmethod
    def detail(icon, label, text):
        '''
        Section with one decoratedText widget (icon is a knownIcon)

        '''
        return {"widgets": [{"decoratedText": {"startIcon": {"knownIcon": icon}, "topLabel": label, "text": text}}]}


    def pr_approved(self, event):
        '''
        Add approved comment with properly template

        '''
        return self.detail("STAR", f"Review by {event['participant']['user']['name']}",
                           str(event['participant']['status']))


    def pr_modified(self, event):
        '''
        Add modified function with properly template

        '''
        return self.detail("DESCRIPTION", f"Modified by {event['actor']['name']}",
                           f"<b>Previous title</b>: {event['previousTitle']}<br>"
                           f"<b>Previous description</b>: {event['previousDescription']}")


    def pr_comment_add(self, event):
        '''
        Add comment function with properly template

        '''
        return self.detail("DESCRIPTION", f"Comment by {event['comment']['author']['name']}",
                           str(event['comment']['text']))


    def prepare_template(self, message):
        '''
        Prepare final template before send

        '''
        def meta(icon, label, text):
            return {"decoratedText": {"startIcon": icon, "topLabel": label, "text": str(text)}}

        card = {
            "header": {
                "title": f"{self.pr_event_key} | ({self.pr_project}) {self.pr_repository}",
                "imageUrl": "https://cdn-icons-png.flaticon.com/512/6125/6125001.png"
            },
            "sections": [
                {
                    "widgets": [
                        meta({"knownIcon": "PERSON"}, "author", self.author),
                        meta({"iconUrl": "https://cdn-icons-png.flaticon.com/512/7201/7201872.png"},
                             "Pull Request", self.pr_title),
                        meta({"iconUrl": "https://cdn-icons-png.flaticon.com/512/6577/6577243.png"},
                             "ID Pull Request", f"{self.pr_id} (version: {self.pr_version})"),
                        meta({"iconUrl": "https://cdn-icons-png.flaticon.com/512/1721/1721936.png"},
                             "Status", self.pr_state)
                    ]
                },
                {
                    "widgets": [
                        {
                            "buttonList": {
                                "buttons": [
                                    {
                                        "text": "Review PR",
                                        "onClick": {"openLink": {"url": str(self.pr_link)}}
                                    }
                                ]
                            }
                        }
                    ]
                }
            ]
        }

        if message:
            card["sections"].insert(1, message)

        return {"cardsV2": [{"cardId": f"pr-{self.pr_id}", "card": card}]}


    def send_message(self, message=None):
        '''
        Prepare message and send to bot

        '''
        # pylint fix W0102 (dangerous-default-value)
        if message is None:
            message = {}

        # prepare final message
        bot_message = self.prepare_template(message)

        # send request
        headers = {'Content-Type': 'application/json; charset=UTF-8'}
        response = requests.post(
            url=self.url,
            headers=headers,
            data=json.dumps(bot_message),
            timeout=10
        )

        return response.text


@app.route("/", methods=["POST"])
def main():
    '''
    Main function to deploy

    '''
    url = os.environ.get('URL', 'http://example.com')
    token = os.environ.get('TOKEN')
    r = {}

    if request.args['token'] != token:
        return "Invalid token", 403

    event = request.get_json()

    if not event:
        return "event empty", 400

    message = Message(url, event)
    if (event['eventKey'] == 'pr:opened' or event['eventKey'] == 'pr:merged' or event['eventKey'] == 'pr:declined'):
        r = message.send_message()
    elif event['eventKey'] == 'pr:modified':
        r = comment = message.pr_modified(event)
        message.send_message(comment)
    elif event['eventKey'] == 'pr:comment:added':
        comment = message.pr_comment_add(event)
        r = message.send_message(comment)
    elif (event['eventKey'] == 'pr:reviewer:needs_work' or event['eventKey'] == 'pr:reviewer:approved'):
        comment = message.pr_approved(event)
        r = message.send_message(comment)

    return html.escape(json.dumps(r))


if __name__ == "__main__":
    app.run()
