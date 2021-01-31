from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Login_User(models.Model):
	''' Demonstrate docstring for storing User personal information'''
	username = models.ForeignKey(User, on_delete = models.CASCADE)
	first_name = models.CharField(max_length = 200)
	last_name = models.CharField(max_length = 200, blank = True, null = True)
	phone_number = models.BigIntegerField(null = True)
	email = models.CharField(max_length = 300, blank = True, null = True)
	role = models.CharField(max_length = 200, blank = True, null = True)
	time_stamp = models.DateTimeField(auto_now = True)
	email_query_code = models.CharField(max_length = 200, blank = True , null = True)
	email_verification_check = models.BooleanField(default = False)
	normal_login = models.BooleanField(default = False)
	gmail_login = models.BooleanField(default = False)
	facebook_login = models.BooleanField(default = False)
	continue_with_email = models.BooleanField(default = False)
	uid = models.CharField(max_length = 500, blank = True, null = True)

	def __str__(self):
		return (str(self.username)+'  --  '+str(self.id))


class Password_Reset(models.Model):
	''' Demonstrate docstring for storing User personal information'''
	username = models.ForeignKey(User, on_delete = models.CASCADE)
	verification_code = models.CharField(max_length = 20)
	created_at = models.DateTimeField(auto_now = True)

	def __str__(self):
		return str(self.username)

class Folder(models.Model):
	creator = models.ForeignKey(Login_User, on_delete = models.CASCADE, blank = True, null = True)
	name = models.CharField(max_length = 200)
	recent_date = models.DateTimeField(blank = True, null = True)
	description = models.TextField(blank = True, null = True)
	created_at = models.DateTimeField(auto_now = True)

	def __str__(self):
		return str(self.name)


class SetTable(models.Model):
	creator = models.ForeignKey(Login_User, on_delete = models.CASCADE, blank = True, null = True)
	folder = models.ForeignKey(Folder, on_delete = models.CASCADE, blank = True, null = True)
	name = models.CharField(max_length = 200)
	recent_date = models.DateTimeField(blank=True, null=True)
	description = models.TextField(blank = True, null = True)
	created_at = models.DateTimeField(auto_now = True)

	def __str__(self):
		return str(self.name)

class Category(models.Model):
	''' Demonstrate docstring for storing category related information '''
	name = models.CharField(max_length = 200)
	description = models.TextField(blank = True, null = True)
	image = models.FileField(null = True, blank = True)
	folder = models.ForeignKey(Folder, on_delete = models.CASCADE)
	settbl = models.ForeignKey(SetTable, on_delete = models.CASCADE)
	recent_date = models.DateTimeField(blank=True, null=True)
	creator = models.ForeignKey(Login_User, on_delete = models.CASCADE, blank = True, null = True)
	time_stamp = models.DateTimeField(auto_now = True)

	def __str__(self):
		return str(self.name)

class CardContent(models.Model):
	category = models.ForeignKey(Category, on_delete = models.CASCADE)
	question = models.TextField()
	answer = models.TextField()
	hint = models.TextField(blank = True, null = True)
	recent_date = models.DateTimeField(blank=True, null=True)
	question_file_path = models.CharField(max_length = 1000, blank = True, null = True)
	answer_file_path = models.CharField(max_length = 1000, blank = True, null = True)
	hint_file_path = models.CharField(max_length = 1000, blank = True, null = True)
	created_at = models.DateTimeField(auto_now = True)

	def __str__(self):
		return str(self.question)

class UserVoiceInput(models.Model):
	cc = models.ForeignKey(CardContent, on_delete = models.CASCADE, blank = True, null = True)
	voice_input = models.FileField(blank=True, null=True)
	created_at = models.DateTimeField(auto_now = True)

	def __str__(self):
		return str(self.id)


class ReportResult(models.Model):
	category = models.ForeignKey(Category, on_delete = models.CASCADE)
	user = models.ForeignKey(Login_User, on_delete = models.CASCADE, blank = True, null = True)
	test_data = models.TextField(blank = True, null = True)
	percentage = models.FloatField(default = 0.0)
	created_at = models.DateTimeField(auto_now = True)

	def __str__(self):
		return (str(self.created_at)+'----'+str(self.user)+'  -- '+str(self.percentage))
		