import pytz
from django.conf import settings
from rest_framework import serializers


def get_local_time(value):
	np = pytz.timezone(settings.TIME_ZONE)
	value = value.astimezone(np)
	return value


class DateTimeSerializer(serializers.DateTimeField):
	
	def to_representation(self, value):
		value = get_local_time(value)
		date = super(DateTimeSerializer, self).to_representation(value)
		return date


def get_attribute(obj, attribute):
	attr = getattr(obj, attribute, None)
	ret = attr() if callable(attr) else attr
	return ret


def to_string(value):
	value = value.encode('utf-8') if isinstance(value, str) else value
	value = value.decode('utf-8') if isinstance(value, bytes) else value
	value = str(value) if isinstance(value, (int, float)) else value
	value = value.strip() if value else value
	return value


class ForeignKeySerializerField(serializers.Field):
	default_dict = {'name': '', 'pk': None}
	
	def __init__(self, **kwargs):
		self.model = kwargs.pop('model', None)
		self.pk = kwargs.pop('pk', 'pk')
		self.name = kwargs.pop('name', 'name')
		self.many = kwargs.pop('many', False)
		if not self.model:
			raise ValueError('ForeignkeySerializer requires a "model" field.')
		super(ForeignKeySerializerField, self).__init__(**kwargs)
		
	def to_representation_for_list(self, n_value, value):
		value = n_value if len(n_value) > 0 else value
		return [
			{'name': get_attribute(item, self.name),
			 'pk': get_attribute(item, self.pk)} if isinstance(item, self.model) else self.default_dict
			for item in value]
	
	def to_representation(self, value):
		if value:
			if self.many:
				n_value = list(value.all())
				if isinstance(n_value, list):
					self.to_representation_for_list(n_value, value)
				else:
					raise ValueError('Expected list field.')
			else:
				return {'name': get_attribute(value, self.name), 'pk': get_attribute(value, self.pk)} if isinstance(
					value, self.model) else self.default_dict
		else:
			return None
	
	def to_internal_value(self, value):
		if self.many:
			return self.get_queryset(value)
		else:
			return self.get_object(value)
	
	def get_queryset(self, value):
		querydict = {}
		if value:
			if not isinstance(value, list):
				value = to_string(value).split(',')
			querydict['{}__in'.format(self.pk)] = value
			if hasattr(self.model, 'is_deleted'):
				querydict['is_deleted'] = False
			qs = self.model.objects.filter(**querydict)
		else:
			qs = self.model.objects.none()
		return qs
	
	def get_object(self, value):
		querydict = {}
		
		querydict[self.pk] = value
		try:
			obj = self.model.objects.get(**querydict)
		except Exception as e:
			print('ForeignKeySerializerGETObject :', e)
			obj = None
		return obj
