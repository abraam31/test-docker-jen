import wave
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth import authenticate
from .serial import *
from django.contrib.auth.models import User
from .models import *
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
import random
import string
import os
import time
import smtplib
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTPException
from email.message import EmailMessage
from django.conf import settings
from gtts import gTTS
import speech_recognition as sr
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from django.conf import settings
from django.core.mail import send_mail
from random import choice
from string import ascii_uppercase
import logging
from django.core.mail import EmailMessage
import re

# Create your views here.


class Register(APIView):
  '''API for registration'''
  permission_classes = (AllowAny,)

  def post(self, request):
    data = request.data
    serializer = Login_UserSerializer(data=data)
    phone_number = data.get('phone_number')
    username = data.get('email')
    password = data.get('password')
    # email = data.get('email')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    role = data.get('role')

    if not username:
      # Email as username is required
      return Response({'code': 400, 'message': 'Enter the valid email..'})

    email_query_code = ''.join(
        [random.choice(string.ascii_letters + string.digits) for n in range(8)])
    if not role:
      role = 'user'
    user_check = User.objects.filter(username=username)
    if user_check:
      # Checking if user already exist or not.
      return Response({'code': 400, 'message': 'User Already exists.'})

    if phone_number:
      # PhoneNumer Validations
      try:
        int(phone_number)
        pass
      except Exception as e:
        return Response({'code': 400, 'message': 'Phone number should be numeric.'})
    else:
      return Response({'code': 400, 'message': 'Enter Phone No.'})

    if first_name:
      # FirstName Validations
      if len(first_name) > 200:
        return Response({'code': 400, 'message': 'Max Length for First name is 200.'})
      else:
        pass
    else:
      return Response({'code': 400, 'message': 'Enter First Name.'})

    if serializer.is_valid():
      user = User.objects.create(username=username)
      user.set_password(password)
      user.save()
      try:
        if username is None:
          pass
        else:
          user.email = username
          user.save()
      except Exception as e:
        pass

      try:
        login_user = Login_User(username_id=user.id, first_name=str(first_name), last_name=last_name,
                                phone_number=phone_number, email=username, role=role, email_query_code=email_query_code)
        login_user.save()
        token, status = Token.objects.get_or_create(user=user)
        login_user.normal_login = True
        login_user.save()
        return Response({'code': 200, 'message': 'Login Successful', 'token': token.key, 'login_user_id': login_user.id, 'first_name': login_user.first_name, 'last_name': login_user.last_name, 'role': login_user.role})

      except Exception as error:
        return Response({'code': 400, 'message': 'Something went wrong.', 'error': str(error)})

    return JsonResponse(serializer.errors, status=400)


class EmailVerification(APIView):
  '''API for email verification to complete the registration process'''

  permission_classes = (AllowAny,)

  def get(self, request):
    pass
# 		email_query_code = request.GET.get('query')
# 		print(email_query_code)
# 		username = request.GET.get('u')

# 		user_name_check = User.objects.filter(username = username).first()
# 		if not user_name_check:
# 			return Response({'code' : 400, 'message' : 'Invalid Username.'})
# 		else:
# 			user_login_info_check = Login_User.objects.filter(username_id = int(user_name_check.id) ,email_query_code = email_query_code).first()
# 			if not user_login_info_check:
# 				return Response({'code' : 400 ,'message' : 'Invalid parameters.'})
# 			else:
# 				user_login_info_check.email_verification_check = True
# 				user_login_info_check.save()
# 				user_login_info_check.normal_login = True
# 				user_login_info_check.save()
# 				return Response({'code' : 200, 'messsage' : 'Email has been verified.'})


class SocialPlatformLogin(APIView):
  permission_classes = (AllowAny,)

  def post(self, request):
    username = request.POST.get('email')
    name = request.POST.get('name')
    uid = request.POST.get('uid')
    login_type = request.POST.get('type')

    if not username:
      return Response({'code': 400, 'message': 'Please send the email'})

    if not login_type:
      return Response({'code': 400, 'message': 'Please send the login_type'})

    user_check = User.objects.filter(username=username).first()

    if user_check:
      # user is already registered and verifying and getting person_id
      user_login_info_check = Login_User.objects.filter(
          username_id=int(user_check.id)).first()
      if user_login_info_check:
        if user_login_info_check.normal_login == False:
          user_check.set_password(uid)
          user_check.save()
          try:
            user = authenticate(username=username, password=uid)
            if user:
              token, status = Token.objects.get_or_create(user=user)
              print('token_id', token.key)

          except Exception as error:
            print('Error is :', error)
            pass

        # user_login_info_check.email_verification_check = True

        if login_type == 'gmail':
          user_login_info_check.gmail_login = True

        if login_type == 'facebook':
          user_login_info_check.facebook_login = True

        if login_type == 'continue_with_email':
          last_name = request.POST.get('last_name')
          if last_name:
            user_login_info_check.last_name = last_name
          user_login_info_check.continue_with_email = True

        if user_login_info_check.normal_login == False:
          user_check.set_password(uid)
          user_check.save()

        user_login_info_check.save()

        return Response({'code': 200, 'message': 'Login Successful', 'token': token.key, 'login_user_id': user_login_info_check.id, 'username': user_login_info_check.email, 'role': user_login_info_check.role})
      else:
        return Response({'code': 400, 'message': 'Something went wrong.'})

    else:
      # Creating new user regiteration as person is logged in for first time with socialplatform APIs.
      user = User.objects.create(username=username)
      user.set_password(uid)
      user.save()
      try:
        if username is None:
          pass
        else:
          user.email = username
          user.save()
      except Exception as e:
        print('errr', e)
        pass
      # login_user = Login_User(username_id = user.id, first_name = str(first_name), last_name = last_name, phone_number = phone_number, email = email ,role = role, email_query_code = email_query_code)
      if not name:
        name = ' '
      login_user = Login_User.objects.create(username_id=user.id, email=str(
          username), first_name=str(name), role='user', uid=uid)
      # login_user.email_verification_check = True
      if login_type == 'gmail':
        login_user.gmail_login = True

      if login_type == 'facebook':
        login_user.facebook_login = True

      if login_type == 'continue_with_email':
        last_name = request.POST.get('last_name')
        login_user.last_name = last_name
        login_user.continue_with_email = True

      login_user.save()

      user = authenticate(username=username, password=uid)
      if user:
        try:
          token, status = Token.objects.get_or_create(user=user)
          print('token_id :', token.key)
        except Exception as error:
          print('Error is :', error)
          pass

      return Response({'code': 200, 'message': 'Login Successful', 'token': token.key, 'login_user_id': login_user.id, 'username': login_user.email, 'first_name': login_user.first_name, 'role': login_user.role, 'last_name': login_user.last_name})


