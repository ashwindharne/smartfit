import unittest
import requests
import json

class SmartFitUnitTests(unittest.TestCase):
	def setup(self):
		pass
	def teardown(self):
		pass
	def test_fitting_check_smoketest(self):
		req = requests.request('GET', 'http://127.0.0.1:5000/fitting')
		assert(req.content != 0)

	def test_01_fitting_request_submission(self):
		req=requests.request('GET', 'http://127.0.0.1:5000/fitting/request_item?itemID=2025&roomNumber=99')
		assert(req.content == b'Successfully requested 2025 for room 99')

	def test_02_fitting_request_error(self):
		req = requests.request('GET', 'http://127.0.0.1:5000/fitting/request_item?itemID=2025&roomNumber=99')
		assert(req.content == b'Error: 2025 has already been requested!')

	def test_04_fitting_fulfilled(self):
		req = requests.request('GET', 'http://127.0.0.1:5000/fitting/fulfill_item?itemID=2025&roomNumber=99')
		assert(req.content == b'Successfully fulfilled 2025 for room 99')

	def test_05_fitting_fulfilled_db(self):
		req = requests.request('GET', 'http://127.0.0.1:5000/fitting')
		fitting = json.loads(req.content.decode('utf-8'))
		try:
			assert(not fitting[0]['99'])
		except KeyError:
			pass

	def test_06_fitting_fulfilled_error(self):
		req = requests.request('GET', 'http://127.0.0.1:5000/fitting/fulfill_item?itemID=2025&roomNumber=99')
		assert(req.content == b'Error: 2025 does not exist in requests!')

	def test_recommendations(self):
		req = requests.request('GET', 'http://127.0.0.1:5000/recommend/206025?tooBig=false&tooSmall=true&tooPricey=true&wrongColor=true&showSimilar=true' )
		recs = json.loads(req.content.decode('utf-8'))
		correctRecs = {
		  "47026": {
		    "brand": "Frame Denim",
		    "composition": {
		      "Cotton": "93%",
		      "Spandex_Elastane": "7%"
		    },
		    "description": "Blue cotton stretch skinny jeans  from Frame Denim. ",
		    "image": "https://cdn-images.farfetch-contents.com/12/88/28/96/12882896_13211469_480.jpg",
		    "name": "Frame Denim",
		    "price": "215",
		    "sizeScale": "WAIST"
		  },
		  "88026": {
		    "brand": "Frame Denim",
		    "composition": {
		      "Cotton": "94%",
		      "Polyester": "5%",
		      "Spandex_Elastane": "1%"
		    },
		    "description": "White denim distressed high-rise flared jeans from Frame Denim. ",
		    "image": "https://cdn-images.farfetch-contents.com/12/91/99/32/12919932_13292412_480.jpg",
		    "name": "Frame Denim",
		    "price": "235",
		    "sizeScale": "WAIST"
		  },
		  "88027": {
		    "brand": "Frame Denim",
		    "composition": {
		      "Cotton": "94%",
		      "Polyester": "5%",
		      "Spandex_Elastane": "1%"
		    },
		    "description": "White denim distressed high-rise flared jeans from Frame Denim. ",
		    "image": "https://cdn-images.farfetch-contents.com/12/91/99/32/12919932_13292412_480.jpg",
		    "name": "Frame Denim",
		    "price": "235",
		    "sizeScale": "WAIST"
		  },
		  "157026": {
		    "brand": "Frame Denim",
		    "composition": {
		      "Cotton": "95%",
		      "Polyester": "4%",
		      "Spandex_Elastane": "1%"
		    },
		    "description": "Blue cotton blend cropped fitted jeans from Frame Denim. ",
		    "image": "https://cdn-images.farfetch-contents.com/12/82/87/18/12828718_12951897_480.jpg",
		    "name": "Frame Denim",
		    "price": "177",
		    "sizeScale": "WAIST"
		  },
		  "157027": {
		    "brand": "Frame Denim",
		    "composition": {
		      "Cotton": "95%",
		      "Polyester": "4%",
		      "Spandex_Elastane": "1%"
		    },
		    "description": "Blue cotton blend cropped fitted jeans from Frame Denim. ",
		    "image": "https://cdn-images.farfetch-contents.com/12/82/87/18/12828718_12951897_480.jpg",
		    "name": "Frame Denim",
		    "price": "177",
		    "sizeScale": "WAIST"
		  },
		  "192026": {
		    "brand": "Nobody Denim",
		    "composition": {
		      "Cotton": "100%"
		    },
		    "description": "A high rise, slim fit, a-line skirt, constructed in a bright indigo rigid denim. Piper Skirt Familiar features light distressing and a raw frayed hem.",
		    "image": "https://cdn-images.farfetch-contents.com/12/58/97/83/12589783_12102393_480.jpg",
		    "name": "Nobody Denim",
		    "price": "159",
		    "sizeScale": "WAIST"
		  },
		  "current": {
		    "brand": "Frame Denim",
		    "composition": {
		      "Cotton": "94%",
		      "Polyester": "5%",
		      "Spandex_Elastane": "1%"
		    },
		    "description": "White cotton blend distressed skinny jeans from Frame Denim featuring a high rise, a waistband with belt loops, a button and zip fly, a five pocket design, a skinny fit, ripped details and a cropped length. ",
		    "image": "https://cdn-images.farfetch-contents.com/12/91/24/04/12912404_13264083_480.jpg",
		    "name": "Frame Denim",
		    "price": "240",
		    "size": 25,
		    "sizeScale": "WAIST"
		  }
		}
		assert(recs == correctRecs)