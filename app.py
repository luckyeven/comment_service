# comment_service.py

from flask import Flask, jsonify
import requests

app = Flask(__name__)


@app.route('/')
def index():
    return 'comment server up and running'

@app.route('/comment/<id>')
def comment(id):
    comments = {
        '1': {'user_id': '1', 'post_id' : '2', 'comment' : 'Amazing post!'},
        '2': {'user_id': '2', 'post_id' : '2', 'comment' : 'I did not know that'}
    }
    comment_info = comments.get(id, {})
    
    # Get user info from User Service
    if comment_info:


        userResponse = requests.get(f'https://userservice.ashyrock-0da57b89.canadacentral.azurecontainerapps.io/user/{comment_info["user_id"]}')
        postResponse = requests.get(f'https://postservice.ashyrock-0da57b89.canadacentral.azurecontainerapps.io/post/{comment_info["post_id"]}')
        if userResponse.status_code and postResponse.status_code == 200:
            comment_info['user'] = userResponse.json()
            comment_info['post'] = postResponse.json()['post']

    return jsonify(comment_info)

if __name__ == '__main__':
    app.run()