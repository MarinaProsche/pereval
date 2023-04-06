from .models import *
from rest_framework import serializers
from django.db.utils import OperationalError
import datetime
from django.forms import model_to_dict



def file_size(value):  # add this to some file where you can import it from
    limit = 2 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 2 MiB.')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'surname', 'patronymic', 'phone', 'email']

        extra_kwargs = {
            'email': {'validators': []}, #убираем валидацию мейла
        }
class CoordSerializer(serializers.ModelSerializer):
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    class Meta:
        model = Coords
        fields = ['latitude', 'longitude', 'height']

class ImagesSerializer(serializers.ModelSerializer):
    img = serializers.ImageField(max_length=None, use_url=True, validators=[file_size])
    class Meta:
        model = Images
        fields = ['title', 'img', 'date_added', 'pereval']
        read_only_fields = [
            'id',
            'date_added',
        ]

    def create(self, validated_data):
        pereval = Pereval.objects.create(**validated_data)
        coords_data = validated_data.pop('coords')
        images_data = validated_data.pop('img')
        Coords.objects.create(pereval=pereval, **coords_data)
        for image_data in images_data:
            image = Images.objects.create(**image_data)
            Images.objects.create(foto=image, pereval=pereval)
        return pereval

class PerevalSerializer(serializers.ModelSerializer):
    # connects = serializers.CharField(source='connects', label='Connects', allow_blank=True)
    coords = CoordSerializer()
    user = UserSerializer()
    images = ImagesSerializer(source = 'photos', many=True)
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
                 'images'
                  ]
        read_only_fields = [
           'id',
           'add_time',
        ]

    def create(self, validated_data):
        coords = validated_data.pop('coords')
        user = validated_data.pop('user')
        weather = validated_data.pop('weather')
        levels = validated_data.pop('level')
        images = validated_data.pop('images')
        try:
            user_instance = User.objects.filter(email=user['email']).first()
            if not user_instance:
                user_instance = User.objects.create(**user)
            coords_instance = Coords.objects.create(**coords)
            pereval_instance = Pereval.objects.create(
                user=user_instance,
                coords=coords_instance,
                **validated_data
            )
            for image in images:
                Images.objects.create(pereval=pereval_instance, **image)
            return pereval_instance
        except OperationalError:
            raise DBConnectException()

    def update(self, instance, validated_data):
        coords = validated_data.pop('coords', None)
        user = validated_data.pop('user', None)
        images = validated_data.pop('pereval_images', None)
        try:
            # in case when user should be modifiable or replaceable
            # if user:
            #     email = user.get('email')
            #     if email:
            #         instance.user, created = MPassUser.objects.get_or_create(email=email)
            #     else:
            #         email = instance.user.email
            #     MPassUser.objects.filter(email=email).update(**user)
            if coords:
                coords_fields = model_to_dict(instance.coords)
                coords_unit = {**coords_fields, **coords}
                coords_unit.pop('id', None)
                coords_instance, created = Coords.objects.get_or_create(**coords_unit)
                instance.coords = coords_instance
            # if images:
            #     Image.objects.filter(mpass=instance).delete()
            #     for image in images:
            #         Image.objects.create(mpass=instance, **image)
            return super().update(instance, validated_data)
        except OperationalError:
            raise DBConnectException()