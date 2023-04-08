from django.db import models
import os

from django.contrib.auth.models import AbstractUser

STATUS_CHOICES = [
    ("new", "новый"),
    ("pending", "модератор взял в работу"),
    ("accepted", "модерация прошла успешно"),
    ("rejected", "модерация прошла, информация не принята"),
]

WEATHER_CHOICES = [
    ('winter', 'зима'),
     ('spring', 'весна'),
     ('summer', 'лето'),
     ('autumn', 'осень')
]

LEVEL_CHOICES = [
    ('1A', '1A'),
    ('1Б', '1Б'),
    ('2А', '2А'),
    ('2Б', '2Б'),
    ('3А', '3А'),
    ('3Б', '3Б')
]

class User(AbstractUser):
    name = models.CharField(verbose_name='имя', max_length=255)
    surname = models.CharField(verbose_name='фамилия', max_length=255)
    patronymic = models.CharField(verbose_name='отчество',
                                max_length=255,
                                null=True,
                                blank=True)
    phone = models.CharField(verbose_name='телефон',
                             max_length=20,
                             null=True,
                             blank=True)
    email = models.EmailField(verbose_name='e-mail', unique=True, max_length=255)

    class Meta:
        db_table = 'auth_user'

    def save(self, *args, **kwargs):
        if not self.pk:
            self.username = self.email
        super(User, self).save(*args, **kwargs)

class Coords(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    height = models.IntegerField()

class Pereval(models.Model):
    title = models.CharField(max_length=255)
    beautyTitle = models.CharField(max_length=255)
    other_titles = models.CharField(max_length=255)
    connects = models.CharField(verbose_name='pass connects', max_length=255)
    coords = models.ForeignKey(Coords,
                               null=True,
                               on_delete=models.CASCADE,
                               related_name = "coords_pereval"
                               )
    weather = models.CharField(max_length=10,
                               choices=WEATHER_CHOICES,
                               null = True,
                               blank = True
                               )
    level = models.CharField(max_length=2, choices=LEVEL_CHOICES, null = True, blank = True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="new")
    add_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_pereval")


def pereval_directory_path(instance, filename):
    return os.path.join(f'pereval_{instance.pereval.id}', filename)

class Images(models.Model):
    pereval = models.ForeignKey(Pereval, on_delete=models.CASCADE, related_name="photos")
    title = models.CharField(max_length=255)
    date_added = models.DateField(auto_now_add=True)
    img = models.ImageField(null=True, blank = True, upload_to=pereval_directory_path)

    def __str__(self):
        return f"id: {self.pk}, title:{self.title}"
