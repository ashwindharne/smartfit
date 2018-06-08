# Server Info

### Collecting Data from Farfetch
The data collection script data_scraper.py utilizes the geckodriver for Firefox. It will recursively collect items from Farfetch.com (recommendations from the current items in the database) and add them to the database women.denim. At the start, it will open up a new Firefox browser. Then for each item URL, it will load a GET request to the item's Farfetch URL on the browser, and click the "Recommendations" button. Then, it will wait for the recommendations to load before parsing the page data to collect information about the item including description, title, price, sizes, and recommendations and adding this item's data to the Firebase database. This process takes around 1 second per item and will continue until the script is stopped or all items in this category (~23000) have been loaded into the databse. 

### Cleaning the Data  
The data cleaning script data_cleaner.py will process these items, accomplishing serveral tasks. First, it will correlate each item URL with its own ID. Second, it will augment the data so that recommendations of recommendations are added to its recommendations list. While doing so, it will retain the same recommendation order. Third, it will standardize the sizes to WAIST scale. For example, a 'S' will be converted into a 27 waist. These conversions are according to https://www.vince.com/womenssizeguide.html#womensize. 
This process takes about a millisecond to run per item in the database. 

### Server 
The server server.py must be maintained for the client to grab recommendations and request items, as well as for the shop clerk to view requests and fulfill items. It's primary purpose is to communicate between the client/clerk and the database as well as to filter the recommendations stored on the database.
