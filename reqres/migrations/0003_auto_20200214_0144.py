# Generated by Django 3.0.3 on 2020-02-13 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reqres', '0002_auto_20200214_0114'),
    ]

    operations = [
        migrations.AddField(
            model_name='searchres',
            name='tweetcount',
            field=models.IntegerField(default=1000),
        ),
        migrations.AlterField(
            model_name='searchres',
            name='time1',
            field=models.IntegerField(default=0),
        ),
    ]