class Login(APIView):
  '''API for User Login'''
  permission_classes = (AllowAny,)

  def post(self, request):
    username = request.POST.get('user_name')
    password = request.POST.get('password')
    role = request.POST.get('role')
    user = authenticate(username=username, password=password)
    # user authentication to check it password and username match exists or not.
    if user:
      login_user = Login_User.objects.filter(
          username_id=user.id, role=role).first()
      if login_user:
        # if login_user.email_verification_check == False:
        # 	return Response({'code' : 400,'message' : 'Email has not been verified.'})
        # else:
        token, status = Token.objects.get_or_create(user=user)
        login_user.normal_login = True
        login_user.save()
        return Response({'code': 200, 'message': 'Login Successful', 'token': token.key, 'login_user_id': login_user.id, 'first_name': login_user.first_name, 'last_name': login_user.last_name, 'role': login_user.role})
      else:
        return Response({'code': 400, 'message': 'User Credentials were incorrect..'})
    else:
      return Response({'code': 400, 'message': 'User Credentials were incorrect.'})


class ForgotPassword(APIView):
  '''API for email verification to complete the registration process'''

  permission_classes = (AllowAny,)

  def get(self, request):
    email_id = request.GET.get('email_id')
    code = 200
    message = ''
    if not email_id:
      code = 400
      message = 'Email-ID not present.'

    try:
      user_name_check = User.objects.get(email=email_id)
      random_string = ''.join(choice(ascii_uppercase) for _ in range(6))
      t_message = ' <table border="0" cellpadding="0" cellspacing="0" style="width: 100%;margin:0 auto;padding: 35px;"><tr><td><table cellpadding="0" cellspacing="0" align="center" style="background: #fff;border-collapse:collapse;text-align: center;border-top: 4px solid #fd5353; padding: 10px;background: #fff;width: 550px;"><tr><td class="td-pad-20" style="padding:20px 0px 9px 0px;border-bottom: 1px solid #f9f9f9;" valign="top" align="center"><span style="display:block;"><img src="https://letsflash.co/images/logo.png" width="150px"> </span></td></tr><tr><td><h6 style="font-family: "Roboto Slab";serif;font-size:25px;margin-bottom: 22px;margin-top:20px; color:#fd5353;">Reset Password</h6></td></tr><tr><td style="text-align: center;"><span style="display:block;margin-bottom:5px;font-family: "Open Sans", sans-serif;font-weight: 600;">Your Password has been Reset.</span><span style="display:block;margin-bottom:5px;font-family: "Open Sans", sans-serif;, Arial, sans-serif;font-size: 14px;line-height: 32px;"> Your Password Reset Link is  <a href="https://letsflash.co/reset_password/'+email_id+'" target="_blank" style="color:#FD5353;text-decoration:none;"> https://letsflash.co/reset_password/' + \
          email_id+'</a></span></td></tr><tr><td style="text-align: center;" height="70"><span  style="display:block;font-family: "Open Sans", sans-serif;, Arial, sans-serif;"> Your Verfication Code is <a href="#" style="background-color:#fd5353;color: #fff;width: 100px;padding: 13px 27px;text-decoration: none;text-transform: capitalize;font-family: "Open Sans", sans-serif; font-weight: 700;/*! margin-top: 68px; */font-size: 16px;border-radius: 13px;margin-left: 8px;">'+random_string + \
          '</a></span></td></tr><tr><td><table width="550" cellpadding="0" cellspacing="0" align="center" style="border-collapse:collapse;font-family: "Raleway", Helvetica, Arial, sans-serif; mso-table-lspace:0pt; mso-table-rspace:0pt;background: #fff; margin-top: 30px;border-top:1px solid #f4f4f4;"><tr><td><table width="450" align="center" border="0" cellpadding="0" cellspacing="0" style="border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt; font-size:10px;"><tr><td  style="text-align: center;"><span  style="color: #1D2331;font-family: "Open Sans", sans-serif;font-size:13px;text-transform: capitalize;line-height:41px;">© 2020 flash®. </span></td></tr></table></td></tr></table></td></tr></table></td></tr></table>'
      email = EmailMessage('Password Reset', t_message,
                           settings.EMAIL_HOST_USER, [email_id])
      email.content_subtype = "html"
      res = email.send()

      Password_Reset.objects.filter(username=user_name_check).delete()
      password_verification_obj = Password_Reset(
          username=user_name_check, verification_code=random_string)
      password_verification_obj.save()

      message = 'Password reset links has been sent to your email.'
    except Exception as e:
      code = 400
      message = 'Email not exist'
      print('error is  : ', e)
    return Response({'code': code, 'message': message})

  def post(self, request):
    email_id = request.POST.get('email_id')
    verification_code = request.POST.get('verification_code')
    new_password = request.POST.get('new_password')

    code = 200
    message = ''

    if not email_id or not verification_code or not new_password:
      code = 400
      message = 'Email-ID/Verification-code/Password is not present.'
    try:
      user_name_check = User.objects.get(email=email_id)
      password_reset_obj = Password_Reset.objects.filter(
          username=user_name_check, verification_code=verification_code).last()

      print('password_reset_obj : ', password_reset_obj)

      if password_reset_obj:
        code = 200
        user_name_check.set_password(new_password)
        user_name_check.save()
        message = 'Password changed.'
        password_reset_obj.delete()
      else:
        code = 400
        message = 'Verification code is not matched.'

    except Exception as e:
      code = 400
      message = 'Account is not registered with this email.'
      print('error is  : ', e)

    return Response({'code': code, 'message': message})


