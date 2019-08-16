from rest_framework import serializers
from panel.models import User


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
			raise serializers.ValidationError \
				('password confirmation failed. password and confirm_password did not match')
		
		instance = super().create(validated_data)
		instance.set_password(password)
		instance.save()
		return instance


class PlanSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('email', 'comment', 'password', 'confirm_password',)
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.user = self.context.get('user', None)
		# requested user if needed we can pass from context currently it is not used here
		# just we can pass extra arguments from context get_serializer_context from view.
		
		for field in self.fields.values():
			field.error_messages.update({'required': '"{fieldname}"  is required'.format(fieldname=field.label),
										 'blank': '"{fieldname}" is not allowed blank'.format(fieldname=field.label)})


class CustomerSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('email', 'comment', 'password', 'confirm_password',)
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.user = self.context.get('user', None)
		# requested user if needed we can pass from context currently it is not used here
		# just we can pass extra arguments from context get_serializer_context from view.
		
		for field in self.fields.values():
			field.error_messages.update({'required': '"{fieldname}"  is required'.format(fieldname=field.label),
										 'blank': '"{fieldname}" is not allowed blank'.format(fieldname=field.label)})


class WebsiteSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('email', 'comment', 'password', 'confirm_password',)
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.user = self.context.get('user', None)
		# requested user if needed we can pass from context currently it is not used here
		# just we can pass extra arguments from context get_serializer_context from view.
		
		for field in self.fields.values():
			field.error_messages.update({'required': '"{fieldname}"  is required'.format(fieldname=field.label),
										 'blank': '"{fieldname}" is not allowed blank'.format(fieldname=field.label)})
