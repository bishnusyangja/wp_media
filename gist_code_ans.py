from dateutil.relativedelta import relativedelta
from rest_framework import viewsets
from rest_framework.response import *
import json


# these two classes are created just to avoid warning message in python for my personal comfortability:
class UserSerializer():
    pass


class User():
    id = None
    pass


class UsersViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def create(self, request):
        if not request.user.is_authenticated():
            return Response("You should be authenticated")
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            comment = request.POST["comment"]
            user = User.objects.create(
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password'],
                comment=comment)
            response = {'code': 200, 'success': True, 'id': user.id}
            return Response(response)
        else:
            print ('error on the creation')
            return Response('error')


"""
This is an view to create a user directly through the API while being authenticated.

What do you think of that code? Are there any issues you see? Please describe your evaluation of this code.
Would you write it differently? If so, please rewrite it to meet your standards and explain the reasoning behind
any changes.

"""


"""
Answer of the above code starts from here






"""


# middleware.py
from django.http import HttpResponseRedirect
from django.conf import settings


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
        
        
# views.py
class UsersViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.none()
    # by default no users are available according to permission different filters can
    # be used in queryset and logics are written in get_queryset method

    def create(self, request):
        # authentication is checked in LoginRequiredMiddleware so no authentication is required
        if not request.user.is_authenticated():
            return Response("You should be authenticated")
        
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            comment = request.POST["comment"]
            user = User.objects.create(
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password'],
                comment=comment)
            response = {'code': 200, 'success': True, 'id': user.id}
            return Response(response)
        else:
            print ('error on the creation')
            return Response('error')