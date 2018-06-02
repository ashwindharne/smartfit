import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import flask
from flask import jsonify

app = flask.Flask(__name__)
cred = credentials.Certificate("credentials/credentials.json")

firebase_admin.initialize_app(cred,options={
    'databaseURL': 'https://smartfit-3ad0b.firebaseio.com/'
})

root = db.reference('items')

@app.route('/item/<int:id>')
def show_subpath(id):
    item = root.child('denim').child(str(id)).get()
    if not item:
        print("Invalid Item!")
        return '{}'
    return jsonify(item)

@app.route('/recommend')
def show_subpath(id):
    currentID = request.args.get('currentID')
    if not item:
        print("Invalid Item!")
        return '{}'
    return jsonify(item)