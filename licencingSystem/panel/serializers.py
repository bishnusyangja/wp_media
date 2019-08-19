from rest_framework import serializers

from panel.helpers import ForeignKeySerializerField, DateTimeSerializer
from panel.models import User, Plan, Customer, Website


class UserSerializer(serializers.ModelSerializer):
	confirm_password = serializers.CharField()
	
	class Meta:
		model = User
		fields = ('email', 'password', 'confirm_password', )
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.user   = self.context.get('user', None)
		self.fields['confirm_password'].write_only = True
		self.fields['password'].write_only = True
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
			raise serializers.ValidationError('password confirmation failed. password'
											  'and confirm_password did not match')
		
		instance = super().create(validated_data)
		instance.set_password(password)
		instance.save()
		return instance


class CustomerSerializer(serializers.ModelSerializer):
	user = ForeignKeySerializerField(model=User, pk="pk", name="email")
	subscription_renewed_on = DateTimeSerializer(format='%Y-%m-%d %H:%M', required=False, allow_null=True, read_only=True)
	subscription_valid_till = DateTimeSerializer(format='%Y-%m-%d %H:%M', required=False, allow_null=True, read_only=True)
	
	class Meta:
		model = Customer
		fields = ('user', 'subscription', 'subscription_renewed_on', 'subscription_valid_till',)
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.user = self.context.get('user', None)
		
		for field in self.fields.values():
			field.error_messages.update({'required': '"{fieldname}"  is required'.format(fieldname=field.label),
										 'blank': '"{fieldname}" is not allowed blank'.format(fieldname=field.label)})


class WebsiteSerializer(serializers.ModelSerializer):
	class Meta:
		model = Website
		fields = ('url', 'customer',)
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.user = self.context.get('user', None)
		
		for field in self.fields.values():
			field.error_messages.update({'required': '"{fieldname}"  is required'.format(fieldname=field.label),
										 'blank': '"{fieldname}" is not allowed blank'.format(fieldname=field.label)})


class PlanSerializer(serializers.ModelSerializer):
	class Meta:
		model = Plan
		fields = ('name', 'price', 'website_allowed',)
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.user = self.context.get('user', None)
		
		for field in self.fields.values():
			field.error_messages.update({'required': '"{fieldname}"  is required'.format(fieldname=field.label),
										 'blank': '"{fieldname}" is not allowed blank'.format(fieldname=field.label)})

