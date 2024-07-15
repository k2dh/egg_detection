from rest_framework import serializers
from ..models import Egg
from django.core.files.uploadedfile import InMemoryUploadedFile
from ..apps import EggsConfig
from PIL import Image
from io import BytesIO
import numpy as np
from ..ensemble import ensembleResult
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.validators import UniqueValidator


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
            
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Frontend에서 더 필요한 정보가 있다면 여기에 추가적으로 작성하면 됩니다. token["is_superuser"] = user.is_superuser 이런식으로요.
        token['username'] = user.username
        token['email'] = user.email
        return token

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username']
        )

        user.set_password(validated_data['password'])
        user.save()