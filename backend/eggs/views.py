from django.shortcuts import render
from rest_framework import viewsets
from .api.serializers import EggSerializer
from .models import Egg
# Create your views here.

class EggView(viewsets.ModelViewSet):
    serializer_class = EggSerializer
    queryset = Egg.objects.all()