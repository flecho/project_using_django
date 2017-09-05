#-*- coding:utf-8 -*-
import urllib.request
from bs4 import BeautifulSoup
import ssl
import re
import boto3, botocore
from drugs.models import Drug

# This code should be reformed into OOP style.


class DrugCrawler(object):

	'''
		Variables set outside __init__ belong to the class. They're shared by all instances. 
		Variables created inside __init__(and all other method functions) prefaced with self. belong to the object instance. 
	'''

	def __init__(self):
		self.drug_info = {}

	def obtain_data(self, url):
		'''	This function returns a dictionary that contains all the crawled information, and
			save the reference image at the same time to the S3 storage server. '''

		# Ignore SSL certificate errors
		ctx = ssl.create_default_context()
		ctx.check_hostname = False
		ctx.verify_mode = ssl.CERT_NONE

		html = urllib.request.urlopen(url, context=ctx).read() # read entire documents into a single big string.
		soup = BeautifulSoup(html, 'html.parser')
	
		kor_name_tag = soup.find('title')
		eng_name_tag = soup.find("p", class_='word')
		p_txt_tags = soup("p", class_="txt")
		span_tags = soup.find("span", class_="img_box")

		self.record_kor_name(kor_name_tag)
		self.record_eng_name(eng_name_tag)
		self.record_p_txt_tags(p_txt_tags)

		if span_tags:
			img_addr = span_tags.img['data-src']
			self.send_img_to_s3(img_addr) # If there exists a reference img, it is stored in S3 storage.

		return self.drug_info
		
	def record_kor_name(self, tag):
		if tag:
			self.drug_info['kor_name'] = str(tag.text).replace('/', ' ')
		else:
			self.drug_info['kor_name'] = '' # In case there is no information, return an empty string.
	
	def record_eng_name(self, tag):
		eng_name = str(tag.string)
		search_result = re.findall('\[(.+)\]', eng_name)

		if not search_result:
			self.drug_info['eng_name'] = ''
		else:
			self.drug_info['eng_name'] = search_result[0].strip().replace('/', ' ')
	
	def record_p_txt_tags(self, tags):
		''' Get contents out of beautifulsoup object and put them into dictionary.'''
		pattern = re.compile('"\s*txt\s*"\s*>\s*(.+)<\s*/\s*p\s*>', re.MULTILINE)
		for i, tag in enumerate(tags):
			parsed_tag = str(tag).replace('\n', '') # unnecessary new line hampers parsing html file.
			matched_list = re.findall(pattern, parsed_tag)
	
			if not matched_list:
				continue
	
			temp_string = re.findall(pattern, parsed_tag)[0].replace('<br/>', '\n')
	
			if i == 0:
				self.drug_info['shape'] = self.remove_inner_tags(temp_string)
			elif i == 1:
				self.drug_info['content'] = self.remove_inner_tags(temp_string)
			elif i == 2:
				self.drug_info['way_to_store'] = self.remove_inner_tags(temp_string)
			elif i == 3:
				self.drug_info['effect'] = self.remove_inner_tags(temp_string)
			elif i == 4:
				self.drug_info['dosage'] = self.remove_inner_tags(temp_string)
			else: # 5
				self.drug_info['caution'] = self.remove_inner_tags(temp_string)
				break

	def remove_anchor_tags(remove_inner_tags):
		''' Remove anchor tags that are contained in the string and return it. '''
		def func(self, *args, **kwargs):
			string = args[0]
			anchor_tags = re.findall('<\s*a\s*\href\s*=.+>.+<\s*/\s*a\s*>', string)
			# if there is no anchor tags, the following loop is not to be executed.
			for anchor_tag in anchor_tags:
				string = string.replace(anchor_tag, re.findall('<\s*a\s*\href\s*=.+>(.+)<\s*/\s*a\s*>', anchor_tag)[0])
			return remove_inner_tags(self, string)
		return func
	
	@remove_anchor_tags
	def remove_inner_tags(self, string):
		''' Remove_anchor_tag function should precede remove_inner_tags function. '''
		parsed = re.sub('<\s*[a-zA-Z/]*\s*>', '', string)
		return parsed

	def send_img_to_s3(self, img_addr):
		if img_addr:
			temp, _ = urllib.request.urlretrieve(img_addr)
			s3 = boto3.resource('s3')

			print(list(s3.buckets.all()))
			if s3.Bucket('refimg') not in s3.buckets.all():
				s3.create_bucket(Bucket='refimg', CreateBucketConfiguration={'LocationConstraint': 'ap-northeast-2'})

			s3.Bucket('refimg').put_object(Key=self.drug_info['kor_name'] + '.jpg', Body=open(temp, 'rb'))
		else:
			print("Sending an image has failed.")

	def print_drug_info(self):
		fields = ['kor_name', 'eng_name', 'shape', 'content', 'way_to_store', 'effect', 'dosagee' 'caution']
		for field in fields:
			print(field + ': ' + self.drug_info[field])



'''
	# Successful Download 
	print(drug_info_dict['kor_name'])
	#print_drug_info_dict(drug_info_dict)
	s3 = boto3.resource('s3')
	bucket_name = 'refimg'
	key = drug_info_dict['kor_name'] + '.jpg'
	try:
		s3.Bucket(bucket_name).download_file(key, key)
	except botocore.exceptions.ClientError as e:
		if e.response['Error']['Code'] == "404":
			print("The object does not exist.")
		else:
			raise	
'''


