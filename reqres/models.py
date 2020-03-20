from django.db import models
class Searchres(models.Model):
    hashtag=models.CharField(max_length=100)
    positive=models.FloatField(default=0)
    negative=models.FloatField(default=0)
    postweet1 = models.CharField(max_length=1000, default='')
    postweet2 = models.CharField(max_length=1000, default='')
    negtweet1 = models.CharField(max_length=1000, default='')
    negtweet2 = models.CharField(max_length=1000, default='')
    tweetcount=models.IntegerField(default=1000)
    time=models.PositiveIntegerField(default=0)

class Detailed(models.Model):
    hashtag = models.CharField(max_length=100)
    positive=models.FloatField(default=0)
    negative=models.FloatField(default=0)
    dorm = models.PositiveIntegerField(default=0)
    countofdorm = models.PositiveIntegerField(default=0)
    tweetcount = models.IntegerField(default=1000)
    time=models.PositiveIntegerField(default=0)
