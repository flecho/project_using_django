#-*- coding:utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
#import sys
#print(sys.path)
from drugs.models import Drug
from drugs.management.commands.drugcrawler import DrugCrawler
import tqdm
from urllib.parse import quote

BASE_URL = 'http://terms.naver.com'
S3_REF_IMG_BUCKET_URL = 'https://s3.ap-northeast-2.amazonaws.com/refimg/'


class Command(BaseCommand):
	help = 'Populate the database with crawled drug data'

	def add_arguments(self, parser):
		parser.add_argument('start_index', type=int, help='type non-negative start index')
		parser.add_argument('end_index', type=int, help='type non-negative end index')

	def handle(self, *args, **options):
		'''	This function takes the number as an input, and populate drug information as many as that number '''

		start = options['start_index']
		end = options['end_index']
		if start >= 0 and end > start:
			f = open('drugs/management/commands/new_urls.txt', 'r')
			urls = f.read().split(',')[start:end]

			for url in tqdm.tqdm(urls):
				url = BASE_URL + url
				data_dic = DrugCrawler().obtain_data(url)
				# 'obtain_data' is a very important function. 
				# To create and save an object in a single step, use the create() method.
				Drug.objects.create(kor_name=data_dic['kor_name'],
									eng_name=data_dic['eng_name'],
									ref_img= S3_REF_IMG_BUCKET_URL + quote(data_dic['kor_name']) + ".jpg",
									content=data_dic['content'],
									way_to_store=data_dic['way_to_store'],
									effect=data_dic['effect'],
									dosage=data_dic['dosage'],
									caution=data_dic['caution']
				)

				# color, shape, imprinted_text는 나중에 update.
		else:
			self.stdout.write(self.style.SUCCESS('Populating the data has failed!: %s' % number))
		
	
