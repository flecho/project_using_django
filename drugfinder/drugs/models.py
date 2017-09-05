#-*- coding:utf-8 -*-
from django.db import models
from django.contrib.postgres.fields import HStoreField

import boto3
import botocore
import cv2
from celery import shared_task
from PIL import Image
import tensorflow as tf

from .faster_rcnn.tools import inference

# Remember fat models, thin views...
# - maintainability
# - a model is much easier to test
# - reusable logic: form validation, signals, etc.
# - the code becomes clearer, more self-documenting

# naver health encyclopedia --> django postgre.
class Drug(models.Model):
	kor_name = models.CharField(max_length=100, primary_key=True)
	eng_name = models.CharField(max_length=100, default='', blank=True) # used to retrieve reference image.
	color = models.CharField(max_length=100, null=True)
	shape = models.CharField(max_length=100, null=True)
	ref_img = models.CharField(max_length=200, null=True)
	imprint = HStoreField(default={})
	content = models.TextField(null=True) # a large text field
	way_to_store = models.TextField(null=True)
	effect = models.TextField(null=True)
	dosage = models.TextField(null=True)
	caution = models.TextField(null=True)

	load_flag = False
	sess = None
	net = None

	def __str__(self):
		return self.kor_name

	@staticmethod
	def search(key_list):
		''' This function gets a list of input and output a QuerySet which is
			the result of searching. '''
		MAX_CANDIDATES = 10
		queryset = Drug.objects.none()

		# If CNN didn't extract any characters, return empty QuerySet.
		if not key_list:
			return queryset
		
		key_dic = Drug.list_to_dic(key_list)		
		queryset = Drug.get_queryset_with_all_keys(key_dic)

		# QuerySet이 empty list일 때 
		if not queryset.exists():
			return queryset

		if queryset.count() > 10:
			queryset = queryset[:MAX_CANDIDATES]

		return queryset.values('kor_name', 'eng_name', 'ref_img')

	@staticmethod
	def get_queryset_with_all_keys(input_dic):
		''' This function returns a list of drug candidates that contain every
			character recognized thorugh CNN. '''
		keys = list(input_dic.keys())
		return Drug.objects.filter(imprint__has_keys=keys) # .values('kor_name', 'eng_name', 'ref_img')


	@staticmethod
	def list_to_dic(input_list):
		'''	This function removes duplicate elements of the input_list and make dictionary 
			by using those elements as keys. '''
		no_dup_list = list(set(input_list))
		result_dic = {}

		for key in no_dup_list:
			result_dic[key] = input_list.count(key)

		return result_dic


	@staticmethod
	@shared_task
	def evaluate(image_name):
		''' Tensorflow code. An image is received as an input, and it returns
			a list of characters detected through faster-RCNN.
		'''

		image = cv2.imread('temp_storage/' + image_name)

		if not Drug.load_flag: 
			Drug.sess, Drug.net = inference.load_network('/home/ubuntu/user_management/drugfinder/drugs/faster_rcnn/VGGnet_fast_rcnn_iter_140K.ckpt', 'VGGnet_test')		
			Drug.load_flag = True

		scores, boxes, det_results = inference.inference(Drug.sess, Drug.net, image)

		return det_results


	@staticmethod
	@shared_task
	def upload_to_s3():
		''' This function uploads an image to s3 storage.
			The job must be proceeded as a background job. '''
		image = open('temp_storage/' + image_name, "rb") 	
		s3 = boto3.resource('s3')
	
		if s3.Bucket('posimg') not in list(s3.buckets.all()): 
			s3.create_bucket(Bucket='posimg', CreateBucketConfiguration={'LocationConstraint': 'ap-northeast-2'})
			'''NOTE: Check whether your Bucket name already exists or not.'''
	
		s3.Object('posimg', email + '/' + image_name).put(Body=image)

	

#========================= Tips =============================#
'''
	1. Avoid using null on string-based fields such as CharField and TextField. If a string-based field has null=True,
	that means it has two possible values for "no data": NULL, and the empty string.
		In most cases, it's redundant to have two possible values for "no data;" the Django convention is to use the empty
	string, not NULL.
	2. 
'''


'''
		Once you've created your data models, Django automatically gives you a database-abstraction API that lets you 
	create, retrieve, update and delete objects. This document explains how to use this API. Refer to the data model reference
	for full details of all the various model lookup options. 
'''


#========================= Code past =============================#
'''
def search(chars):
	# If CNN didn't extract any characters, return empty QuerySet.
	if not chars:
		return Drug.objects.none()		

	length = len(chars)
	result_set = Drug.objects.none() # creating empty queryset.

	# - SearchResult is restricted to 10 entities.
	# - Later, classification using color/shape might be added.  

	query_set = get_query_sets(chars) # QuerySet
	result_set = result_set.union(query_set) # If exists, best case. 

	# If it doesn't exist, 
	if length <= 1:
		return result_set

	candidates_set_a = itertools.combinations(chars, length-1)
	for cand in candidates_set_a:
		result_set = result_set.union(get_query_sets(list(cand)))
		if len(result_set) > CANDIDATES_MAX:
			result_set = result_set[:CANDIDATES_MAX]
			return result_set

	return result_set

	if length <=2:
		return result_set

	candidates_set_b = itertools.combinations(chars, length-2)
	for cand in candidates_set_b:
		result_set = result_set.union(get_query_sets(list(cand)))
		if len(result_set) > CANDIDATES_MAX:
			result_set = result_set[:CANDIDATES_MAX]
			return result_set
	

	# 종결조건 result_set의 길이가 7개를 넘었을 때 
	# 인식된 글자에서 2개까지 뺀 combination까지 다 계산했을 때
def get_query_sets(characters):
	#This function returns a Query Set.	
	# 여기서 중복 characters를 인식할 수 있는 로직이 필요함.
	return Drug.objects.filter(imprint__contains=characters).values('kor_name', 'eng_name', 'ref_img')
	# list of columns that are exposed when user sent an image.
'''
