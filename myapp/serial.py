from rest_framework import serializers
from .models import Login_User

class Login_UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = Login_User
		fields = ('id', 'first_name', 'last_name', 'phone_number', 'email')
