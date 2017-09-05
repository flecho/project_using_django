from django.db import models
from accounts.models import MyUser as User
from drugs.models import Drug

class History(models.Model):
	'''
		This model represents a relationship between a user and drugs that he/she searched. 
	'''

	user = models.ForeignKey(User, on_delete=models.CASCADE)
	drug = models.ForeignKey(Drug, on_delete=models.CASCADE)

	class Meta:
		unique_together = ('user', 'drug')

	# Think of which is better to use between staticmethod and classmethod.
	# Do these methods need to return something?
	
	@staticmethod
	def insert(validated_data):
		History.objects.create(user = validated_data['user'],
							   drug = validated_data['drug'])
	
	@staticmethod
	def delete(validated_data):
		History.objects.get(user = validated_data['user'],
							drug = validated_data['drug']).delete()

	@staticmethod
	def get_search_history(validated_data):
		queryset = History.objects.filter(user=validated_data['user']).select_related('drug').only('drug__kor_name', 'drug__eng_name', 'drug__ref_img').values('drug__kor_name', 'drug__eng_name', 'drug__ref_img')
		return queryset

#		join_result = queryset.select_related()
#	 	result_list = []
#
#		for i in len(join_result):
#			kor_name = join_result[i].drug.kor_name
#			eng_name = join_result[i].drug.eng_name
#			ref_img = join_result[i].drug.ref_img
#			temp_dic = {}
#			temp_dic['kor_name'] = kor_name
#			temp_dic['eng_name'] = eng_name
#			temp_dic['ref_name'] = ref_name
#			result_list.append(temp_dic)	
#		# dictionary로 만들어서, serialize해서 보내면 됨. 	
#
#		return result_list # list of dictionaries.
#		return queryset.select_related('drug').values('kor_name', 'eng_name', 'ref_img')




	'''
		[ select_related(*fields) ]
		Returns a QuerySet that will "follow" foreign-key relationships, selecting additional related-object data
		when it executes its query. This is a performance booster which results in a single more complex query but
		means later use of foreign-key relationships won't require database queries.

	'''


	'''
		ManyToManyField cannot be included in unique_together. 
		If you need to validate uniqueness related to a ManyToManyField, 
		try using a signal or an explicit rhough model.
	'''

	'''
		[ ForeignKey.to_field ]

		The field on the related object that the relation is to. 
		By default, Django uses the primary key of the related object. 
		If you reference a different field, that field must have unique=True.
	'''

	'''
		When an object referenced by a ForeignKey is deleted, Django will 
		emulate the behavior of the SQL constraint specified by the on_delete
		argument. 
	'''
