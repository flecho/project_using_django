#-*- coding:utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from drugs.models import Drug
from drugs.management.commands.drugcrawler import DrugCrawler
from urllib.parse import quote
import re
import io

# 일단 3
class Command(BaseCommand):
	help = "Populate each drug's character information"

	def add_arguments(self, parser):
		pass
		parser.add_argument('file_number', type=str, help='')

	def handle(self, *args, **options):
		'''	This function takes the number as an input, and populate drug information as many as that number '''

		file_number = options['file_number']	

		f = open('drugs/management/commands/parsing/d.txt', 'rt') # d.txt contains about 300 data.
		print(f.name)
		print(f.encoding)
		print(f.mode)

		# jpg/ 뒤에 string이 비어있는 경우 문제를 해결해야 함
		for row in f:
			key_name, char_set = re.findall('(.+).jpg/(.*)' , row)[0]			
			
#			for c in key:
#				print(ord(c))
#			try:
				# HStoreField로 바꿔야 함.
#				drug = Drug.objects.get(kor_name=key)
#				drug.imprint = char_set.split(',')
#				print(drug.imprint)
#				drug.save()
				
# list to dic 있으면 좋을 것 같은데,
			dict_keys = list(set(char_set.split(',')))
			new_dict = {}
			for key in dict_keys:
				new_dict[key] = str(char_set.count(key)) # HStoreField Value needs to be string. 

			print(new_dict)

			try:
				drug = Drug.objects.get(kor_name=key_name)
				drug.imprint = new_dict
				drug.save()
			except:
				print("A pill that does not exist: ", key_name)
