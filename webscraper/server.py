import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import flask
from flask import request
from flask import jsonify
import pprint

app = flask.Flask(__name__)
cred = credentials.Certificate("credentials/credentials.json")

firebase_admin.initialize_app(cred,options={
    'databaseURL': 'https://smartfit-3ad0b.firebaseio.com/'
})

root = db.reference('women').child('denim-1-backup2')


@app.route('/item/<int:id>')
def recommend(id):
    max_recommendations = 9
    #get params
    big=request.args.get('tooBig') and request.args.get('tooBig').lower()=='true'
    small=request.args.get('tooSmall') and request.args.get('tooSmall').lower()=='true'
    pricey=request.args.get('tooPricey') and request.args.get('tooPricey').lower()=='true'
    color=request.args.get('wrongColor') and request.args.get('wrongColor').lower()=='true'
    similar=request.args.get('showSimilar') and request.args.get('showSimilar').lower()=='true'

    def cleanUp(item):
        #get first size for now
        item['size'] = item['sizes'][0]
        del item['sizes']
        del item['recommendations']
        del item['url']
        return item

    currItem = root.child(str(id)).get()
    if not currItem:
        return 'Error: Invalid item id'
    if small and big:
        return 'Error: Item cannot be both big and small'

    pprint.pprint(currItem)
    recs=currItem['recommendations']
    recommendations={}
    for r in recs:
        if (len(recommendations)>max_recommendations):
            continue 
        recommendations[r] = cleanUp(root.child(str(r)).get())
    pprint.pprint(recommendations)
    return jsonify(recommendations)

@app.route('/item2/<int:id>/<int:size>')
def recommend2(id, size):
    max_recommendations = 9
    #get params
    big=request.args.get('tooBig') and request.args.get('tooBig').lower()=='true'
    small=request.args.get('tooSmall') and request.args.get('tooSmall').lower()=='true'
    pricey=request.args.get('tooPricey') and request.args.get('tooPricey').lower()=='true'
    color=request.args.get('wrongColor') and request.args.get('wrongColor').lower()=='true'
    similar=request.args.get('showSimilar') and request.args.get('showSimilar').lower()=='true'

    def cleanUp(item):
        #get first size for now
        item['size'] = item['sizes'][0]
        del item['sizes']
        del item['recommendations']
        del item['url']
        return item

    currItem = root.child(str(id)).get()
    if not currItem:
        return 'Error: Invalid item id'
    if small and big:
        return 'Error: Item cannot be both big and small'

    pprint.pprint(currItem)
    recs=currItem['recommendations']
    recommendations={}
    for r in recs:
        if (len(recommendations)>max_recommendations):
            continue 
        recommendations[r] = cleanUp(root.child(str(r)).get())
    pprint.pprint(recommendations)
    return jsonify(recommendations)
