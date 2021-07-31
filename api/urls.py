from django.urls import path, include
from api import views
from django.db import router
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('blog', views.BlogView, basename='blog')
router.register('contact', views.ContactView, basename='contact')
router.register('user', views.CreateUser, basename='user')
router.register('staff', views.CreateStaff, basename='staff')

urlpatterns = [
    path('',include(router.urls)),
    path('auth/', include('rest_framework.urls', namespace='authentication')),
]
