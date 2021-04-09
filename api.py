from flask import Flask
from flask_restful import Api, Resource, reqparse, abort

from flask import request, jsonify

app = Flask(__name__)
app.config["DEBUG"] = True
api = Api(app)

users = [
    {'id': 0, 'username': 'Fire'},
    {'id': 1, 'username': 'Omelas'},
    {'id': 2, 'username': 'Dhalgren'}
]

@app.route('/api/users', methods=['GET', 'SET'])
def usr():
    if request.method == 'GET':
        return jsonify(users)
    
    if request.method == 'SET':
        return "GOT USER"

app.run()