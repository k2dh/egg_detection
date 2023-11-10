from rest_framework.viewsets import ModelViewSet
from ..models import Egg
from .serializers import EggSerializer

class EggViewSet(ModelViewSet):
    queryset = Egg.objects.all()
    serializer_class = EggSerializer
