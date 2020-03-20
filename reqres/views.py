from django.shortcuts import render
from django.http import HttpResponse
from .models import Searchres
from .models import Detailed
from django.http import JsonResponse
from json import JSONEncoder
import json
import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
from datetime import datetime
import preprocessor as p
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyser = SentimentIntensityAnalyzer()


def sentiment_analyzer_scores(sentence):
    score = analyser.polarity_scores(sentence)
    if score['compound']<=-0.05:
        return -1
    if score['compound']>=0.05:
        return 1
    else:
        return 0
def to_dictsim(x):
    l1=[]
    l2=[]
    try:
        l2.append(x.postweet1)
        l1.append(x.negtweet1)
        l2.append(x.postweet2)
        l1.append(x.negtweet2)
    except:
        pass
    y = { "hashtage": x.hashtag, 'positive':x.positive,'negative':x.negative,'negtweet':l1,'postweet':l2,'tweetcount':x.tweetcount,"time":x.time}
    return y
#resobj = Searchres(hashtag='',time=0,positive=0,negative=0,postweet=[],negtweet=[],tweetcount=0)
#detres = Detailed(hashtag='',poslist = [],neglist = [],postweet = [],negtweet = [],tweetcountl=0,dorm=0,countofdorm=0,label=[])
#test for github

class ObjectEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

def to_integer(dt_time):
    return 1000000*dt_time.year + 10000*dt_time.month + 100*dt_time.day +  4*dt_time.hour +int(dt_time.minute/15)

class TwitterClient(object):

    def __init__(self):

        consumer_key = "npoB5bsWEjCvZVniYnQJFRqmE"
        consumer_secret = "pUCNx7zmP6dvlG0TOApM347fx2KJZuqXSlhBnkdmKB69cAuxRs"
        access_token = "793737675115081728-uyy6IDIAI4TICd1dTKnqkOkOxCmPLQc"
        access_token_secret = "J6J2MR3gdvpY2wKclIa21iZTJx4Y8FCUm5wandFRP0IkV"


        try:

            self.auth = OAuthHandler(consumer_key, consumer_secret)

            self.auth.set_access_token(access_token, access_token_secret)

            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")

    def clean_tweet(self, tweet):
        p.set_options(p.OPT.URL)
        x=p.clean(tweet)
        return x.replace('#', '')

    def fetching_tweets(self, query,type=0, count=100):
        msgs = []
        i=1
        if type == 0 :
            try:
                for tweet in tweepy.Cursor(self.api.search, lang='en', count=1000, q=query).items(count):
                    print(i)
                    i = i + 1
                    msgs.append(tweet)
            except:
                pass
            return msgs


    def get_tweets(self, query,type=0, count=100):
        

        tweets = []

        try:

            fetched_tweets=self.fetching_tweets(query,type,count)
            for tweet in fetched_tweets:

                parsed_tweet = {}
                parsed_tweet['status'] = f'https://twitter.com/{tweet.user.screen_name}/status/{tweet.id}'
                parsed_tweet['text'] = self.clean_tweet(tweet.text)
                parsed_tweet['sentiment'] = sentiment_analyzer_scores(tweet.text)

                if tweet.retweet_count > 0:
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)

            return tweets

        except tweepy.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))


def simpleanalysis(request):

    api = TwitterClient()
    if request.method == 'GET':
        hashtag1 = request.GET['hashtag']
        tweetcounting = 100
        try:
            tweetcounting = int(request.GET['tcount'])
        except:
            pass
        j = -1
        searchress = Searchres.objects.all().order_by('-time')
        for i in range(0, searchress.count()):
            if searchress[i].hashtag == hashtag1:
                j = i
                time1 = int(to_integer(datetime.now()))
                diff = time1 - searchress[j].time
                if diff >= 1:
                    j = -1
                break
        if j >= 0:
            resobj1 = searchress[j]
            return to_dictsim(resobj1)

        else:
            hashtag2 = '#' + hashtag1
            resobj = Searchres(hashtag='', time=0, positive=0, negative=0, tweetcount=0)
            resobj.hashtag = hashtag1
            time = datetime.now()
            tweets = api.get_tweets(query=hashtag2 ,type=0, count=tweetcounting)
            resobj.positive=0
            resobj.negetive=0
            if len(tweets) > 0:
                ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 1]
                resobj.positive = 100 * len(ptweets) / len(tweets)
                ntweets = [tweet for tweet in tweets if tweet['sentiment'] == -1]
                resobj.negative = 100 * len(ntweets) / len(tweets)
                try:
                    resobj.postweet1 = ptweets[len(ptweets)-1]['status']
                except:
                    pass
                try:
                    resobj.negtweet1 = ntweets[len(ntweets) - 1]['status']
                except:
                    pass
                try:
                    resobj.postweet2 = ptweets[len(ptweets) - 2]['status']
                except:
                    pass
                try:
                    resobj.negtweet2 = ntweets[len(ntweets) - 2]['status']
                except:
                    pass

            resobj.time = to_integer(datetime.now())
            resobj.tweetcount = len(tweets)
            resobj.save()
            resobj1 = to_dictsim(resobj)
            return resobj1
def index(request):

    print(request.GET['hashtag'])
    print(to_integer(datetime.now()))
    res=''
    if request.method == 'GET':
        reqtype = 0
        try:reqtype = request.GET['type']
        except:pass
        if reqtype==1:
            pass #detailedanalysis(request)
        else:
            res = simpleanalysis(request)
    print(res)
    response = HttpResponse(json.dumps(res))
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Methods'] = 'GET'
    return response








