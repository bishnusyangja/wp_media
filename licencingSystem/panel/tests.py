import unittest

from panel.serializers import UserSerializer


class PanelTestCase(unittest.TestCase):
	
	def setUp(self):
		pass
	
	def tearDown(self):
		pass
	
	def test_UserSerializer(self):
		serializer = UserSerializer(data={'email': 'jpt@gmail.com'})
		is_valid = serializer.is_valid()
		self.assertEqual(is_valid, False)