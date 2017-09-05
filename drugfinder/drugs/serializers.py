#-*- coding:utf-8 -*-
from rest_framework import serializers
import PIL

class DrugSerializer(serializers.Serializer):
	kor_name = serializers.CharField(max_length=100)
	eng_name = serializers.CharField(max_length=100)
	color = serializers.CharField(max_length=100)
	shape = serializers.CharField(max_length=100)
	ref_img = serializers.CharField(max_length=200)
#	imprint = serializers.ListField(child=serializers.CharField(max_length=200))
	# imprint info is not necessary for the frontend.
	content = serializers.CharField() # serializer.CharField에서는 max_length 제한이 없음. 
	way_to_store = serializers.CharField() # At model.py, the corresponding field is TextField.
	effect = serializers.CharField()
	dosage = serializers.CharField()
	caution = serializers.CharField()

	# The data coming from external source must be deserialized, that's why the name of the parameter is validated_data
	
	def create(self, validated_data):
		''' Create and return a new `Drug` instance, given the validated data. '''
		return Drug.objects.create(**validated_data)

	def update(self, instance, validated_data):
		''' Update and return an existing `Drug` instance, given the validated data. '''
		instance.kor_name = validated_data.get('kor_name', instance.kor_name)
		instance.eng_name = validated_data.get('eng_name', instance.eng_name)
		instance.color = validated_data.get('color', instance.color)
		instance.shape = validated_data.get('shape', instance.shape)
		instance.ref_img = validated_data.get('ref_img', instance.ref_img)
		instance.imprint = validated_data.get('imprinted_text', instance.imprint)
		instance.content = validated_data.get('info', instance.content)
		instance.way_to_store = validated_data.get('way_to_store', instance.way_to_store)
		instance.effect = validated_data.get('effect', instance.effect)
		instance.dosage = validated_data.get('dosage', instance.dosage)
		instance.caution = validated_data.get('caution', instance.caution)

		instance.save()
		return instance

	# Now when deserializing data, we can call '.save()' to return an object instance, based on the validated data.

# Non Model serializer
class UserImageSerializer(serializers.Serializer):
	email = serializers.EmailField()
	image = serializers.ImageField()

class CandidateSerializer(serializers.Serializer):
	kor_name = serializers.CharField()
	eng_name = serializers.CharField()
	ref_img = serializers.CharField()

class UserSelectSerializer(serializers.Serializer):
	kor_name = serializers.CharField()


