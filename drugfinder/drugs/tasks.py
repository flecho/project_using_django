from celery import Task
from celery import shared_task
import boto3, botocore

class UploadToS3(Task):

	def __init__(self, *args, **kwargs):
		self.email = kwargs.get('email', None)
		self.image = kwargs.get('image', None)
		
	# Main entry
	def run(self, *args, **kwargs):
		self.upload(self.email, self.image)

#	def bind(self, app):
#		return super(self.__class__, self).bind(celery_app)

	def upload():
		s3 = boto3.resource('s3')

		if s3.Bucket('posimg') not in list(s3.buckets.all()): 
			s3.create_bucket(Bucket='posimg', CreateBucketConfiguration={'LocationConstraint': 'ap-northeast-2'})
		'CAUTION: the bucket name must be unique in the region your s3 belongs to.'

		# Upload to s3 storage
		s3.Object('posimg', email + '/' + image.name).put(Body=image)	


@shared_task				
def upload_to_s3(email, image):

	s3 = boto3.resource('s3')

	if s3.Bucket('posimg') not in list(s3.buckets.all()): 
		s3.create_bucket(Bucket='posimg', CreateBucketConfiguration={'LocationConstraint': 'ap-northeast-2'})
	'CAUTION: the bucket name must be unique in the region your s3 belongs to.'

	# Upload to s3 storage
	s3.Object('posimg', email + '/' + image.name).put(Body=image)
