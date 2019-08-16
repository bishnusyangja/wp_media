from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
# Create your models here.


class UserManager(BaseUserManager):

	def _create_user(self, name,  email, password,
					 is_staff, is_superuser, **extra_fields):
		"""
		Creates and saves a User with the given  email and password.
		"""
		current_time = now()
		if not email:
			raise ValueError('The given email must be set')
		email = self.normalize_email(email)
		user = self.model(email=email,
						  name=name,
						  is_staff=is_staff, is_active=True,
						  is_superuser=is_superuser, last_login=current_time, **extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_user(self, name,  email, password=None, **extra_fields):
		return self._create_user(name, email, password, False, False,
								 **extra_fields)

	def create_superuser(self, name,  email, password, **extra_fields):
		return self._create_user(name, email, password, True, True,
								 **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['name', ]
	name = models.CharField(u"Name", max_length=200, blank=False)
	email = models.EmailField(u"email address", blank=False, unique=True)
	is_staff = models.BooleanField(u"staff status", default=False,
								   help_text=_('Designates whether the user can log into this admin site.'))
	is_active = models.BooleanField(u"Active", default=True, help_text=_(
		'Designates whether this user should be treated as active. Unselect this instead of deleting accounts.'))
	created_on = models.DateTimeField(u'Created Date', auto_now_add=True)
	modified_on = models.DateTimeField(u'Modified Date', auto_now=True)
	
	objects = UserManager()


class Plan(models.Model):
	name = models.CharField(max_length=100)
	price = models.PositiveIntegerField()
	website_allowed = models.PositiveIntegerField()


class Customer(models.Model):
	user = models.ForeignKey(User, on_delete=models.PROTECT)
	subscription = models.ForeignKey(Plan, on_delete=models.PROTECT)
	subscription_renewed_on = models.DateTimeField(default=None, null=True)
	subscription_valid_till = models.DateTimeField(default=None, null=True)


class Website(models.Model):
	url = models.URLField()
	customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
	



# Licencing System
#
# We would like to see how you solve an OO design problem. Let's create a simple subscription system.
# The goal is to emulate buying a yearly plan and attach website(s) to it.
#
# There are 3 business entities :
#
# - Customer - has a name, a password an email address, a subscription and a subscription renewal date.
# - Plan - has a name, a price, and a number of websites allowance.
# - Website - has an URL, and a customer
#
#
# A customer should be able to subscribe to plan, move from a plan to another and manage websites
# (add/update/remove) according to his plan.
# Subscriptions have a 1-year time value.
#
#
#
# Notes :
# - Having a DB is optional
# - We have 3 plans :
# 	- Single, 1 website, 49$
# 	- Plus, 3 websites $99
# 	- Infinite, unlimited websites $249
#
#
# - Please add automated tests, using unittest
# - Please use plain Python for this test : no framework . Of course any useful libraries can be used
# - Since we are looking for OOP architecture/pattern, no front-end is needed.
#
# Code should be posted on Github/Gitlab/BitBucket
