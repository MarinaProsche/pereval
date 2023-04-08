from .models import *
from rest_framework import serializers
from django.db.utils import OperationalError
import datetime
from django.forms import model_to_dict
from drf_extra_fields.fields import Base64ImageField
from rest_framework.response import Response


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'surname', 'patronymic', 'phone', 'email']

        extra_kwargs = {
            'email': {'validators': []}, #убираем валидацию мейла, чтобы можно было редактировать записи
        }
class CoordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coords
        fields = ['latitude', 'longitude', 'height']

class ImagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Images
        fields = ['title', 'img', 'date_added',]
        read_only_fields = [
            'id',
            'date_added',
        ]

class PerevalSerializer(serializers.ModelSerializer):
    coords = CoordSerializer()
    user = UserSerializer()
    photos = ImagesSerializer(many=True)
    class Meta:
        model = Pereval
        fields = ['id',
                 'title',
                 'beautyTitle',
                 'other_titles',
                 'connects',
                 'coords',
                 'level',
                 'weather',
                 'status',
                 'add_time',
                 'user',
                 'photos'
                  ]
        read_only_fields = [
            'id',
            'add_time',
            'status'
        ]
        depth = 1

    def create(self, validated_data):
        coords = validated_data.pop('coords')
        user = validated_data.pop('user')
        images = validated_data.pop('photos')
        try:
            user_instance = User.objects.filter(email=user['email']).first()
            if not user_instance:
                user_instance = User.objects.create(**user)
            coords_instance = Coords.objects.create(**coords)
            pereval_instance = Pereval.objects.create(
                user=user_instance,
                coords=coords_instance,
                **validated_data)
            for image in images:
                Images.objects.create(pereval=pereval_instance, **image)
            return pereval_instance
        except OperationalError:
            raise DBConnectException()

    def update(self, instance, validated_data):
        coords = validated_data.pop('coords', None)
        user = validated_data.pop('user', None)
        images = validated_data.pop('photos', None)
        try:
            if coords:
                coords_fields = model_to_dict(instance.coords)
                coords_unit = {**coords_fields, **coords}
                coords_unit.pop('id', None)
                coords_instance, created = Coords.objects.get_or_create(**coords_unit)
                instance.coords = coords_instance
            if images:
                Images.objects.filter(pereval=instance).delete()
                for image in images:
                    Images.objects.create(pereval=instance, **image)
            return super().update(instance, validated_data)
        except OperationalError:
            raise DBConnectException()