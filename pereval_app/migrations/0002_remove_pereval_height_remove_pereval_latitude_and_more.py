# Generated by Django 4.2 on 2023-04-05 12:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pereval_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pereval',
            name='height',
        ),
        migrations.RemoveField(
            model_name='pereval',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='pereval',
            name='longitude',
        ),
        migrations.DeleteModel(
            name='PerevalAreas',
        ),
    ]