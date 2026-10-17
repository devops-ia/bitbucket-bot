import json
import os

import pytest

ICON_PEOPLE = "https://cdn-icons-png.flaticon.com/512/6125/6125001.png"
ICON_URLS = [
    "https://cdn-icons-png.flaticon.com/512/7201/7201872.png",
    "https://cdn-icons-png.flaticon.com/512/6577/6577243.png",
    "https://cdn-icons-png.flaticon.com/512/1721/1721936.png",
]


def send(client, token, post, sample):
    """Post a sample event and return (response, JSON sent to Google Chat)."""
    path = os.path.join(os.path.dirname(__file__), '../samples', sample)
    with open(path, 'r', encoding='utf-8') as f:
        event = json.load(f)
    response = client.post('/', query_string={'token': token}, json=event)
    sent = json.loads(post.call_args.kwargs['data']) if post.called else None
    return response, event, sent


def check_base(event, sent):
    """Assert the parts common to every event; return the card."""
    assert 'cards' not in sent
    assert sent['cardsV2'][0]['cardId'] == f"pr-{event['pullRequest']['id']}"
    card = sent['cardsV2'][0]['card']
    repo = event['pullRequest']['fromRef']['repository']
    assert card['header'] == {
        "title": f"{event['eventKey']} | ({repo['project']['key']}) {repo['name']}",
        "imageUrl": ICON_PEOPLE,
    }
    meta = [w['decoratedText'] for w in card['sections'][0]['widgets']]
    assert [m['topLabel'] for m in meta] == ['author', 'Pull Request', 'ID Pull Request', 'Status']
    assert meta[0]['startIcon'] == {'knownIcon': 'PERSON'}
    assert [m['startIcon']['iconUrl'] for m in meta[1:]] == ICON_URLS
    button = card['sections'][-1]['widgets'][0]['buttonList']['buttons'][0]
    assert button['text'] == 'Review PR'
    assert button['onClick']['openLink']['url'] == event['pullRequest']['links']['self'][0]['href']
    assert 'keyValue' not in json.dumps(sent) and 'textButton' not in json.dumps(sent)
    return card


def test_invalid_token(client, post):
    response = client.post('/', query_string={'token': 'wrong-token'}, json={})
    assert response.status_code == 403
    assert b'Invalid token' in response.data
    post.assert_not_called()


def test_empty_event(client, valid_token, post):
    response = client.post('/', query_string={'token': valid_token}, json={})
    assert response.status_code == 400
    assert b'event empty' in response.data
    post.assert_not_called()


@pytest.mark.parametrize('sample', ['sample_pr_opened.json', 'sample_pr_merged.json', 'sample_pr_declined.json'])
def test_pr_without_detail(client, valid_token, post, sample):
    response, event, sent = send(client, valid_token, post, sample)
    assert response.status_code == 200
    assert len(check_base(event, sent)['sections']) == 2


@pytest.mark.parametrize('sample', ['sample_pr_approved.json', 'sample_pr_needs_work.json'])
def test_pr_review(client, valid_token, post, sample):
    response, event, sent = send(client, valid_token, post, sample)
    assert response.status_code == 200
    section = check_base(event, sent)['sections']
    assert len(section) == 3
    text = section[1]['widgets'][0]['decoratedText']
    assert text['topLabel'] == f"Review by {event['participant']['user']['name']}"
    assert text['text'] == event['participant']['status']
    assert text['startIcon'] == {'knownIcon': 'STAR'}


def test_pr_comment_added(client, valid_token, post):
    response, event, sent = send(client, valid_token, post, 'sample_pr_add_comment.json')
    assert response.status_code == 200
    section = check_base(event, sent)['sections']
    assert len(section) == 3
    text = section[1]['widgets'][0]['decoratedText']
    assert text['topLabel'] == f"Comment by {event['comment']['author']['name']}"
    assert text['text'] == event['comment']['text']
    assert text['startIcon'] == {'knownIcon': 'DESCRIPTION'}


def test_pr_modified(client, valid_token, post):
    response, event, sent = send(client, valid_token, post, 'sample_pr_modified.json')
    assert response.status_code == 200
    section = check_base(event, sent)['sections']
    assert len(section) == 3
    text = section[1]['widgets'][0]['decoratedText']
    assert text['topLabel'] == f"Modified by {event['actor']['name']}"
    assert text['text'] == (f"<b>Previous title</b>: {event['previousTitle']}<br>"
                            f"<b>Previous description</b>: {event['previousDescription']}")
    assert '\n' not in text['text']
