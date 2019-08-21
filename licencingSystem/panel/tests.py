import unittest

from panel.serializers import UserSerializer, PlanSerializer, CustomerSerializer, WebsiteSerializer


"""
Note to the examiner

I usually write functional test cases for api test cases using django.test.TestCase (Transactional test case)
which also verifies the db operation we have performed in right manner.

I also write selenium test cases in some cases to test end-to-end UI test.

unittests are written without hitting the db for helper functions and serializer validations.
If db operation performed I mock the function and get the return value to test other than the db operations
are working perfectly.

"""

class UserSerializerTestCase(unittest.TestCase):
	
	def setUp(self):
		pass
	
	def tearDown(self):
		pass
	
	def test_UserSerializer_with_email_only(self):
		serializer = UserSerializer(data={'email': 'jpt@gmail.com'})
		is_valid = serializer.is_valid()
		self.assertEqual(is_valid, False)
		
	def test_UserSerializer_with_email_password_and_wrong_confirm_password(self):
		serializer = UserSerializer(data={'email': 'jpt@gmail.com', 'password': '1', 'confirm_password': '2'})
		is_valid = serializer.is_valid()
		self.assertEqual(is_valid, False)
		
	def test_UserSerializer_with_valid_fields(self):
		serializer = UserSerializer(data={'email': 'jpt@gmail.com', 'password': '1', 'confirm_password': '1'})
		is_valid = serializer.is_valid()
		self.assertEqual(is_valid, True)


class WebsiteSerializerTestCase(unittest.TestCase):
	
	def setUp(self):
		pass
	
	def tearDown(self):
		pass
	
	def test_WebsiteSerializer(self):
		serializer = WebsiteSerializer(data={'url': 'something.com'})
		is_valid = serializer.is_valid()
		self.assertEqual(is_valid, False)


class CustomerSerializerTestCase(unittest.TestCase):
	
	def setUp(self):
		pass
	
	def tearDown(self):
		pass
	
	def test_CustomerSerializer(self):
		serializer = CustomerSerializer(data={})
		is_valid = serializer.is_valid()
		self.assertEqual(is_valid, False)


class PlanSerializerTestCase(unittest.TestCase):
	
	def setUp(self):
		pass
	
	def tearDown(self):
		pass
	
	def test_UserSerializer(self):
		serializer = PlanSerializer(data={'name': 'some', 'price': 2000, 'website_allowed': 3})
		is_valid = serializer.is_valid()
		self.assertEqual(is_valid, True)