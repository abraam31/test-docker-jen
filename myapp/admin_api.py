from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response

from django.contrib.auth.models import User
from .models import Login_User

class AllUsersinfo(APIView):
	''' For getting all information of the users.'''

	permission_classes = (AllowAny,) 

	def get(self,request):
		''' For fetching all user data and one user data. '''
		code = 200
		message = ''
		try:
			user_id = request.GET.get('user_id')
			user_all_data = []
			if user_id:
				user_info = Login_User.objects.filter(id = int(user_id)).last()
				user_data = {}
				try:
					if user_info:
						user_data['user_name'] = user_info.username.username
						user_data['first_name'] = user_info.first_name
						user_data['last_name'] = user_info.last_name
						user_data['phone_number'] = user_info.phone_number
						user_data['email'] =  user_info.email
						user_data['role'] = user_info.role
						message = 'Successfully fetched.'
					else:
						message = 'No user found.'
				except Exception as e:
					code = 400
					message = 'Invalid user_id.'
				return Response({'code' : 200, 'message' : message,'data' : user_data })
			else:
				user_info = Login_User.objects.filter(role = 'user')
				for info in user_info:
					user_data={}
					print(info)
					user_data['user_name'] = info.username.username
					user_data['first_name'] = info.first_name
					user_data['last_name'] = info.last_name
					user_data['phone_number'] = info.phone_number
					user_data['email'] =  info.email
					user_data['role'] = info.role
					user_data['user_id'] = info.id
					user_all_data.append(user_data)
				message = 'Successfully fetched.'
		except Exception as e:
			code = 400
			message = 'Something went wrong.'
		return Response({'code' : code, 'message' : message, 'data': user_all_data})

	def post(self,request):
		code = 200
		message = ''
		try:
			first_name = request.POST.get('first_name')
			last_name = request.POST.get('last_name')
			username = request.POST.get('email')
			phone_number = request.POST.get('phone_number')
			password = request.POST.get('password')


			print('first_name : ',first_name)
			print('last_name : ',last_name)
			print('username : ',username)
			print('phone_number : ',phone_number)
			print('password : ',password)


			# first_name = 'user'
			# last_name = 'admin'
			# username = 'user@gmail.com'
			# phone_number = '2222222222'
			# password = '123456'

			try:
				user = User.objects.create(username = username)
				user.set_password(password)
				user.save()
				if username is None:
					pass
				else:
					user.email = username
					user.save()
			except Exception as e:
				code = 400
				message = 'User already Exist.'
				return Response({'code' : code,'message' : message})
				pass


			login_user = Login_User(username_id = user.id, first_name = str(first_name), last_name = last_name, phone_number = phone_number, email = username ,role = 'user')
			login_user.save()

			message = 'User created Successfully.'
		except Exception as e:
			print('error is : ',e)
			code = 400
			message = 'Something went wrong.'
		return Response({'code' : code,'message' : message})

	def delete(self,request):
		''' For deleting the exsiting category. '''
		code = 200
		message = ''
		user_id = request.GET.get('user_id')

		if not user_id:
			return Response({'code' : 400,'message' : 'Enter the user_id.'})
		else:
			try:
				user_obj = Login_User.objects.filter(id = int(user_id),role = 'user').last()
				user_obj.username.delete()
				message = 'User is deleted Successfully.'
			except Exception as e:
				code=400
				message = 'Something went wrong.'

			return Response({'code' : code,'message' : message})

	def put(self,request):
		code = 200
		message = ''
		try:
			user_id = request.POST.get('user_id')
			first_name = request.POST.get('first_name')
			last_name = request.POST.get('last_name')
			phone_number = request.POST.get('phone_number')
			password = request.POST.get('password')

			user_info = Login_User.objects.filter(id = int(user_id),role = 'user').last()

			user_info.first_name = first_name
			user_info.last_name = last_name
			user_info.phone_number = phone_number
			user_info.save()

			if password: 
				user_info.username.set_password(password)
				user_info.username.save()

			message = 'User inforamtion updated Successfully.'
		except Exception as e:
			code = 400
			message = 'Something went wrong.'
		return Response({'code' : code,'message' : message})