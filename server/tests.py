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

	def test_recommendations_invalid_id_string(self):
		req = requests.request('GET', 'http://127.0.0.1:5000/recommend/blahblah')
		assert(req.content==b'Error: Invalid item id')

	def test_Recommendations_invalid_id_number(self):
		req = requests.request('GET', 'http://127.0.0.1:5000/recommend/123')
		assert (req.content == b'Error: Invalid item id')

	def test_recommendations_tooBig_tooSmall_error(self):
		req = requests.request('GET', 'http://127.0.0.1:5000/recommend/206025?tooBig=true&tooSmall=true&tooPricey=true&wrongColor=true&showSimilar=true')
		assert(req.content == b'Error: Item cannot be both big and small')

	def test_recommendations_tooBig(self):
		req = requests.request('GET', 'http://127.0.0.1:5000/recommend/206025?tooBig=true&tooSmall=false&tooPricey=false&wrongColor=false&showSimilar=true')
		recommendations = json.loads(req.content.decode('utf-8'))
		ret = True
		for elem in recommendations:
			if not elem == 'current':
				if(int(recommendations[elem]['size']) >= 25):
					ret=False
		assert(ret)

	def test_recommendations_tooSmall(self):
		req = requests.request('GET', 'http://127.0.0.1:5000/recommend/206025?tooBig=false&tooSmall=true&tooPricey=false&wrongColor=false&showSimilar=true')
		recommendations = json.loads(req.content.decode('utf-8'))
		ret = True
		for elem in recommendations:
			if not elem == 'current':
				if (int(recommendations[elem]['size']) <= 25):
					ret = False
		assert(ret)

	def test_recommendations_tooPricey(self):
		req = requests.request('GET','http://127.0.0.1:5000/recommend/206025?tooBig=false&tooSmall=false&tooPricey=true&wrongColor=false&showSimilar=true')
		recommendations = json.loads(req.content.decode('utf-8'))
		ret = True
		for elem in recommendations:
			if not elem == 'current':
				if (int(recommendations[elem]['price']) >= int(recommendations['current']['price'])):
					ret = False
		assert(ret)
