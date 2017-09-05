# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
'''
	To make it easy to include Django's permission framework into your own userclass, Django provides PermissionsMixin. This is an abstract model you can include in the class hierarchy for your user model, giving you all the methods and database fields necessary to support Django's permission model.
'''

class MyUserManager(BaseUserManager):

	def create_user(self, email, name, date_of_birth, sex, password=None, icon=0):
		"""
		Creates and saves a User with the given email, date of
		birth and password.
		"""
		if not email:
			raise ValueError('Users must have an email address')

		user = self.model(
			email=self.normalize_email(email),
			name=name,
			date_of_birth=date_of_birth,
			sex=sex,
			icon=icon,
		)

		user.set_password(password)
#		user.groups.add(group, group, ...)
#		user.user_permissions.add('permission_name')
		user.save(using=self._db)
		return user

	def create_superuser(self, email, name, date_of_birth, sex, password, icon=0):
		"""
		Creates and saves a superuser with the given email, date of
		birth and password.
		"""
		user = self.create_user(
			email=self.normalize_email(email),
			name=name,
			password=password,
			date_of_birth=date_of_birth,
			sex=sex,
			icon=icon,
        )
		user.is_admin = True
		user.save(using=self._db)
		return user

	def create_manager(self, email, name, date_of_birth, sex, password, icon=0):
		"""
		Creates and saves a manager with the given email, date of birth and password
		A manager is entitled to see hidden page on the application.
		"""
		user = self.create_user(
			email=self.normalize_email(email),
			name=name,
			date_of_birth=date_of_birth,
			sex=sex,
			icon=icon,
		)
		# group info should be added.
		user.set_password(password)
#		user.groups.add(group, group, ...)
#		user.user_permissions.add('permission_name')
#		user group을 두고 권한을 관리하는 방식이 더 합리적.. 나중에 권한이 추가되거나 삭제될 때 변경하는 게 편리함.
		user.save(using=self._db)
		return user


class MyUser(AbstractBaseUser):
	email = models.EmailField(
		verbose_name='email address',
		max_length=255,
		primary_key=True,
		)
	name = models.CharField(max_length=50)
	date_of_birth = models.DateField()
	sex = models.CharField(max_length=1, default='M')
	icon = models.IntegerField(default=0)	

	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)

	objects = MyUserManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['name', 'date_of_birth', 'sex'] 
	# 'USERNAME_FIELD' for a custom user model must not be included in 'REQUIRED_FIELDS'	

	def get_id(self):
	# The user is identified by their email address
		return self.email

	def get_name(self):
	# The user is identified by their email address
		return self.name

	def __str__(self):              # __unicode__ on Python 2
		return self.email

	def has_perm(self, perm, obj=None):
	# Does the user have a specific permission?
	# Simplest possible answer: Yes, always
		return True

	def has_module_perms(self, app_label):
	# Does the user have permissions to view the app `app_label`?
	# Simplest possible answer: Yes, always
		return True

	@property
	def is_staff(self):
	# Is the user a member of staff?
	# Simplest possible answer: All admins are staff
		return self.is_admin









