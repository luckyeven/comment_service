# comment_service.py

from flask import Flask, jsonify
import requests
comments_count = 2
comments = {
    '1': {'user_id': '1', 'post_id' : '2', 'comment' : 'Amazing post!'},
    '2': {'user_id': '2', 'post_id' : '2', 'comment' : 'I did not know that'}
}

app = Flask(__name__)

@app.route('/')
def index():
    return 'comment server up and running'

@app.route('/comment/<id>')
def comment(id):
    comment_info = comments.get(id, {})
    
    # Get user info from User Service
    if comment_info:


        userResponse = requests.get(f'https://userservice.ashyrock-0da57b89.canadacentral.azurecontainerapps.io/user/{comment_info["user_id"]}')
        postResponse = requests.get(f'https://postservice.ashyrock-0da57b89.canadacentral.azurecontainerapps.io/post/{comment_info["post_id"]}')
        if userResponse.status_code and postResponse.status_code == 200:
            comment_info['user'] = userResponse.json()
            comment_info['post'] = postResponse.json()['post']

    return jsonify(comment_info)

@app.route('/create/<user_id>/<post_id>/<comment>')
def create(user_id,post_id,comment):
    global comments_count
    comment = {
        'user_id': user_id,
        'post_id': post_id,
        'comment': comment
    }
    comments_count += 1
    comments[str(comments_count)] = comment
    return jsonify(comment)

@app.route('/delete/<id>')
def delete(id):
    if comments.get(id):
        del comments[id]
        return 'Comment deleted'
    else:
        return 'Comment not found'
    
@app.route('/update/<id>/<comment>')
def update(id, comment):
    if comments.get(id):
        comments[id]['comment'] = comment
        return 'Comment updated'
    else:
        return 'Comment not found'

if __name__ == '__main__':
    app.run()