# user_service.py

from flask import Flask, jsonify, request

app = Flask(__name__)

users = {
    '1': {'name': 'Modi', 'email': 'Modiji@example.com'},
    '2': {'name': 'Shah', 'email': 'Motabhai@example.com'}
}
@app.route('/user', methods = ['GET','POST'])
def user():
    if request.method == 'GET':
        return jsonify(users)
    
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        new_index = str(len(users) + 1)

        users[new_index] = {'name': name, 'email': email}
        return jsonify('New User Created', users)

@app.route('/user/<id>', methods = ['GET', 'PATCH', 'DELETE'])
def userid(id):
    if request.method == 'GET':
        user_info = users.get(id, {})
        return jsonify(user_info)
    
    if request.method == 'PATCH':
        name = request.form['name']
        email = request.form['email']

        users[id] = {'name': name, 'email': email}
        return jsonify(f'User {id} Updated', users[id])
    
    if request.method == 'DELETE':
        del users[id]
        return jsonify(f'User {id} Deleted', users)

if __name__ == '__main__':
    app.run(port=5000)