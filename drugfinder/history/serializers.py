#-*- coding:utf-8 -*-
from rest_framework import serializers

class EmailSerializer(serializers.Serializer):
	email = serializers.EmailField()

class BookmarkSerializer(serializers.Serializer):	
	email = serializers.EmailField()
	kor_name = serializers.CharField()

class HistorySerializer(serializers.Serializer):
	kor_name = serializers.CharField(source='drug__kor_name')
	eng_name = serializers.CharField(source='drug__eng_name')
	ref_img = serializers.CharField(source='drug__ref_img')
