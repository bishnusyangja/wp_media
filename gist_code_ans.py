# from dateutil.relativedelta import relativedelta
from rest_framework import viewsets
from rest_framework.response import *
import json


# these two classes are created just to avoid warning message in python for my personal comfortability:
class UserSerializer(object):
    pass


class User(object):
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
        if not request.user.is_authenticated:
            # return Response("You should be authenticated")
            return HttpResponseRedirect(settings.LOGIN_URL)
        
        
# views.py

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.none() # by default no data is passed

    ''' authentication is checked in LoginRequiredMiddleware so no authentication is not required in
        this view
        
        user create and validation and other actions with data is performed in serializer so all the actions
        are moved in serializer class
        
        no need to write create method by default viewsets class does it. Viewsets reads data from request and
        send it to serializer and response accordingly as validation. If any validation fails ValidationError
        is raised and viewsets handle the exception and sends error message with 400 status code.
        '''
    
    def get_queryset(self):
        # filtered data is passed according to user type
        # for example all user list is available only for user.is_staff type
        # we can check request.user.is_staff and filter accordingly
        return User.objects.all()

    def get_serializer_context(self):
        cntx = super().get_serializer_context()
        cntx.update({'user', self.request.user})
        return cntx
        
        
# serializer.py
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('email', 'comment', 'password', 'confirm_password', )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user   = self.context.get('user', None)
        # requested user if needed we can pass from context currently it is not used here
        # just we can pass extra arguments from context get_serializer_context from view.

        for field in self.fields.values():
            field.error_messages.update({'required': '"{fieldname}"  is required'.format(fieldname=field.label),
                                     'blank': '"{fieldname}" is not allowed blank'.format(fieldname=field.label)})
            
    def is_passwd_confirmed(self, password, confirm_password):
        return password == confirm_password

    def create(self, validated_data):
        password = validated_data.pop('password', '')
        confirm_password = validated_data.pop('confirm_password', '')
        if not self.is_passwd_confirmed(password, confirm_password):
            raise serializers.ValidationError('password confirmation failed. password and confirm_password did not match')
        
        instance = super().create(validated_data)
        instance.set_password(password)
        instance.save()
        return instance