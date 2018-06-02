import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import flask
from flask import request
from flask import jsonify

app = flask.Flask(__name__)
cred = credentials.Certificate("credentials/credentials.json")

firebase_admin.initialize_app(cred,options={
    'databaseURL': 'https://smartfit-3ad0b.firebaseio.com/'
})

root = db.reference('items')

@app.route('/item/<int:id>')
def recommend(id):
    currItem = root.child('denim').child(str(id)).get()
    big=request.args.get('tooBig') and request.args.get('tooBig').lower()=='true'
    small=request.args.get('tooSmall') and request.args.get('tooSmall').lower()=='true'
    pricey=request.args.get('tooPricey') and request.args.get('tooPricey').lower()=='true'
    color=request.args.get('wrongColor') and request.args.get('wrongColor').lower()=='true'
    similar=request.args.get('showSimilar') and request.args.get('showSimilar').lower()=='true'

    if not currItem:
        return 'Error: Invalid item id'
    if small and big:
        return 'Error: Item cannot be both big and small'

    recommendedItems = {
        '2':root.child('denim').child(str(2)).get(),
        '23':root.child('denim').child(str(3)).get(),
        '3':root.child('denim').child(str(4)).get()
    }

    return jsonify(recommendedItems)
