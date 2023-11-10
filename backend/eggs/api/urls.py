from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import EggViewSet

egg_router = DefaultRouter()
egg_router.register(r'eggs', EggViewSet)