from rest_framework import viewsets
from app.models import Blog, Contact
from .serializers import BlogSerializer, ContactSerializer, UserSerializer
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.filters import SearchFilter
from .pagination import MyPagination
from django.contrib.auth.models import User, Permission, Group
from rest_framework.response import Response
from rest_framework import status

class BlogView(viewsets.ModelViewSet):
    serializer_class = BlogSerializer

    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]  

    filter_backends = [SearchFilter]
    search_fields = ['title', 'creator']

    pagination_class = MyPagination
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Blog.objects.all()
        else:
            return Blog.objects.filter(creator=user)
    

class ContactView(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAdminUser]   


class CreateUser(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_staff=False)
    serializer_class = UserSerializer

    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():        
            user = User.objects.create(first_name=request.data['first_name'], last_name=request.data['last_name'], email=request.data['email'], username=request.data['username'], password=request.data['password'])
            group = Group.objects.get_or_create(name='Blogger')
            user.groups.add(group)
            user.save()
            return Response({'msg':'Created Successfuly'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)


class CreateStaff(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_staff=True)
    serializer_class = UserSerializer

    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():        
            user = User.objects.create(first_name=request.data['first_name'], last_name=request.data['last_name'], email=request.data['email'], username=request.data['username'], password=request.data['password'], is_staff=True)
            perm = Permission.objects.get_or_create(name='Can delete blog')
            user.user_permissions.add(perm)
            user.save()
            return Response({'msg':'Created Successfuly'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)
