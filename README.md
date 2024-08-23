
# Bitbucket Bot for Google Chat

## Introduction

The Bitbucket Bot integrates Bitbucket's webhook events with Google Chat (Spaces). This bot listens for specific events from Bitbucket, such as pull requests (PRs), and sends notifications directly to a Google Chat (Spaces). The bot is designed to streamline your development workflow by providing real-time updates on key activities in your repositories.

## Example

When a pull request is opened, the bot sends a notification to your Google Chat space with details about the PR:

![Sample open PR](img/sample-pr.png)

## Quick start!

### Run container

```bash
docker run --name <container-name>    \
  -p 8080:8080                        \
  --bind 0.0.0.0:8080                 \
  --log-level=info                    \
  -e URL=<ENDPOINT-GOOGLE-CHAT-SPACE> \
  -e TOKEN=<SECRET-TOKEN>             \
  devopsiaci/bitbucket-bot:latest
```

### Bitbucket Payloads

Refer to the [Bitbucket payload documentation](https://confluence.atlassian.com/bitbucketserver0721/event-payload-1115665959.html?utm_campaign=in-app-help&utm_medium=in-app-help&utm_source=stash#Eventpayload-pullrequest) for details on the data structure of events.

## Request Payload

### Payload example

Here is an example of a pull request payload that the bot processes. Check [samples folder](./samples):

```json
{
    "eventKey": "pr:comment:added",
    "date": "2022-09-02T09:24:34+0000",
    "actor": {
        "name": "sample",
        "emailAddress": "mail@example.com",
        "id": 86045,
        "displayName": "sample",
        "active": true,
        "slug": "sample",
        "type": "NORMAL",
        "links": {
            "self": [
                {
                    "href": "https://bitbucket.org/bitbucket/users/sample"
                }
            ]
        }
    },
    ...
```

On `samples` folder:

```console
# request
$ curl -XPOST -H "Content-Type: application/json" -d '@sample_pr_add_comment.json' http://<IP>:<PORT>\?token\=<SECRET-TOKEN>

POST / HTTP/1.1
Host: <IP>:<PORT>
User-Agent: python-requests/2.32.3
Accept-Encoding: gzip, deflate
Accept: */*
Connection: keep-alive
Content-Type: application/json; charset=UTF-8
Content-Length: 958

{"cards": [{"header": {"title": "pr:comment:added | (GFP) REPOSITORY", "imageUrl": "https://cdn-icons-png.flaticon.com/512/6125/6125001.png"}, "sections": [{"widgets": [{"keyValue": {"icon": "PERSON", "topLabel": "author", "content": "mail@example.com"}}, {"keyValue": {"iconUrl": "https://cdn-icons-png.flaticon.com/512/7201/7201872.png", "topLabel": "Pull Request", "content": "test 3"}}, {"keyValue": {"iconUrl": "https://cdn-icons-png.flaticon.com/512/6577/6577243.png", "topLabel": "ID Pull Request", "content": "1 (version: 5)"}}, {"keyValue": {"iconUrl": "https://cdn-icons-png.flaticon.com/512/1721/1721936.png", "topLabel": "Status", "content": "OPEN"}}]}, {"widgets": [{"keyValue": {"icon": "DESCRIPTION", "topLabel": "Comment by sample", "content": "Test"}}]}, {"widgets": [{"buttons": [{"textButton": {"text": "Review PR", "onClick": {"openLink": {"url": "https://bitbucket.org/bitbucket/projects/KEY/repos/REPOSITORY/pull-requests/1"}}}}]}]}]}]}

```

## Tests

### Running Tests

The project uses `pytest` for testing. To run the tests, navigate to the project directory and execute the following command:

```bash
pytest
```

This will run all the tests located in the `tests/` directory. Make sure you have the necessary dependencies installed by running:

```bash
pip install -r requirements-dev.txt
```

### Writing Tests

To write new tests, create a new file in the `tests/` directory with the prefix `test_`. For example, to test a new feature in `app.py`, create a file named `test_app.py` and add your test cases there.

## Contributing

Please read the [CONTRIBUTING.md](CONTRIBUTING.md) file for details on our code of conduct and the process for submitting pull requests.
