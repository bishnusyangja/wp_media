from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets

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
	

class WebSiteAPIView(viewsets.ModelViewSet):
	serializer_class = WebsiteSerializer
	queryset = Website.objects.none()