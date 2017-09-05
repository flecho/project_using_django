#-*- coding:utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
#from drugs.models import Drug
#from drugs.management.commands.drugcrawler import DrugCrawler
from urllib.parse import quote
import re
import io
	
from_file1 = open('d3.txt', 'rt')
from_file2 = open('c3.txt', 'rt')#, encoding="utf-8")
to_file = open('out.txt', 'wt')

helper_list = []

# jpg/ 뒤에 string이 비어있는 경우 문제를 해결해야 함

for line in from_file1:
	char_set = re.findall('.+.jpg/(.)*', line)[0]
	to_file.write(char_set + from_file2.readline())


#	for c in key:
#		print(ord(c))
#	for c in '저니스타서방정64mg':
#		print(ord(c))
#	return
#
#	try:
#		drug = Drug.objects.get(kor_name=key)
#		drug.imprinted_text = char_set.split(',')
##				drug.save()
#	except:
#		print("error")
#		continue
			


		# 조합형을 완성형으로 만들어야 되는 문제

#			char_dict[key] = char_set	
#		
#		for i, key in enumerate(char_dict.keys()):
#			print(i, key)
#			print(type(key))
#			try:
#				drug = Drug.objects.get(kor_name='트락손정25mg') 
#				drug.imprinted_text = char_dict[key].split(',')
#				break
#			except:
#				print("error")
#				continue
		
#		self.stdout.write(self.style.SUCCESS('Hoho!: %s' % number))

