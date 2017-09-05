from django.shortcuts import render

from .models import History
from .serializers import EmailSerializer
from .serializers import BookmarkSerializer
from .serializers import HistorySerializer

from accounts.models import MyUser as User

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from rest_framework_jwt.authentication import JSONWebTokenAuthentication




class GetHistory(APIView):
#	authentication_classes = (JSONWebTokenAuthentication,)
#	permission_classes = (IsAuthenticated,)

	def post(self, request):
		# email
		'''
			Expected to get user_email. 
		'''
		serializer = EmailSerializer(data=request.data)
		if serializer.is_valid():
			validated_data = serializer.validated_data

			user = User.objects.get(email=validated_data['email'])
			data_set = {'user': user}			
			queryset = History.get_search_history(data_set)			
			serialized_queryset = HistorySerializer(queryset, many=True)

			return Response(serialized_queryset.data, status=status.HTTP_200_OK)

		else:
			return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

	def get(self, request):
	
		user = User.objects.get(email='ad@ad.com')
		data_set = {'user': user}			
		queryset = History.get_search_history(data_set)
		serialized_queryset = HistorySerializer(queryset, many=True)
	
		return Response(serialized_queryset.data, status=status.HTTP_200_OK)
	


class Bookmark(APIView):
	'''
		User bookmark a searched drug in its history. 
	'''
	def post(self, request):
		# email, kor_name 
		serializer = BookmarkSerializer(data=request.data)
		if serializer.is_valid():

			validated_data = serializer.validated_data

			user = User.objects.get(email=validated_data['email'])
			drug = Drug.objects.get(kor_name=validated_data['kor_name'])

			data_set = {'user': user, 'drug': drug}			

			History.insert(data_set) # create! 

			return Response(serializer.data, status=status.HTTP_200_OK)
		else:			
			return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

	
