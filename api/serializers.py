from rest_framework import serializers
from app.models import Blog, Contact
from django.contrib.auth.models import User

class BlogSerializer(serializers.ModelSerializer):
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Blog
        
        fields = "__all__"
        read_only_fields = ['slug', 'date']

   

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, write_only=True)
    confirm_password = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'is_staff',
            'is_superuser',
            'password',
            'confirm_password',
            'groups',
            'user_permissions',
        ]
        read_only_fields = ['id', 'is_staff', 'is_superuser', 'user_permissions', 'groups']

    def validate(self, data):
        p1 = data.get('password')
        p2 = data.get('confirm_password')
        if p1 != p2:
            raise serializers.ValidationError("Password doesn't match")
        return data