from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Login_User, Folder, SetTable


class FolderInfo(APIView):
	'''API for creating,fetching,editing and deleting Categories'''
	permission_classes = (AllowAny,)

	def get(self,request):
		'''Getting all the category info of existing categories'''
		folder_data = []
		folder_id = request.GET.get('folder_id')
		login_user_id = request.GET.get('user_id')
		role = request.GET.get('role')

		if folder_id:
			all_folder_obj = Folder.objects.filter(id = int(folder_id))
			if not all_folder_obj:
				return Response({'code' : 200, 'message' : 'Invalid folder id.' })
		elif login_user_id:
			all_folder_obj = Folder.objects.filter(creator_id = int(login_user_id))
			if not all_folder_obj:
				return Response({'code' : 400, 'message' : 'Invalid user id.' })
		else:
			all_folder_obj = Folder.objects.all()

		if all_folder_obj:
			for folder in all_folder_obj:
				category_info = {}
				category_info['name'] = folder.name
				category_info['description'] = folder.description
				category_info['role'] = folder.creator.role
				category_info['folder_id'] = folder.id
				category_info['recent_date'] = folder.recent_date
				if folder.creator:
					category_info['user_id'] = folder.creator.id

				folder_data.append(category_info)

			return Response({'code' : 200, 'message' : 'Succesfully fetched.', 'data' : folder_data })
		else:
			return Response({'code' : 200, 'message' : 'No data found.', 'data' : folder_data })


	def post(self, request):
		'''For creating the categpry.'''
		name = request.POST.get('name')
		description = request.POST.get('description')
		login_user_id = request.POST.get('user_id')

		if not name:
			# Category name validation
			return Response({'code' : 200, 'message' : 'Please enter the name of category.'})


		# folder_obj = Folder.objects.filter(name = str(name)).first()
		# # Checking if any folder exist with the same name or not.
		# if folder_obj:
		# 	return Response({'code' : 200, 'message' : 'This category name already exists.'})
		try:
			folder_obj = Folder(name = name, recent_date=timezone.now(), description = description, creator_id = int(login_user_id))
			folder_obj.save()
			return Response({'code' : 200, 'message' : 'Succesfully saved.'})
		except Exception as error:
			return Response({'code' : 400, 'message' : 'Something went wrong.','error' : str(error)})
 

	def put(self,request):
		''' For update the existing categories '''
		folder_id = request.POST.get('folder_id')
		folder_name = request.POST.get('name')
		folder_description = request.POST.get('description')

		folder_obj = Folder.objects.filter(id = int(folder_id)).last()
		if not folder_id:
			return Response({'code' : 400,'message' : 'Enter the folder_id.'})
		else:
			folder_obj.name = folder_name
			folder_obj.description = folder_description
			folder_obj.recent_date = timezone.now()
			folder_obj.save()
		return Response({'code' : 200,'message' : 'Folder Information updated.'})


	def delete(self,request):
		''' For deleting the exsiting category. '''
		code = 200
		message = ''
		folder_id = request.GET.get('folder_id')

		if not folder_id:
			return Response({'code' : 400,'message' : 'Enter the folder_id.'})
		else:
			try:
				folder_obj = Folder.objects.filter(id = int(folder_id)).last()
				folder_obj.delete()
				message = 'Folder is deleted Successfully.'
			except Exception as e:
				code=400
				message = 'Folder_id Not exist.'

			return Response({'code' : code,'message' : message})

class SetInfo(APIView):
	'''API for creating,fetching,editing and deleting Categories'''
	permission_classes = (AllowAny,)

	def get(self,request):
		'''Getting all the Set info of existing categories'''
		set_data = []
		set_id = request.GET.get('set_id')
		login_user_id = request.GET.get('user_id')
		role = request.GET.get('role')
		folder_id = request.GET.get('folder_id')

		if set_id:
			all_set_obj = SetTable.objects.filter(id = int(set_id))
			if not all_set_obj:
				return Response({'code' : 200, 'message' : 'Invalid folder id.' })
		if folder_id : 
			all_set_obj = SetTable.objects.filter(folder_id = int(folder_id))
			print('all set obj : ',all_set_obj)
		elif login_user_id:
			all_set_obj = SetTable.objects.filter(creator_id = int(login_user_id), creator__role = str(role))
			if not all_set_obj:
				return Response({'code' : 200, 'message' : 'Invalid user id.' })
		else:
			all_set_obj = SetTable.objects.all()

		if all_set_obj:
			for set_obj in all_set_obj:
				set_info = {}
				set_info['name'] = set_obj.name
				set_info['description'] = set_obj.description
				set_info['set_id'] = set_obj.id
				set_info['folder_id'] = set_obj.folder.id
				set_info['role'] = set_obj.creator.role
				set_info['recent_date'] = set_obj.recent_date
				if set_obj.creator:
					set_info['user_id'] = set_obj.creator.id
				set_data.append(set_info)

			return Response({'code' : 200, 'message' : 'Succesfully fetched.', 'data' : set_data })
		else:
			return Response({'code' : 200, 'message' : 'No data found.', 'data' : set_data })


	def post(self, request):
		'''For creating the categpry.'''
		name = request.POST.get('name')
		description = request.POST.get('description')
		login_user_id = request.POST.get('user_id')
		folder_id = request.POST.get('folder_id')

		# settable_obj = SetTable.objects.filter(name = str(name)).first()
		# # Checking if any set exist with the same name or not.
		# if settable_obj:
		# 	return Response({'code' : 200, 'message' : 'This set name already exists.'})
		try:
			settable_obj = SetTable(name = name, recent_date=timezone.now(), description = description , creator_id = int(login_user_id), folder_id=int(folder_id))
			settable_obj.save()
			return Response({'code' : 200, 'message' : 'Succesfully saved.'})
		except Exception as error:

			return Response({'code' : 400, 'message' : 'Something went wrong.','error' : str(error)})
 

	def put(self,request):
		''' For update the existing categories '''
		set_id = request.POST.get('set_id')
		set_name = request.POST.get('name')
		set_description = request.POST.get('description')

		set_obj = SetTable.objects.filter(id = int(set_id)).last()
		if not set_id:
			return Response({'code' : 400,'message' : 'Enter the set_id.'})
		else:
			set_obj.name = set_name
			set_obj.description = set_description
			set_obj.recent_date = timezone.now()
			set_obj.save()
		return Response({'code' : 200,'message' : 'Set Information updated.'})


	def delete(self,request):
		''' For deleting the exsiting category. '''
		code = 200
		message = ''
		set_id = request.GET.get('set_id')

		if not set_id:
			return Response({'code' : 400,'message' : 'Enter the Set ID.'})
		else:
			try:
				folder_obj = SetTable.objects.filter(id = int(set_id)).last()
				folder_obj.delete()
				message = 'Set is deleted Successfully.'
			except Exception as e:
				code=400
				message = 'Set Not exist.'

			return Response({'code' : code,'message' : message})