class CategoryInfo(APIView):
  '''API for creating,fetching,editing and deleting Categories'''
  permission_classes = (AllowAny,)

  def get(self, request):
    '''Getting all the category info of existing categories'''
    categories_data = []
    category_id = request.GET.get('category_id')
    login_user_id = request.GET.get('user_id')
    role = request.GET.get('role')

    folder_id = request.GET.get('folder_id')
    settbl_id = request.GET.get('set_id')

    if category_id:
      try:
        category_obj = Category.objects.get(id=category_id)
        category_info = {}
        category_info['name'] = category_obj.name
        category_info['description'] = category_obj.description
        category_info['category_id'] = category_obj.id
        category_info['folder_id'] = category_obj.folder.id
        category_info['set_id'] = category_obj.settbl.id
        category_info['role'] = category_obj.creator.role
        category_info['user_id'] = category_obj.creator.id
        category_info['recent_date'] = category_obj.recent_date
        if category_obj.image:
          category_info['image'] = category_obj.image.name
        return Response({'code': 200, 'message': 'Succesfully fetched.', 'data': category_info})
      except Exception as e:
        return Response({'code': 400, 'message': 'Something went wrong.', 'data': categories_data})

    if folder_id and settbl_id:
      existing_all_categoires = Category.objects.filter(
          folder_id=int(folder_id), settbl_id=int(settbl_id))
    elif folder_id:
      existing_all_categoires = Category.objects.filter(
          folder_id=int(folder_id))
    elif settbl_id:
      existing_all_categoires = Category.objects.filter(
          settbl_id=int(settbl_id))
    else:
      existing_all_categoires = Category.objects.all()

    if existing_all_categoires:
      for category in existing_all_categoires:
        category_info = {}
        category_info['name'] = category.name
        category_info['description'] = category.description
        category_info['category_id'] = category.id
        category_info['folder_id'] = category.folder.id
        category_info['set_id'] = category.settbl.id
        category_info['role'] = category.creator.role
        category_info['recent_date'] = category.recent_date
        if category.creator:
          category_info['user_id'] = category.creator.id
        if category.image:
          category_info['image'] = category.image.name

        categories_data.append(category_info)

      return Response({'code': 200, 'message': 'Succesfully fetched.', 'data': categories_data})
    else:
      return Response({'code': 200, 'message': 'No data found.', 'data': categories_data})

    if category_id:
      existing_all_categoires = Category.objects.filter(id=int(category_id))
      if not existing_all_categoires:
        return Response({'code': 400, 'message': 'Invalid category id.'})
    elif login_user_id:
      existing_all_categoires = Category.objects.filter(
          creator_id=int(login_user_id), creator__role=str(role))
      if not existing_all_categoires:
        return Response({'code': 400, 'message': 'Invalid person id.'})

    else:
      existing_all_categoires = Category.objects.all()

  def post(self, request):
    '''For creating the categpry.'''
    name = request.POST.get('name')
    description = request.POST.get('description')
    folder_id = request.POST.get('folder_id')
    settbl_id = request.POST.get('set_id')
    login_user_id = request.POST.get('user_id')
    if not name:
      # Category name validation
      return Response({'code': 400, 'message': 'Please enter the name of category.'})
    if not login_user_id:
      return Response({'code': 400, 'message': 'Send the user id.'})

    # check_obj = Category.objects.filter(name = str(name)).first()
    # # Checking if any category exist with the same name or not.
    # if check_obj:
    # 	return Response({'code' : 400, 'message' : 'This category name already exists.'})

    try:
      if request.FILES:
        # for image file in request.FILES
        image = request.FILES['image']

        category_with_image = Category.objects.create(name=name, description=description, image=image, creator_id=int(
            login_user_id), folder_id=folder_id, settbl_id=settbl_id, recent_date=timezone.now())
        category_with_image.save()
        return Response({'code': 200, 'message': 'Succesfully saved.'})
      else:
        category_without_image = Category.objects.create(name=name, description=description, creator_id=int(
            login_user_id), folder_id=folder_id, settbl_id=settbl_id, recent_date=timezone.now())
        category_without_image.save()
        return Response({'code': 200, 'message': 'Succesfully saved.'})
    except Exception as error:
      return Response({'code': 400, 'message': 'Something went wrong.', 'error': str(error)})

  def put(self, request):
    ''' For update the existing categories '''
    category_name = request.POST.get('name')
    category_description = request.POST.get('description')

    category_id = request.POST.get('category_id')
    name = request.POST.get('name')
    description = request.POST.get('description')
    folder_id = request.POST.get('folder_id')
    settbl_id = request.POST.get('set_id')

    if not category_id:
      return Response({'code': 400, 'message': 'Invalid category id.'})
    else:
      category_to_update = Category.objects.filter(id=int(category_id)).first()
      if category_to_update:
        category_to_update.name = name
        category_to_update.description = description
        category_to_update.folder_id = folder_id
        category_to_update.settbl_id = settbl_id
        category_to_update.recent_date = timezone.now()
        category_to_update.save()

        return Response({'code': 200, 'message': 'Category Information updated.'})
      else:
        return Response({'code': 400, 'message': 'Invalid category id.'})

  def delete(self, request):
    ''' For deleting the exsiting category. '''
    category_id = request.GET.get('category_id')
    if not category_id:
      return Response({'code': 400, 'message': 'Enter the category id.'})
    else:
      category_to_be_deleted = Category.objects.filter(
          id=int(category_id)).first()
      if category_to_be_deleted:
        category_to_be_deleted.delete()
        return Response({'code': 200, 'message': 'Successfully deleted.'})
      else:
        return Response({'code': 400, 'message': 'Invalid Category id.'})


