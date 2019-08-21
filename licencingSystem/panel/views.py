import datetime

from django.shortcuts import render

# Create your views here.
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import action

from licencingSystem.permissions import StaffPermission
from panel.models import User, Plan, Customer, Website
from panel.serializers import UserSerializer, PlanSerializer, CustomerSerializer, WebsiteSerializer


class UserAPIView(viewsets.ModelViewSet):
	serializer_class = UserSerializer
	queryset = User.objects.none()
	permission_classes = (StaffPermission, )
	

class PlanAPIView(viewsets.ModelViewSet):
	serializer_class = PlanSerializer
	queryset = Plan.objects.none()
	
	http_method_names = ('get', )
	
	def get_queryset(self):
		return Plan.objects.all()
	

class CustomerAPIView(viewsets.ModelViewSet):
	serializer_class = CustomerSerializer
	queryset = Customer.objects.none()
	
	# requesting new subscription plan automatically updates the subscription plan
	# so I have not implemented subscription update plan
	@action(detail=True, methods=['PATCH'])
	def add_subscription(self, request, *args, **kwargs):
		obj = self.get_object()
		now = timezone.now()
		obj.subcription_renewed_on = now
		obj.subscription_valid_till = now + datetime.timedelta(days=365) # added 1 year time for plan
		obj.save()
	
	@action(detail=True, methods=['PATCH'])
	def remove_subscription(self, request, *args, **kwargs):
		obj = self.get_object()
		obj.subcription_renewed_on = None
		obj.subscription_valid_till = None
		obj.save()


class WebSiteAPIView(viewsets.ModelViewSet):
	serializer_class = WebsiteSerializer
	queryset = Website.objects.none()