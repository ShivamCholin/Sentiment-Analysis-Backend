# Generated by Django 3.0.4 on 2020-03-28 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reqres', '0007_searchres_photo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='searchres',
            name='photo',
        ),
        migrations.AddField(
            model_name='searchres',
            name='negwc',
            field=models.CharField(default='', max_length=1000000),
        ),
        migrations.AddField(
            model_name='searchres',
            name='poswc',
            field=models.CharField(default='', max_length=1000000),
        ),
    ]