class CardContentInfo(APIView):
  '''API for creating,fetching,editing and deleting Categories'''
  permission_classes = (AllowAny,)

  def get(self, request):
    '''Getting all the category info of existing categories'''
    card_content_data = []
    category_id = request.GET.get('category_id')
    card_content_id = request.GET.get('card_content_id')

    if card_content_id:
      try:
        card_info_obj = CardContent.objects.get(id=card_content_id)
        card_info = {}
        card_info['card_content_id'] = card_info_obj.id
        card_info['category_id'] = card_info_obj.category.id
        card_info['question'] = card_info_obj.question
        card_info['answer'] = card_info_obj.answer
        card_info['hint'] = card_info_obj.hint
        card_info['recent_date'] = card_info_obj.recent_date
        card_info['question_file_path'] = card_info_obj.question_file_path
        card_info['answer_file_path'] = card_info_obj.answer_file_path
        card_info['hint_file_path'] = card_info_obj.hint_file_path
        return Response({'code': 200, 'message': 'Succesfully fetched.', 'data': card_info})
      except Exception as e:
        print('error is : ', e)
        return Response({'code': 200, 'message': 'No data found', 'data': {}})
    if category_id:
      card_info_obj = CardContent.objects.filter(category_id=category_id)
    else:
      card_info_obj = CardContent.objects.all()

    if card_info_obj:
      for card_obj in card_info_obj:
        card_info = {}
        card_info['card_content_id'] = card_obj.id
        card_info['category_id'] = card_obj.category.id
        card_info['question'] = card_obj.question
        card_info['answer'] = card_obj.answer
        card_info['hint'] = card_obj.hint
        card_info['recent_date'] = card_obj.recent_date
        card_info['question_file_path'] = card_obj.question_file_path
        card_info['answer_file_path'] = card_obj.answer_file_path
        card_info['hint_file_path'] = card_obj.hint_file_path

        card_content_data.append(card_info)

      return Response({'code': 200, 'message': 'Succesfully fetched.', 'data': card_content_data})
    else:
      return Response({'code': 200, 'message': 'No data found.', 'data': card_content_data})

  def post(self, request):
    '''For creating the categpry.'''
    logging.info('\n Screenshot 444444444444444\n')
    category_id = request.POST.get('category_id')
    if not category_id:
      # Category name validation
      return Response({'code': 400, 'message': 'Please enter the category id.'})
    ques_list = request.POST.getlist('question_data')
    try:
      card_data = json.loads(ques_list[0])
      for card in card_data:

        print(card)
        file_name = (str(time.time()).replace('.', ''))+'.mp3'

        question = card['question']
        answer = card['answer']
        hint = card['hint']

        try:
          question = question.replace('\'', '')
          answer = answer.replace('\'', '')
          if hint:
            hint = hint.replace('\'', '')
        except Exception as e:
          pass

        try:
          question = re.sub(r'[^\x00-\x7F]+', ' ', question)
          question = question.strip()
          answer = re.sub(r'[^\x00-\x7F]+', ' ', answer)
          answer = answer.strip()
          if hint:
            hint = re.sub(r'[^\x00-\x7F]+', ' ', hint)
            hint = hint.strip()
        except Exception as e:
          pass

        mytext = question+' Please speak your answer.'
        language = 'en'
        myobj = gTTS(text=mytext, lang=language, slow=False)
        os.chdir(settings.BASE_DIR+'/media/q2t/')
        q_file_name = 'q_' + file_name
        myobj.save(q_file_name)
        q_file_path = 'media/q2t/'+q_file_name

        mytext = answer
        language = 'en'
        myobj = gTTS(text=mytext, lang=language, slow=False)
        os.chdir(settings.BASE_DIR+'/media/q2t/')
        a_file_name = 'a_' + file_name
        myobj.save(a_file_name)
        a_file_path = 'media/q2t/'+a_file_name

        if hint:
          mytext = hint+' Please speak your answer.'
          language = 'en'
          myobj = gTTS(text=mytext, lang=language, slow=False)
          os.chdir(settings.BASE_DIR+'/media/q2t/')
          h_file_name = 'h_' + file_name
          myobj.save(h_file_name)
          h_file_path = 'media/q2t/'+h_file_name

          card_obj = CardContent(category_id=int(category_id), question=question, answer=answer, hint=hint,
                                 question_file_path=q_file_path, answer_file_path=a_file_path, hint_file_path=h_file_path)
          card_obj.save()

        else:
          card_obj = CardContent(category_id=int(category_id), question=question, answer=answer,
                                 hint=hint, recent_date=timezone.now(), question_file_path=q_file_path, answer_file_path=a_file_path)
          card_obj.save()
        time.sleep(0.1)
      return Response({'code': 200, 'message': 'Succesfully saved.'})
    except Exception as error:
      return Response({'code': 400, 'message': 'Something went wrong.', 'error': str(error)})

    return Response({'code': 400, 'message': 'Something went wrong.', 'error': ''})

  def put(self, request):
    ''' For update the existing categories '''

    category_id = request.POST.get('category_id')
    if not category_id:
      # Category name validation
      return Response({'code': 400, 'message': 'Please enter the category id.'})
    ques_list = request.POST.getlist('question_data')

    try:
      card_data = json.loads(ques_list[0])
      for card in card_data:

        print(card)

        file_name = (str(time.time()).replace('.', ''))+'.mp3'

        card_info_obj = ''
        try:
          card_info_obj = CardContent.objects.filter(
              id=card['card_content_id']).last()
          os.remove(settings.BASE_DIR+'/'+card_info_obj.question_file_path)
          os.remove(settings.BASE_DIR+'/'+card_info_obj.answer_file_path)
          if card_info_obj.hint:
            os.remove(settings.BASE_DIR+'/'+card_info_obj.hint_file_path)
        except Exception as e:
          pass

        # saving new question file

        question = card['question']
        answer = card['answer']
        hint = card['hint']

        try:
          question = question.replace('\'', '')
          answer = answer.replace('\'', '')
          if hint:
            hint = hint.replace('\'', '')
        except Exception as e:
          pass

        try:
          question = re.sub(r'[^\x00-\x7F]+', ' ', question)
          question = question.strip()
          answer = re.sub(r'[^\x00-\x7F]+', ' ', answer)
          answer = answer.strip()
          if hint:
            hint = re.sub(r'[^\x00-\x7F]+', ' ', hint)
            hint = hint.strip()
        except Exception as e:
          pass

        file_name = (str(time.time()).replace('.', ''))+'.mp3'

        mytext = question+' Please speak your answer.'
        language = 'en'
        myobj = gTTS(text=mytext, lang=language, slow=False)
        os.chdir(settings.BASE_DIR+'/media/q2t/')
        q_file_name = 'q_' + file_name
        myobj.save(q_file_name)
        q_file_path = 'media/q2t/'+q_file_name

        language = 'en'
        myobj = gTTS(text=answer, lang=language, slow=False)
        os.chdir(settings.BASE_DIR+'/media/q2t/')
        a_file_name = 'a_' + file_name
        myobj.save(a_file_name)
        a_file_path = 'media/q2t/'+a_file_name

        if card_info_obj:
          card_info_obj.category_id = category_id
          card_info_obj.question = question
          card_info_obj.answer = answer
          card_info_obj.hint = hint
          card_info_obj.recent_date = timezone.now()
          card_info_obj.question_file_path = q_file_path
          card_info_obj.answer_file_path = a_file_path

          if hint:
            language = 'en'
            hint = hint + ' Please speak your answer.'
            myobj = gTTS(text=hint, lang=language, slow=False)
            os.chdir(settings.BASE_DIR+'/media/q2t/')
            h_file_name = 'h_' + file_name
            myobj.save(h_file_name)
            h_file_path = 'media/q2t/'+h_file_name
            card_info_obj.hint_file_path = h_file_path

          card_info_obj.save()
        else:

          if hint:
            language = 'en'
            hint = hint + ' Please speak your answer.'
            myobj = gTTS(text=hint, lang=language, slow=False)
            os.chdir(settings.BASE_DIR+'/media/q2t/')
            h_file_name = 'a_' + file_name
            myobj.save(h_file_name)
            h_file_path = 'media/q2t/'+h_file_name
            card_obj = CardContent(category_id=int(category_id), question=question, answer=answer, hint=hint, recent_date=timezone.now(),
                                   question_file_path=q_file_path, answer_file_path=a_file_path, hint_file_path=h_file_path)
            card_obj.save()
          else:
            card_obj = CardContent(category_id=int(category_id), question=question, answer=answer,
                                   hint=hint, recent_date=timezone.now(), question_file_path=q_file_path, answer_file_path=a_file_path)
            card_obj.save()
          time.sleep(0.1)

      return Response({'code': 200, 'message': 'Information updated successfully.'})
    except Exception as e:
      print('error is : ', e)
      return Response({'code': 400, 'message': 'Something went wrong.', 'error': str(e)})

  def delete(self, request):
    ''' For deleting the exsiting category. '''
    card_content_id = request.GET.get('card_content_id')
    if not card_content_id:
      return Response({'code': 400, 'message': 'Enter the category id.'})
    else:
      card_obj = CardContent.objects.filter(id=card_content_id).first()
      if card_obj:
        try:

          print('card_obj.question_file_path : ', card_obj.question_file_path)
          print('card_obj.answer_file_path : ', card_obj.answer_file_path)
          print('card_obj.hint_file_path : ', card_obj.hint_file_path)
          os.remove(settings.BASE_DIR+'/'+card_obj.question_file_path)
          os.remove(settings.BASE_DIR+'/'+card_obj.answer_file_path)
          if card_obj.hint:
            os.remove(settings.BASE_DIR+'/'+card_obj.hint_file_path)
        except Exception as e:
          pass
        card_obj.delete()
        return Response({'code': 200, 'message': 'Successfully deleted.'})
      else:
        return Response({'code': 400, 'message': 'Invalid card content id.'})


