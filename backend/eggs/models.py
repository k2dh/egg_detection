from django.db import models
from . import apps

# Create your models here.
class Egg(models.Model):
    name = models.TextField()
    image = models.ImageField(blank=True, upload_to='images', null=True)

    def __str__(self) -> str:
        return self.name