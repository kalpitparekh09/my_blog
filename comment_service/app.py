# comment_service.py

from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

comments = {
    '1': {'user_id': '1', 'post_id': '1', 'comment': 'Hello, world!'},
    '2': {'user_id': '2', 'post_id': '2', 'comment': 'Namaskar Mitro'}
}

@app.route('/comment/<id>',  methods = ['GET', 'PATCH', 'DELETE'])
def commentid(id):
    if request.method == 'GET':
        comment_info = comments.get(id, {})
        
        if comment_info:
        # Get user info from User Service
            response = requests.get(f'http://localhost:5000/user/{comment_info["user_id"]}')
            if response.status_code == 200:
                comment_info['user'] = response.json()
        # Get post info from User Service
            response = requests.get(f'http://localhost:5001/post/{comment_info["post_id"]}')
            if response.status_code == 200:
                comment_info['post'] = response.json()

        return jsonify(comment_info)

    if request.method == 'PATCH':
        user_id = request.form['user_id']
        post_id = request.form['post_id']
        comment = request.form['comment']

        comments[id] = {'user_id': user_id, 'post_id': post_id, 'comment': comment}
        return jsonify(f'Comment {id} Updated', comments[id])

    if request.method == 'DELETE':
        del comments[id]
        return jsonify(f'Comment {id} Deleted', comments)

@app.route('/comment',  methods = ['GET', 'POST'])
def comment():
    if request.method == 'GET':
        return jsonify(comments)

    if request.method == 'POST':
        user_id = request.form['user_id']
        post_id = request.form['post_id']
        comment = request.form['comment']
        new_index = str(len(comments) + 1)
        
        # Get user info from User Service and post info from Post Service
        response1 = requests.get(f'http://localhost:5000/user/{user_id}')
        response2 = requests.get(f'http://localhost:5001/post/{post_id}')
        if response1.status_code == 200 and response2.status_code == 200:
            comments[new_index] = {'user_id': user_id, 'post_id': post_id, 'comment': comment}
            return jsonify('New Comment Created', comments)
        else:
            return jsonify('User or Post Not Found')

if __name__ == '__main__':
    app.run(port=5002)