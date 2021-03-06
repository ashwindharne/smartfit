import pprint
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from collections import OrderedDict

cred = credentials.Certificate("credentials/credentials.json")

firebase_admin.initialize_app(cred,options={
    'databaseURL': 'https://smartfit-3ad0b.firebaseio.com/'
})

#maps objects to ids
def get_url_mapper():
    data_dict = db.reference('women').child('denim').get()
    url_mapper = {}
    num = 0
    for obj in data_dict:
        url_mapper[obj['url']] = num
        obj['id'] = num
        num += 1

    db.reference('women').child('denim_clean').set(data_dict)
    return url_mapper


#convert recommendationUrls to numbers
def add_recommendation_ids(url_mapper):
    # get firebase database 
    data_dict = db.reference('women').child('denim_clean').get()

    for obj in data_dict:
        # some don't have any recommendationUrls 
        #if they don't, ignore
        if('recommendationUrls' not in obj):
            continue 
        recommendations = set()
        for url in obj['recommendationUrls']:
            #some recommendations were not yet collected 
            if (url in url_mapper): 
                recommendations.add(url_mapper[url])
        #use set to avoid dups, convert to list to make it serializable
        obj['recommendations'] = list(recommendations)

    db.reference('women').child('denim_clean').set(data_dict)

#add recommendations from recommendations to inflate recommendations lists
def inflate_recommendations(url_mapper):
    # get firebase database 
    data_dict = db.reference('women').child('denim_clean').get()
    # for each item, iterate through recommendations of recommendations 
    list_data_dict = list(data_dict)

    for obj in data_dict:
        # some don't have any recommendationUrls 
        #if they don't, ignore
        if('recommendations' not in obj):
            continue 
        recommendations = list(obj['recommendations'])
        recommendations_new = list(obj['recommendations'])
        for ID in recommendations:
            item_other = list_data_dict[int(ID)]
            if('recommendations' not in item_other):
                continue
            for rec in item_other['recommendations']:
                #recommending self is allowed
                recommendations_new.append(rec)
        #use set to avoid dups, convert to list to make it serializable
        obj['recommendations'] = list(OrderedDict.fromkeys(recommendations_new))
    db.reference('women').child('denim_clean').set(data_dict)


#Using https://www.vince.com/womenssizeguide.html#womensize for standardization into waist size
#standardize sizes such as Italian, US, etc 
def standardize_sizes():
    # get firebase database 
    data_dict = db.reference('women').child('denim_clean').get()
    sizeConversions = {
        'XXS':23,
        'XS':25,
        'S':27,
        'M':29,
        'L':30,
        'XL':33,
        'XXL':35
    }
    for obj in data_dict:
        newSizes = []
        for size in obj['sizes']:
            if size in sizeConversions:
                newSizes.append(sizeConversions[size])
            else:
                try: 
                    #if size is int, just append it
                    int(size)
                    newSizes.append(size)
                except:
                    #if size is unrecognizable, pretend it's 30 
                    newSizes.append('30')
        obj['sizes'] = newSizes
    db.reference('women').child('denim_clean').set(data_dict)

# convert list to a dictionary
# for easier access
def convert_list_to_dict():
    data_list = db.reference('women').child('denim_clean').get()
    data_dict = {}
    num = 0
    for obj in data_list:
        data_dict[num] = obj
        num += 1

    db.reference('women').child('denim_clean').set(data_dict)

# ONLY DENIM FOR NOW 
# assume all items are denim
def clean_items_in_db():
    url_mapper = get_url_mapper()
    add_recommendation_ids(url_mapper)
    inflate_recommendations(url_mapper)
    standardize_sizes()
    convert_list_to_dict()

def main():
    clean_items_in_db()

if __name__ == '__main__':
    main()