class Logout(APIView):
  '''API for user logout'''
  permission_classes = (AllowAny,)

  def get(self, request):
    request.user.auth_token.delete()
    # if '_auth_user_id' in self.request.session:
    # 	del self.request.session['_auth_user_id']

    return Response({'code': 200, 'message': 'Successfully logout.'})


class QuestionToText(APIView):
  '''API for creating,fetching,editing and deleting Categories'''
  permission_classes = (AllowAny,)

  def get(self, request):
    '''Getting all the category info of existing categories'''
    cc_id = request.GET.get('cc_id')
    try:
      card_info_obj = CardContent.objects.get(id=cc_id)

      mytext = card_info_obj.question+' Please speak your answer.'
      language = 'en'
      myobj = gTTS(text=mytext, lang=language, slow=False)
      os.chdir(settings.BASE_DIR+'/media/q2t/')

      file_name = str(int(time.time()))+'.mp3'
      myobj.save(file_name)
      file_path = 'media/q2t/'+file_name
      return Response({'code': 200, 'message': 'Succesfully fetched.', 'file_path': file_path})
    except Exception as e:
      print('error is : ', e)
      return Response({'code': 200, 'message': 'No data found', 'file_path': ''})


class AccuracyCalculationText(APIView):
  '''API for creating,fetching,editing and deleting Categories'''
  permission_classes = (AllowAny,)

  def post(self, request):
    '''Getting all the category info of existing categories'''
    # json_data = json.loads(request.body)
    # print(json_data)
    # cc_id = json_data['cc_id']
    # attempt = json_data['attempt']
    # last_question = json_data['last_question']
    # input_type = json_data['input_type']
    # input_text = json_data['input_text']
    cc_id = request.POST.get('cc_id')
    print(cc_id)
    attempt = request.POST.get('attempt')
    last_question = request.POST.get('last_question')
    input_type = request.POST.get('input_type')
    input_text = request.POST.get('input_text')

    accuracy_per = ''
    output_type = ''

    try:
      print(cc_id)
      card_info_obj = CardContent.objects.get(id=cc_id)
      stored_text = card_info_obj.answer

      if input_text and input_type == 'text':
        input_text = input_text.lower()
        input_text = input_text.replace('\'', '')
        input_text = input_text.strip()

        try:
          input_text = input_text.replace('allan', 'allen')
        except Exception as e:
          pass

      if stored_text:
        stored_text = stored_text.lower()
        stored_text = stored_text.strip()

      print('input_text : ', input_text)
      print('stored_text : ', stored_text)

      def simlarity(database_sentence, current_sentence):
        X_list = word_tokenize(database_sentence)
        Y_list = word_tokenize(current_sentence)

        sw = stopwords.words('english')
        list1, list2 = list(), list()

        X_set = {w for w in X_list if not w in sw}
        Y_set = {w for w in Y_list if not w in sw}

        rvector = X_set.union(Y_set)
        for w in rvector:
          if w in X_set:
            list1.append(1)
          else:
            list1.append(0)
          if w in Y_set:
            list2.append(1)
          else:
            list2.append(0)

        c = 0
        for i in range(len(rvector)):
          c += list1[i] * list2[i]
        try:
          cosine = c / float((sum(list1) * sum(list2)) ** 0.5)
          return(str(round(cosine * 100, 3)))
        except:
          print('No words matched')
          return('0')

      # if input_text == "show me hint" or input_text == "show me hints" or input_text == "show me the hint" or input_text == "show me the hints":
      if input_text == "show me hint":

        if card_info_obj.hint:
          output_path = card_info_obj.hint_file_path
        else:
          output_path = 'media/universal/no_hint.mp3'

        output_type = 'tryagain'
        next_attempt = attempt
        return Response({'code': 200, 'message': 'Succesfully fetched.', 'accuracy': accuracy_per, 'input_text': input_text, 'stored_text': stored_text, 'output_path': output_path, 'output_type': output_type, 'next_attempt': next_attempt})

      # if input_text.find('i do not know') >= 0 or input_text.find('i dont know') >= 0 or input_text == 'i dont know' or input_text == 'i do not know':
      if input_text.find('i dont know') >= 0 or input_text == 'i dont know':
        output_path = card_info_obj.answer_file_path
        next_attempt = '1'

        if last_question:
          output_path_next = 'media/universal/testover.mp3'
          output_type = 'testover_dont_know'
        else:
          output_path_next = 'media/universal/move2next.mp3'
          output_type = 'move2next_dont_know'
        return Response({'code': 200, 'message': 'Succesfully fetched.', 'accuracy': accuracy_per, 'input_text': input_text, 'stored_text': stored_text, 'output_path': output_path, 'output_path_next': output_path_next, 'output_type': output_type, 'next_attempt': next_attempt})

      accuracy_per = simlarity(stored_text, input_text)

      print('accuracy_per : ', accuracy_per)
      print('attempt : ', attempt)
      if attempt == 1 or attempt == '1':
        if float(accuracy_per) >= 75:
          print('>75')
          next_attempt = '1'
          if last_question:
            output_path = 'media/universal/c_testover.mp3'
            output_type = 'testover'
          else:
            output_path = 'media/universal/c_move2next.mp3'
            output_type = 'move2next'

        elif float(accuracy_per) >= 50:
          print('>50 and <75')
          output_path = 'media/universal/close_try_again.mp3'
          output_type = 'tryagain'
          next_attempt = '2'
        else:
          print('<50')
          output_path = 'media/universal/nc_try_again.mp3'
          output_type = 'tryagain'
          next_attempt = '2'
      else:
        next_attempt = '1'
        if float(accuracy_per) >= 75:
          print('>75')
          if last_question:
            output_path = 'media/universal/c_testover.mp3'
            output_type = 'testover'
          else:
            output_path = 'media/universal/c_move2next.mp3'
            output_type = 'move2next'

        elif float(accuracy_per) >= 50:
          print('>50 and <75')
          if last_question:
            output_path = 'media/universal/close_testover.mp3'
            output_type = 'testover'
          else:
            output_path = 'media/universal/close_move2next.mp3'
            output_type = 'move2next'
        else:
          print('<50')
          if last_question:
            output_path = 'media/universal/nc_testover.mp3'
            output_type = 'testover'
          else:
            output_path = 'media/universal/nc_move2next.mp3'
            output_type = 'move2next'

      return Response({'code': 200, 'message': 'Succesfully fetched.', 'accuracy': accuracy_per, 'input_text': input_text, 'stored_text': stored_text, 'output_path': output_path, 'output_type': output_type, 'next_attempt': next_attempt})
    except Exception as e:
      print('error is : ', e)
      return Response({'code': 200, 'message': 'No data found', 'accuracy': '', 'error': str(e), 'output_path': '', 'output_type': 'error', 'next_attempt': ''})


