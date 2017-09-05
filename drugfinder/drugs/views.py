#-*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from .models import Drug
from .serializers import DrugSerializer
from .serializers import UserImageSerializer
from .serializers import CandidateSerializer
from .serializers import UserSelectSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from celery import shared_task
from PIL import Image
import boto3, botocore
import itertools
import os

## CONSTANTS ##		
CANDIDATES_MAX = 10

class GetSampledData(APIView):
	''' API View that returns a detailed information of a particular pill'''
	authentication_classes = (JSONWebTokenAuthentication,)
	permission_classes = (IsAuthenticated,)

	def post(self, request):
		serializer = UserSelectSerializer(data=request.data)
		if serializer.is_valid():
			key_name = serializer.validated_data['kor_name']
			drug = None
			try:
				drug = Drug.objects.get(kor_name=key_name)
			except ObjectDoesNotExist:			
				pass # must never reach here.
		
			if drug:
				drug_serializer = DrugSerializer(drug) 
				return Response(drug_serializer.data)
			else: 
				return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
		else:
			return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

class SendImage(APIView):
	''' API View that returns the result of the recognized pill when a client sends an image.'''
	# This function should be divided into for test and for login users.

	# User-email info needed.
	# In s3, files are stored like the following:
	#	'positive/flecho@naver.com/date-time.jpg'

	authentication_classes = (JSONWebTokenAuthentication,)	
	permission_classes = (IsAuthenticated,)

	def post(self, request, format=None):

		serializer = UserImageSerializer(data=request.data)
		if serializer.is_valid(): # When deserializing data, you always need to call is_valid().
			email = serializer.validated_data['email']
			image = serializer.validated_data['image']

			if not os.path.isdir('temp_storage'): # Which path? 
				os.makedirs('temp_storage')

			# Save local spaces first, in order not to send image as a function parameter.
			default_storage.save('temp_storage/' + image.name, ContentFile(image.read()))			

			list_of_chars = Drug.evaluate(str(image.name))						
#			list_of_chars = Drug.evaluate.delay(email, str(image.name))

			drugset = Drug.search(list_of_chars)
			drugset_serializer = CandidateSerializer(drugset, many=True)

			return Response(drugset_serializer.data, status=status.HTTP_200_OK)			
		else:
			return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

class TestSendImage(SendImage):
	authentication_classes = ()	
	permission_classes = ()



	def get(self, request):

		import random		
		letters = 'abcdefghijklmnopqrstuvwxyz0123456789'
		temp_chars = []
		temp_chars.append(letters[int(random.random() * 35)])
		temp_chars.append(letters[int(random.random() * 35)])

#		temp_chars = ['a', 'b', 'c']

		drugset = Drug.search(temp_chars) # static method
		drugset_serializer = CandidateSerializer(drugset, many=True) # ListSerializer로 되나 

		return Response(drugset_serializer.data, status=status.HTTP_200_OK)




