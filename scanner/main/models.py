from django.db import models

# Create your models here.

class UploadFile(models.Model):
	file = models.FileField(upload_to = 'files/%Y/%m/%d')

class Node(models.Model):
	sha1_id 	= models.CharField(max_length = 40)
	hotkey_info = models.CommaSeparatedIntegerField(max_length=200)


# Might not want to put this here
# Not actual a django model
class Player(object):
	def __init__(self, percent_match, sample_size, url, name):
		self.name = name
		self.confidence = percent_match
		self.url = url
		self.sample_size = sample_size

	def __lt__(self, other):
		# return self.confidence < other.confidence
		return self.sample_size < other.sample_size

	def __repr__(self):
		return self.url
