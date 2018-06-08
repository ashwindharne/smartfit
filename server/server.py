import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import flask
from flask import request
from flask import jsonify
import pprint
import copy

app = flask.Flask(__name__)
cred = credentials.Certificate("credentials/credentials.json")

firebase_admin.initialize_app(cred,options = {
    'databaseURL': 'https://smartfit-3ad0b.firebaseio.com/'
})

root = db.reference('women').child('denim_clean')
fitting_root = db.reference('fitting')

def get_ID_and_size(identitystr):
    ID = int(identitystr[:-3])
    size = int(identitystr[-3:])
    return ID, size

def filter_price(recommendations,max_price):
    new_recommendations = []
    #get first size for now
    for item in recommendations:
        price = int(item['price'])
        #remove if too expensive
        if price < max_price:
            new_recommendations.append(item) 
    return new_recommendations

def filter_size(recommendations,sizes):
    new_recommendations = []
    #get first size for now
    for item in recommendations:
        item_sizes = set(map(int,item['sizes']))
        #remove if not in sizes:
        for size in sizes:
            if size in item_sizes:
                item2 = copy.deepcopy(item)
                item2['size'] = size
                item2['id'] = str(item['id'])+"{:03}".format(size)
                new_recommendations.append(item2)
    return new_recommendations

def cleanUp(item):
    if('sizes' in item):
        del item['sizes']
    if('url' in item):
        del item['url']
    if('recommendations' in item):
        del item['recommendations']
    if('recommendationUrls' in item):
       del item['recommendationUrls']
    if('id' in item):
        del item['id']

@app.route('/recommend/<string:identitystr>', methods=['GET'])
def recommend(identitystr):
    global root
    #size is integrated as last three digits of ID
    #last three digits is size, beginning is ID
    #example: 1032
    max_recommendations = 6

    ID, size = get_ID_and_size(identitystr)
    
    objects = root.get()

    currItem = objects[ID]

    if not currItem:
        return 'Error: Invalid item id'
        
    recs = [] 
    if('recommendations' in currItem):
        recs = currItem['recommendations']

    recommendations=[]

    for r in recs:
        recommendations.append(objects[r])

    #filter prices
    pricey = request.args.get('tooPricey') and request.args.get('tooPricey').lower()=='true'
    if pricey:
        recommendations = filter_price(recommendations, int(currItem['price']))

    #filter colors, TODO 
    color = request.args.get('wrongColor') and request.args.get('wrongColor').lower()=='true'

    #always show similar, so ignore this, actually 
    similar = request.args.get('showSimilar') and request.args.get('showSimilar').lower()=='true'

    #filter size
    tooBig = request.args.get('tooBig') and request.args.get('tooBig').lower()=='true'
    tooSmall = request.args.get('tooSmall') and request.args.get('tooSmall').lower()=='true'
    if tooBig and tooSmall:
        return 'Error: Item cannot be both big and small'
    sizes = [size]
    if (tooBig):
        sizes = [size-1, size-2]
    elif(tooSmall):
        sizes = [size+1, size+2]
    recommendations = filter_size(recommendations, sizes)

    if tooBig and tooSmall and not tooPricey and not pricey and not color and not similar:
        return 'Error: must have at least one parameter set to true!'

    #selction only top
    selection = recommendations[:max_recommendations]

    results = {}
    for s in selection:
        ID = s['id']
        results[ID] = s

    #include current info too
    currItem['size'] = size
    results['current'] = currItem

    #remove unneeded info for display
    for key,item in results.items():
        cleanUp(item)
        
    return jsonify(results)

@app.route('/fitting', methods=['GET'])
def get_fitting_items():
    global fitting_root, root
    max_rooms = 9
    data_collected = {}

    objects = root.get()
    fitting_room = fitting_root.get()

    for room_number in range(1,max_rooms+1):
        # too long 
        if(room_number >= len(fitting_room)):
            break 
        room = fitting_room[room_number]

        if(room == None):
            continue 
        room_data = {}
        for identitystr in room: 
            ID, size = get_ID_and_size(identitystr)
            item = objects[ID]
            item['size'] = size
            cleanUp(item)
            room_data[identitystr] = item
        data_collected[str(room_number)] = room_data 
    return jsonify(data_collected)  

#request and fulfill assume that you can request/fulfill multiple items at the same time
# use get requests for now
@app.route('/fitting/request_item', methods=['GET'])
def request_item():
    global fitting_root
    roomNumber = request.args.get('roomNumber')  
    itemID = request.args.get('itemID')  
    #confirm parameters are reasonable
    if roomNumber == None:
        return 'Error: no room number parameter found!'
    if itemID == None:
        return 'Error: no itemID parameter found!'
    #confirm that request is an integer
    try:
        int(itemID)
    except:
        return 'Error: itemID must be an integer!'

    currItems = fitting_root.child(roomNumber).get();
    if currItems == None:
        currItems = []
    if itemID in currItems:
        return 'Error: ' + itemID + ' has already been requested!'
    
    currItems.append(itemID)
    #update fitting room with new data
    fitting_root.update({roomNumber:currItems});
    return 'Successfully requested ' + itemID + ' for room ' + roomNumber

@app.route('/fitting/fulfill_item', methods=['GET'])
def fulfill_item():
    global fitting_root
    roomNumber = request.args.get('roomNumber')  
    itemID = request.args.get('itemID')  
    #confirm parameters are reasonable
    if roomNumber == None:
        return 'Error: no room number parameter found!'
    if itemID == None:
        return 'Error: no itemID parameter found!'
    currItems = fitting_root.child(roomNumber).get();
    if currItems == None:
        currItems = []
    if itemID not in currItems:
        return 'Error: ' + itemID + ' does not exist in requests!'
    
    currItems.remove(itemID)
    #update fitting room with new data
    fitting_root.update({roomNumber:currItems});
    return 'Successfully fulfilled ' + itemID + ' for room ' + roomNumber

if __name__ == "__main__":
	app.run(debug=True,threaded=True)