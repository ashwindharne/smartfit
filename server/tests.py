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

	def test_recommendations_invalid_id(self):
		req = requests.request('GET', 'http://127.0.0.1:5000/recommend/blahblah')
		assert(req.content==b'Error: Invalid item id')
		pass
	def test_recommendations_tooBig_tooSmall_error(self):
		req = requests.request('GET', 'http://127.0.0.1:5000/recommend/206025?tooBig=true&tooSmall=true&tooPricey=true&wrongColor=true&showSimilar=true')
		assert(req.content == b'Error: Item cannot be both big and small')

	def test_recommendations_tooBig(self):
		req = requests.request('GET', 'http://127.0.0.1:5000/recommend/206025?tooBig=true&tooSmall=false&tooPricey=false&wrongColor=false&showSimilar=true')
		assert(req.content == b'{"157024":{"brand":"Frame Denim","composition":{"Cotton":"95%","Polyester":"4%","Spandex_Elastane":"1%"},"description":"Blue cotton blend cropped fitted jeans from Frame Denim. ","image":"https://cdn-images.farfetch-contents.com/12/82/87/18/12828718_12951897_480.jpg","name":"Frame Denim","price":"177","size":24,"sizeScale":"WAIST"},"192024":{"brand":"Nobody Denim","composition":{"Cotton":"100%"},"description":"A high rise, slim fit, a-line skirt, constructed in a bright indigo rigid denim. Piper Skirt Familiar features light distressing and a raw frayed hem.","image":"https://cdn-images.farfetch-contents.com/12/58/97/83/12589783_12102393_480.jpg","name":"Nobody Denim","price":"159","size":24,"sizeScale":"WAIST"},"20024":{"brand":"Frame Denim","composition":{"Cotton":"96%","Polyester":"3%","Spandex_Elastane":"1%"},"description":"Ellisfield blue cotton blend Le Nouveau straight leg jeans from Frame Denim. ","image":"https://cdn-images.farfetch-contents.com/12/86/42/39/12864239_13100319_480.jpg","name":"Frame Denim","price":"320","size":24,"sizeScale":"WAIST"},"50024":{"brand":"Frame Denim","composition":{"Cotton":"93%","Polyester":"5%","Spandex_Elastane":"2%"},"description":"Light blue and white cotton blend Le High straight leg jeans from Frame Denim featuring a high waist, a button and zip fly, a waistband with belt loops, a straight leg, frayed edges, a cropped length and an acid dipped hem. ","image":"https://cdn-images.farfetch-contents.com/12/91/23/99/12912399_13264057_480.jpg","name":"Frame Denim","price":"245","size":24,"sizeScale":"WAIST"},"86024":{"brand":"Frame Denim","composition":{"Cotton":"94%","Polyester":"5%","Spandex_Elastane":"1%"},"description":"White cotton blend distressed skinny jeans from Frame Denim. ","image":"https://cdn-images.farfetch-contents.com/12/88/92/49/12889249_13228781_480.jpg","name":"Frame Denim","price":"310","size":24,"sizeScale":"WAIST"},"88024":{"brand":"Frame Denim","composition":{"Cotton":"94%","Polyester":"5%","Spandex_Elastane":"1%"},"description":"White denim distressed high-rise flared jeans from Frame Denim. ","image":"https://cdn-images.farfetch-contents.com/12/91/99/32/12919932_13292412_480.jpg","name":"Frame Denim","price":"235","size":24,"sizeScale":"WAIST"},"current":{"brand":"Frame Denim","composition":{"Cotton":"94%","Polyester":"5%","Spandex_Elastane":"1%"},"description":"White cotton blend distressed skinny jeans from Frame Denim featuring a high rise, a waistband with belt loops, a button and zip fly, a five pocket design, a skinny fit, ripped details and a cropped length. ","image":"https://cdn-images.farfetch-contents.com/12/91/24/04/12912404_13264083_480.jpg","name":"Frame Denim","price":"240","size":25,"sizeScale":"WAIST"}}\n')

	def test_recommendations_tooSmall(self):
		pass
	def test_recommendations_tooPricey(self):
		pass
	def test_recommendations_wrongColor(self):
		pass