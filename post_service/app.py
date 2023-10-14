# post_service.py

from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

posts = {
    '1': {'user_id': '1', 'post': 'Hello, world!'},
    '2': {'user_id': '2', 'post': 'Namaskar Mitro'}
}

@app.route('/post/<id>', methods = ['GET', 'PATCH', 'DELETE'])
def postid(id):
    if request.method == 'GET':
        post_info = posts.get(id, {})
        
        # Get user info from User Service
        if post_info:
            response = requests.get(f'http://localhost:5000/user/{post_info["user_id"]}')
            if response.status_code == 200:
                post_info['user'] = response.json()

        return jsonify(post_info)

    if request.method == 'PATCH':
        user_id = request.form['user_id']
        post = request.form['post']

        posts[id] = {'user_id': user_id, 'post': post}
        return jsonify(f'Post {id} Updated', posts[id])

    if request.method == 'DELETE':
        del posts[id]
        return jsonify(f'Post {id} Deleted', posts)


@app.route('/post', methods = ['GET','POST'])
def post():
    if request.method == 'GET':
        return jsonify(posts)

    if request.method == 'POST':
        user_id = request.form['user_id']
        post = request.form['post']
        new_index = str(len(posts) + 1)
        
        # Get user info from User Service
        response = requests.get(f'http://localhost:5000/user/{user_id}')
        if response.status_code == 200:
            posts[new_index] = {'user_id': user_id, 'post': post}
            return jsonify('New Post Created', posts)
        else:
            return jsonify('User Not Found')

if __name__ == '__main__':
    app.run(port=5001)