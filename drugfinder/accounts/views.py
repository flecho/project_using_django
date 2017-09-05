# -*- coding: utf-8 -*-
# django module
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, Http404
from django.views.decorators.csrf import csrf_exempt

# jwt module
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import JSONWebTokenSerializer
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer
from rest_framework_jwt.serializers import RefreshJSONWebTokenSerializer
from rest_framework_jwt.views import JSONWebTokenAPIView
from rest_framework_jwt.views import ObtainJSONWebToken
from rest_framework_jwt.settings import api_settings

# rest_framework module
from rest_framework.authentication import SessionAuthentication
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

# my module
from .forms import SignUpForm
from .models import MyUser
from .serializers import MyUserSerializer
from .serializers import ChangeProfileSerializer

# for practice
from .forms import GenerateRandomUserForm
from django.shortcuts import redirect
from django.contrib import messages
from django.views.generic.edit import FormView

import datetime
import time
from celery import shared_task

#jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER


# SignIn is implemented as a form of obtain_token. 
# JWT Library supports it. 

def jwt_response_payload_handler(token, user=None, request=None):
	'''
		Returns the response data for both the login and refresh views.
	'''
	return {
		'token': token,
		'user': MyUserSerializer(user, context={'request': request}).data
	}


class SignIn(ObtainJSONWebToken):

	def post(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)

		if serializer.is_valid():
			user = serializer.object.get('user') or request.user
			token = serializer.object.get('token')
			
			user_object = MyUser.objects.get(email=user.email)
			if not user_object:
				return Response("failed to get a User object.")

			response_data = jwt_response_payload_handler(token, user_object, request)
			response = Response(response_data)

			if api_settings.JWT_AUTH_COOKIE:
				expiration = (datetime.utcnow() +
					  api_settings.JWT_EXPIRATION_DELTA)
				response.set_cookie(api_settings.JWT_AUTH_COOKIE,
							token,
							expires=expiration,
							httponly=True)
			return response

		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def get(self, request): # for test
		return render(request, 'accounts/signin.html')
		
class SignUp(APIView):
	
	def post(self, request, format=None):
		serializer = MyUserSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save() # create a new user	
			return Response(serializer.data, status=status.HTTP_201_CREATED) # shouldn't expose password.
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)		

	def get(self, request): # for test
		return render(request, 'accounts/signup.html')

# validate 없어도 되나;;
class ChangePassword(APIView):
	permission_classes = (IsAuthenticated,)
	authentication_classes = (JSONWebTokenAuthentication,)

	"""
		Change the user's password
	"""
	def get_object(self, email):
		try:
			return MyUser.objects.get(email=email)
		except MyUser.DoesNotExist:
			raise Http404

	def post(self, request, format=None):
		# email, old_password, new_password
		user = self.get_object(request.data['email'])
		if user.check_password(request.data['old_password']):
			user.set_password(request.data['new_password'])
			user.save()
		else:
			return Response("Password is invalid.")
		return Response("Password has successfully been changed.")

	def get(self, request):
		return Response("Get!")

class GetName(APIView):
	permission_classes = (IsAuthenticated,)
	authentication_classes = (JSONWebTokenAuthentication,)
	"""
		Return the user's name
	"""
	def get_object(self, email): # code repeatition.
		try:
			return MyUser.objects.get(email=email)
		except MyUser.DoesNotExist:
			raise Http404

	def post(self, request, format=None):
		user = self.get_object(request.data['email'])		
		return Response(user.get_name())

class ChangeProfile(APIView):
	permission_classes = (IsAuthenticated,)
	authentication_classes = (JSONWebTokenAuthentication,)
	
	def get_object(self, email): # code repeatition.
		try:
			return MyUser.objects.get(email=email)
		except MyUser.DoesNotExist:
			raise Http404

	def post(self, request, format=None):
		serializer = ChangeProfileSerializer(data=request.data)

		if serializer.is_valid():

			user = self.get_object(serializer.validated_data['email'])
			if serializer.validated_data['name'] != '':
				user.name = serializer.validated_data['name']
			user.icon = serializer.validated_data['icon']
			user.save()
			return Response(serializer.data, status=status.HTTP_205_RESET_CONTENT)

		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)		


