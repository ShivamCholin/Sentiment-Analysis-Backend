# Generated by Django 3.0.3 on 2020-02-13 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='searchres',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hashtag', models.CharField(max_length=100)),
                ('positive', models.FloatField()),
                ('negetive', models.FloatField()),
                ('positweet1', models.CharField(max_length=2083)),
                ('positweet2', models.CharField(max_length=2083)),
                ('negitweet1', models.CharField(max_length=2083)),
                ('negitweet2', models.CharField(max_length=2083)),
                ('time', models.DateTimeField()),
            ],
        ),
    ]
