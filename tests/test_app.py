
import json
import os

def test_invalid_token(client):
    response = client.post('/', query_string={'token': 'wrong-token'}, json={})
    assert response.status_code == 403
    assert b'Invalid token' in response.data

def test_empty_event(client, valid_token):
    response = client.post('/', query_string={'token': valid_token}, json={})
    assert response.status_code == 400
    assert b'event empty' in response.data

def test_pr_opened(client, valid_token):
    json_path = os.path.join(os.path.dirname(__file__), '../samples/sample_pr_opened.json')
    with open(json_path, 'r') as f:
        event = json.load(f)

    response = client.post('/', query_string={'token': valid_token}, json=event, content_type='application/json')
    assert response.status_code == 200

def test_pr_modified(client, valid_token):
    json_path = os.path.join(os.path.dirname(__file__), '../samples/sample_pr_modified.json')
    with open(json_path, 'r') as f:
        event = json.load(f)

    response = client.post('/', query_string={'token': valid_token}, json=event, content_type='application/json')
    assert response.status_code == 200

def test_pr_comment_added(client, valid_token):
    json_path = os.path.join(os.path.dirname(__file__), '../samples/sample_pr_add_comment.json')
    with open(json_path, 'r') as f:
        event = json.load(f)

    response = client.post('/', query_string={'token': valid_token}, json=event, content_type='application/json')
    assert response.status_code == 200

def test_pr_approved(client, valid_token):
    json_path = os.path.join(os.path.dirname(__file__), '../samples/sample_pr_approved.json')
    with open(json_path, 'r') as f:
        event = json.load(f)

    response = client.post('/', query_string={'token': valid_token}, json=event, content_type='application/json')
    assert response.status_code == 200

def test_pr_declined(client, valid_token):
    json_path = os.path.join(os.path.dirname(__file__), '../samples/sample_pr_approved.json')
    with open(json_path, 'r') as f:
        event = json.load(f)

    response = client.post('/', query_string={'token': valid_token}, json=event, content_type='application/json')
    assert response.status_code == 200

def test_pr_needs_work(client, valid_token):
    json_path = os.path.join(os.path.dirname(__file__), '../samples/sample_pr_needs_work.json')
    with open(json_path, 'r') as f:
        event = json.load(f)

    response = client.post('/', query_string={'token': valid_token}, json=event, content_type='application/json')
    assert response.status_code == 200

def test_pr_merged(client, valid_token):
    json_path = os.path.join(os.path.dirname(__file__), '../samples/sample_pr_merged.json')
    with open(json_path, 'r') as f:
        event = json.load(f)

    response = client.post('/', query_string={'token': valid_token}, json=event, content_type='application/json')
    assert response.status_code == 200
