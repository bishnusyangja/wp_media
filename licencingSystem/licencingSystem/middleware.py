from django.conf import settings
from django.http import HttpResponseRedirect


class MyMiddleware(object):
	def __init__(self, get_response=None):
		self.get_response = get_response
		super().__init__()
	
	def __call__(self, request):
		response = None
		if hasattr(self, 'process_request'):
			response = self.process_request(request)
		response = response or self.get_response(request)
		if hasattr(self, 'process_response'):
			response = self.process_response(request, response)
		return response


class LoginRequiredMiddleware(MyMiddleware):
	
	def process_request(self, request):
		# we can also manage for login_exempt_urls or token_required_urls in our middleware
		if not request.user.is_authenticated():
			# return Response("You should be authenticated")
			return HttpResponseRedirect(settings.LOGIN_URL)