class AccuracyCalculation(APIView):
  '''API for creating,fetching,editing and deleting Categories'''
  permission_classes = (AllowAny,)

  def post(self, request):
    '''Getting all the category info of existing categories'''
    cc_id = request.POST.get('cc_id')
    attempt = request.POST.get('attempt')
    last_question = request.POST.get('last_question')

    accuracy_per = ''
    output_type = ''
    try:
      card_info_obj = CardContent.objects.get(id=cc_id)

      audio = request.FILES['voice_input']
      user_voice_obj = UserVoiceInput(voice_input=audio)
      user_voice_obj.save()
      os.chdir(settings.BASE_DIR+'/media/user_input/')
      file_name = (str(time.time()).replace('.', ''))+'.wav'
      from pydub import AudioSegment
      flac_audio = AudioSegment.from_file(user_voice_obj.voice_input.path)
      flac_audio.export(file_name, format="wav")
      r = sr.Recognizer()
      with sr.AudioFile(file_name) as source:
        audio = r.record(source)
        print('Done!')

      try:
        os.remove(settings.BASE_DIR+'/media/user_input/'+file_name)
        print('File removed successfully.')
        try:
          os.remove(user_voice_obj.voice_input.path)
        except Exception as e:
          pass
        user_voice_obj.delete()
        print('wav file data is removed')
      except Exception as e:
        print('error is: ', e)
        pass

      # # Calculating accuracy
      input_text = r.recognize_google(audio)
      stored_text = card_info_obj.answer

      if input_text:
        input_text = input_text.lower()
        input_text = input_text.replace('\'', '')
        input_text = input_text.strip()

        try:
          input_text = input_text.replace('allan', 'allen')
        except Exception as e:
          pass

      if stored_text:
        stored_text = stored_text.lower()
        stored_text = stored_text.strip()

      print('input_text : ', input_text)
      print('stored_text : ', stored_text)

      def simlarity(database_sentence, current_sentence):
        X_list = word_tokenize(database_sentence)
        Y_list = word_tokenize(current_sentence)

        sw = stopwords.words('english')
        list1, list2 = list(), list()

        X_set = {w for w in X_list if not w in sw}
        Y_set = {w for w in Y_list if not w in sw}

        rvector = X_set.union(Y_set)
        for w in rvector:
          if w in X_set:
            list1.append(1)
          else:
            list1.append(0)
          if w in Y_set:
            list2.append(1)
          else:
            list2.append(0)

        c = 0
        for i in range(len(rvector)):
          c += list1[i] * list2[i]
        try:
          cosine = c / float((sum(list1) * sum(list2)) ** 0.5)
          return(str(round(cosine * 100, 3)))
        except:
          print('No words matched')
          return('0')

      # if input_text == "show me hint" or input_text == "show me hints" or input_text == "show me the hint" or input_text == "show me the hints":
      if input_text == "show me hint":

        if card_info_obj.hint:
          output_path = card_info_obj.hint_file_path
        else:
          output_path = 'media/universal/no_hint.mp3'

        output_type = 'tryagain'
        next_attempt = attempt
        return Response({'code': 200, 'message': 'Succesfully fetched.', 'accuracy': accuracy_per, 'input_text': input_text, 'stored_text': stored_text, 'output_path': output_path, 'output_type': output_type, 'next_attempt': next_attempt})

      # if input_text.find('i do not know') >= 0 or input_text.find('i dont know') >= 0 or input_text == 'i dont know' or input_text == 'i do not know':
      if input_text.find('i dont know') >= 0 or input_text == 'i dont know':
        output_path = card_info_obj.answer_file_path
        next_attempt = '1'

        if last_question:
          output_path_next = 'media/universal/testover.mp3'
          output_type = 'testover_dont_know'
        else:
          output_path_next = 'media/universal/move2next.mp3'
          output_type = 'move2next_dont_know'
        return Response({'code': 200, 'message': 'Succesfully fetched.', 'accuracy': accuracy_per, 'input_text': input_text, 'stored_text': stored_text, 'output_path': output_path, 'output_path_next': output_path_next, 'output_type': output_type, 'next_attempt': next_attempt})

      accuracy_per = simlarity(stored_text, input_text)

      print('accuracy_per : ', accuracy_per)
      print('attempt : ', attempt)
      if attempt == 1 or attempt == '1':
        if float(accuracy_per) >= 75:
          print('>75')
          next_attempt = '1'
          if last_question:
            output_path = 'media/universal/c_testover.mp3'
            output_type = 'testover'
          else:
            output_path = 'media/universal/c_move2next.mp3'
            output_type = 'move2next'

        elif float(accuracy_per) >= 50:
          print('>50 and <75')
          output_path = 'media/universal/close_try_again.mp3'
          output_type = 'tryagain'
          next_attempt = '2'
        else:
          print('<50')
          output_path = 'media/universal/nc_try_again.mp3'
          output_type = 'tryagain'
          next_attempt = '2'
      else:
        next_attempt = '1'
        if float(accuracy_per) >= 75:
          print('>75')
          if last_question:
            output_path = 'media/universal/c_testover.mp3'
            output_type = 'testover'
          else:
            output_path = 'media/universal/c_move2next.mp3'
            output_type = 'move2next'

        elif float(accuracy_per) >= 50:
          print('>50 and <75')
          if last_question:
            output_path = 'media/universal/close_testover.mp3'
            output_type = 'testover'
          else:
            output_path = 'media/universal/close_move2next.mp3'
            output_type = 'move2next'
        else:
          print('<50')
          if last_question:
            output_path = 'media/universal/nc_testover.mp3'
            output_type = 'testover'
          else:
            output_path = 'media/universal/nc_move2next.mp3'
            output_type = 'move2next'

      return Response({'code': 200, 'message': 'Succesfully fetched.', 'accuracy': accuracy_per, 'input_text': input_text, 'stored_text': stored_text, 'output_path': output_path, 'output_type': output_type, 'next_attempt': next_attempt})

    except Exception as e:
      print('error is : ', e)
      return Response({'code': 200, 'message': 'No data found', 'accuracy': '', 'error': str(e), 'output_path': '', 'output_type': 'error', 'next_attempt': ''})

  # def post(self,request):
  # 	'''Getting all the category info of existing categories'''
  # 	cc_id = request.POST.get('cc_id')
  # 	accuracy_per=''
  # 	output_type=''
  # 	try:
  # 		card_info_obj = CardContent.objects.get(id = cc_id)

  # 		# Fetching voice input
  # 		audio = request.FILES['voice_input']
  # 		user_voice_obj = UserVoiceInput(voice_input=audio)
  # 		user_voice_obj.save()
  # 		# user_voice_obj = UserVoiceInput.objects.last()
  # 		os.chdir('/var/www/html/myproject/media/user_input/')
  # 		file_name = (str(time.time()).replace('.',''))+'.wav'
  # 		from pydub import AudioSegment
  # 		flac_audio = AudioSegment.from_file(user_voice_obj.voice_input.path)
  # 		flac_audio.export(file_name, format="wav")

  # 		r = sr.Recognizer()
  # 		with sr.AudioFile(file_name) as source:
  # 			audio = r.record(source)
  # 			print ('Done!')

  # 		try:
  # 			os.remove('/var/www/html/myproject/media/user_input/'+file_name)
  # 			print('File removed successfully.')

  # 			try:
  # 				os.remove(user_voice_obj.voice_input.path)
  # 			except Exception as e:
  # 				pass
  # 			user_voice_obj.delete()
  # 			print('wav file data is removed');
  # 		except Exception as e:
  # 			print('error is: ',e)
  # 			pass

  # 		print('\n line 858 \n')
  # 		# # Calculating accuracy
  # 		input_text = r.recognize_google(audio)
  # 		stored_text = card_info_obj.answer

  # 		if input_text:
  # 			input_text = input_text.lower()
  # 			input_text = input_text.replace('\'','')
  # 			input_text = input_text.strip()

  # 		if stored_text:
  # 			stored_text = stored_text.lower()
  # 			stored_text = stored_text.strip()

  # 		print('input_text : ',input_text)
  # 		print('stored_text : ',stored_text)

  # 		def simlarity(database_sentence, current_sentence):
  # 			X_list = word_tokenize(database_sentence)
  # 			Y_list = word_tokenize(current_sentence)

  # 			sw = stopwords.words('english')
  # 			list1, list2 = list(), list()

  # 			X_set = {w for w in X_list if not w in sw}
  # 			Y_set = {w for w in Y_list if not w in sw}

  # 			rvector = X_set.union(Y_set)
  # 			for w in rvector:
  # 				if w in X_set:
  # 					list1.append(1)
  # 				else:
  # 					list1.append(0)
  # 				if w in Y_set:
  # 					list2.append(1)
  # 				else:
  # 					list2.append(0)

  # 			c = 0
  # 			for i in range(len(rvector)):
  # 				c += list1[i] * list2[i]
  # 			try:
  # 				cosine = c / float((sum(list1) * sum(list2)) ** 0.5)
  # 				return(str(round(cosine * 100, 3)))
  # 			except:
  # 				print('No words matched')
  # 				return('0')

  # 		print('=>', input_text.find('i do not know'))
  # 		print('=--=-=-=-=>', input_text.find('i dont know'))

  # 		if input_text == "hint" or input_text == "hints" or input_text == "show me hint" or input_text == "show me hints" or input_text == "show me the hint" or input_text == "show me the hints":
  # 			if card_info_obj.hint:
  # 				output_type = 'hint'
  # 				return Response({'code':200, 'message':'Succesfully fetched.', 'accuracy':accuracy_per, 'input_text':input_text, 'stored_text':stored_text, 'output_path':card_info_obj.hint_file_path, 'output_type':output_type})
  # 			else:
  # 				output_type = 'no hint'
  # 				return Response({'code':200, 'message':'Succesfully fetched.', 'accuracy':accuracy_per, 'input_text':input_text, 'stored_text':stored_text, 'output_path':'media/no_hint.mp3', 'output_type':output_type})

  # 		if input_text.find('i do not know') > 0 or input_text.find('i dont know') > 0 or input_text == 'i dont know' or input_text == 'i do not know':
  # 			attempt = request.POST.get('attempt')
  # 			if attempt == 1 or attempt == '1':

  # 				print('attempt : ',attempt)
  # 				print('Now check for hints.')

  # 				print('Hint : ',card_info_obj.hint)

  # 				if card_info_obj.hint :
  # 					print('Hint is present. We will check accuracy of entered voice input. ')

  # 					accuracy_per = simlarity(stored_text, input_text)
  # 					# Generate result as per user input.

  # 					print('accuracy_per : ',accuracy_per)

  # 					if float(accuracy_per) < 50 :
  # 						output_path = 'media/improve.mp3'
  # 						output_type = 'improve'
  # 					else:
  # 						os.chdir('/var/www/html/myproject/media/q_result')
  # 						file_name = (str(time.time()).replace('.',''))+'.mp3'

  # 						mytext = 'Your answer is '+str(accuracy_per)+' percent correct.'
  # 						language = 'en'
  # 						myobj = gTTS(text=mytext, lang=language, slow=False)
  # 						q_file_name = 'q_' + file_name
  # 						myobj.save(q_file_name)
  # 						output_path = 'media/q_result/'+q_file_name
  # 						output_type = 'accurate'
  # 					accuracy_per = str(accuracy_per)+'%'
  # 					print('output_path : ',output_path)
  # 					return Response({'code':200, 'message':'Succesfully fetched.', 'accuracy':accuracy_per, 'input_text':input_text, 'stored_text':stored_text, 'output_path':output_path, 'output_type':output_type})

  # 				else:
  # 					print('Hint is not present, and going to share answer file.')
  # 					output_type = 'answer'
  # 					return Response({'code':200, 'message':'Succesfully fetched.', 'accuracy':accuracy_per, 'input_text':input_text, 'stored_text':stored_text, 'output_path':card_info_obj.answer_file_path, 'output_type':output_type})
  # 			else:
  # 				print('attempt : ',attempt)
  # 				print('Give answer as output file.')
  # 				output_type = 'answer'
  # 				return Response({'code':200, 'message':'Succesfully fetched.', 'accuracy':accuracy_per, 'input_text':input_text, 'stored_text':stored_text, 'output_path':card_info_obj.answer_file_path, 'output_type':output_type})

  # 		accuracy_per = simlarity(stored_text, input_text)
  # 		# accuracy_per=''

  # 		# Generate result as per user input.
  # 		print('accuracy_per : ',accuracy_per)

  # 		if float(accuracy_per) < 50 :
  # 			output_path = 'media/improve.mp3'
  # 			output_type = 'improve'
  # 		else:
  # 			os.chdir('/var/www/html/myproject/media/q_result')
  # 			file_name = (str(time.time()).replace('.',''))+'.mp3'

  # 			mytext = 'Your answer is '+str(accuracy_per)+' percent correct.'
  # 			language = 'en'
  # 			myobj = gTTS(text=mytext, lang=language, slow=False)
  # 			q_file_name = 'q_' + file_name
  # 			myobj.save(q_file_name)
  # 			output_path = 'media/q_result/'+q_file_name
  # 			output_type = 'accurate'
  # 		accuracy_per = str(accuracy_per)+'%'
  # 		print('output_path : ',output_path)
  # 		return Response({'code':200, 'message':'Succesfully fetched.', 'accuracy':accuracy_per, 'input_text':input_text, 'stored_text':stored_text, 'output_path':output_path, 'output_type':output_type})
  # 	except Exception as e:
  # 		print('error is : ',e)
  # 		logging.info('sssssssssssssssssssss')
  # 		return Response({'code' : 200, 'message' : 'No data found', 'accuracy' : '', 'error' : str(e), 'output_path':'', 'output_type':'error'})


