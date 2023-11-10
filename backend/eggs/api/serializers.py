from rest_framework import serializers
from ..models import Egg
from django.core.files.uploadedfile import InMemoryUploadedFile
from ..apps import EggsConfig
from PIL import Image
from io import BytesIO
import numpy as np
from ..ensemble import ensembleResult

class EggSerializer(serializers.ModelSerializer):
    class Meta:
        model = Egg
        fields = ['id','name','image']

    def img_process(self, img :InMemoryUploadedFile) -> InMemoryUploadedFile:
        pil_image = Image.open(img).convert("RGB")
        # image_result = EggsConfig.ml_model.predict(pil_image)
        image_result = ensembleResult(pil_image)
        new_img_io = BytesIO()
        # for r in image_result:
        new_img = image_result
        new_img = np.flip(new_img, -1)
        new_img = Image.fromarray(new_img)
        new_img.save(new_img_io, format="JPEG")
        result = InMemoryUploadedFile(
            new_img_io,
            'ImageField',
            img.name,
            'image/jpg',
            new_img_io.getbuffer().nbytes,
            img.charset
        )
            
        return result

    def create(self, validated_data):

        result = self.img_process(validated_data['image'])
        validated_data['image']  = result
        return super().create(validated_data)
            
