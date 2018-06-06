import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("credentials/credentials.json")

firebase_admin.initialize_app(cred,options={
    'databaseURL': 'https://smartfit-3ad0b.firebaseio.com/'
})

# ONLY DENIM FOR NOW 
# assume all items are denim
def clean_items_in_db():
    #open firefox browser
    global browser
    browser = webdriver.Firefox()

    # get firebase database 
    database = db.reference('women').child('denim')
    previous_dict = db.reference('women').child('denim').get()
    num_items = len(previous_dict)

    #set up visited and to_visit for bfs through recommendation links
    visited = set()
    to_visit = set()
    #if no previous start, start from random denim url
    if (len(previous_dict)==0):
        starting_url = 'https://www.farfetch.com/shopping/women/frame-denim-classic-skinny-fit-jeans-item-12818474.aspx'
        to_visit = set({starting_url})
    #else, add on to current items 
    else:
        pprint.pprint(previous_dict)
        for obj in previous_dict:
            visited.add(obj['url'])
            if('recommendationUrls' not in obj):
                continue 
            for url in obj['recommendationUrls']: 
                to_visit.add(url)

    #iterate dfs through recommendation links, bfs
    while len(to_visit)>0: 
        item_url = to_visit.pop()
        if(item_url in visited):
            continue 
        visited.add(item_url)
        item = scrape_item('https://www.farfetch.com' + item_url)
        print("Succeeded to scrape " + item_url)
        # save results to database the moment they are gotten
        database.update({num_items : item})
        for url in item['recommendationUrls']:
            to_visit.add(url)
        num_items+=1
    #close browser, SHOULD NEVER GET HERE
    browser.close()

def main():
    clean_items_in_db()

if __name__ == '__main__':
    main()