class ReportGeneration(APIView):
  '''API for creating,fetching,editing and deleting Categories'''
  permission_classes = (AllowAny,)

  def get(self, request):
    '''Getting all the category info of existing categories'''
    category_id = request.GET.get('category_id')
    user_id = request.GET.get('user_id')
    title = request.GET.get('title')

    # category_id = 36
    # user_id = 82

    print('=============')
    print('category_id : ', category_id)
    print('user_id : ', user_id)
    from datetime import datetime, timedelta
    from collections import OrderedDict
    d1 = OrderedDict()
    try:

      # title= 'monthly'
      if title == 'Month':
        now = datetime.now()
        later = now + timedelta(days=31)
        start_of_week = datetime(year=now.year, month=now.month, day=1)
        end_of_week = datetime(year=later.year, month=later.month, day=1)
      else:
        # date_str = str(datetime.now().date())
        # date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        # start_of_week = date_obj - timedelta(days=date_obj.weekday())
        # end_of_week = start_of_week + timedelta(days=6)
        date_str = str(datetime.now().date())
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')

        start_of_week = date_obj - timedelta(days=date_obj.weekday())
        end_of_week = start_of_week + timedelta(days=6)

      print('start_of_week : ', start_of_week, 'type : ', type(start_of_week))
      print('end_of_week : ', end_of_week, 'type : ', type(end_of_week))
      print('\n\n\n\n\n')
      delta = end_of_week - start_of_week
      for i in range(delta.days+1):
        d1[str((start_of_week + timedelta(days=i)).date())] = [0.0]

      delta = end_of_week - start_of_week
      for i in range(delta.days+1):
        d1[str((start_of_week + timedelta(days=i)).date())] = [0.0]

      o = ReportResult.objects.filter(
          created_at__gte=start_of_week, created_at__lt=end_of_week, category_id=category_id, user_id=user_id)
      print(o)
      print('\n\n\n')

      final_data_list = []
      for i in o:
        d1.setdefault(str(i.created_at.date()), []).append(i.percentage)
      final_data_list.append(d1)

      print(final_data_list)
      print('\n\n\n\n\n\n\n')

      for data in final_data_list:
        for k, v in data.items():
          try:
            data[k] = round(sum(v)/(len(v)-1), 2)
          except Exception as e:
            data[k] = 0.0

      print(data)
      return Response({'code': 200, 'message': 'Succesfully fetched.', 'title': title, 'graph_data': data})
    except Exception as e:
      print('error is : ', e)
      return Response({'code': 200, 'message': 'No data found'})

  def post(self, request):
    '''Getting all the category info of existing categories'''
    print(request.POST)
    category_id = request.POST.get('category_id')
    user_id = request.POST.get('user_id')
    test_data = request.POST.getlist('test_data')

    try:
      test_data = json.loads(test_data[0])
      correct_question = len(test_data)
      total_question = CardContent.objects.filter(
          category_id=category_id).count()
      total_question = 9
      if correct_question:
        percentage = (float(correct_question)/float(total_question))*100
        percentage = round(percentage, 2)
      else:
        percentage = 0.0

      print('percentage : ', percentage)
      # for data in test_data:
      # 	for k,v in data.items():
      # 		print(k,'-=-> ',v)

      obj = ReportResult(category_id=category_id, user_id=user_id,
                         test_data=test_data, percentage=percentage)
      obj.save()

      return Response({'code': 200, 'message': 'Succesfully saved.'})

    except Exception as e:
      print('error is : ', e)
      f = open("demofrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrile2.txt", "a")
      f.write("Now the file has more content!")
      f.close()
      return Response({'code': 400, 'message': str(e)})


class DummyAPI(APIView):
  permission_classes = (AllowAny,)

  def post(self, request):
    try:
      print('\n\n\n\n\n')
      print('data is  : ')
      print(request.POST)
    except Exception as e:
      pass
    return Response({'code': '200', 'message': 'dummy api'})
