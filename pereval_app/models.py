from django.db import models

from django.contrib.auth.models import AbstractUser

STATUS_CHOICES = [
    ("new", "новый"),
    ("pending", "модератор взял в работу"),
    ("accepted", "модерация прошла успешно"),
    ("rejected", "модерация прошла, информация не принята"),
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

class Coords(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    height = models.IntegerField()

class Pereval(models.Model):
    title = models.CharField(max_length=255)
    beautyTitle = models.CharField(max_length=255)
    other_titles = models.CharField(max_length=255)
    connects = models.CharField(verbose_name='pass connects', max_length=255)
    coords = models.ForeignKey(Coords, null=True, on_delete=models.CASCADE)

    level_winter = models.CharField(max_length=255, null = True, blank = True)
    level_summer = models.CharField(max_length=255, null = True, blank = True)
    level_autumn = models.CharField(max_length=255, null = True, blank = True)
    level_spring = models.CharField(max_length=255, null = True, blank = True)

    latitude = models.FloatField()
    longitude = models.FloatField()
    height = models.IntegerField()

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="new")
    add_time = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class PerevalAreas(models.Model):
    pereval = models.ForeignKey(Pereval, on_delete=models.CASCADE, related_name="areas")
    title = models.TextField()

def pereval_directory_path(instance, filename):
    return os.path.join(f'pereval_{instance.pereval.id}', filename)

class Images(models.Model):
    pereval = models.ForeignKey(Pereval, on_delete=models.CASCADE, related_name="photos")
    title = models.CharField(max_length=255)
    date_added = models.DateField(auto_now_add=True)
    img = models.ImageField(upload_to=pereval_directory_path)

    def __str__(self):
        return f"id: {self.pk}, title:{self.title}"
