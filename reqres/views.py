from django.shortcuts import render
from django.http import HttpResponse
from .models import Searchres
from .models import Detailed
from django.http import JsonResponse
from json import JSONEncoder
import json
import re
import tweepy
from datetime import timedelta
from tweepy import OAuthHandler
from textblob import TextBlob
from datetime import datetime
import preprocessor as p
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyser = SentimentIntensityAnalyzer()


def sentiment_analyzer_scores(sentence):
    score = analyser.polarity_scores(sentence)
    if score['compound']<=-0.01:
        return -1
    if score['compound']>=0.01:
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
def monthret(x):
    if x==1:
        return 'jan'
    if x==1:
        return 'Feb'
    if x==1:
        return 'Mar'
    if x==1:
        return 'Apr'
    if x==1:
        return 'May'
    if x==1:
        return 'june'
    if x==1:
        return 'july'
    if x==1:
        return 'Aug'
    if x==1:
        return 'Sept'
    if x==1:
        return 'Oct'
    if x==1:
        return 'Nov'
    if x==1:
        return 'Dec'

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

    def simfetching_tweets(self, query,type=0, count=100):
        msgs = []
        i=1
        if type == 0 :
            try:
                for tweet in tweepy.Cursor(self.api.search, lang='en', count=100, q=query).items(count):
                    print(i)
                    i = i + 1
                    msgs.append(tweet)
            except:
                pass
            return msgs


    def simget_tweets(self, query,type=0, count=100):

        tweets = []

        try:

            fetched_tweets=self.simfetching_tweets(query,type,count)
            for tweet in fetched_tweets:

                parsed_tweet = {}
                parsed_tweet['status'] = f'https://twitter.com/{tweet.user.screen_name}/status/{tweet.id}'
                y = self.clean_tweet(tweet.text)
                parsed_tweet['text'] = y
                parsed_tweet['sentiment'] = sentiment_analyzer_scores(y)
                if tweet.retweet_count > 0:
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)

            return tweets

        except tweepy.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))
    def detfetching_tweets(self, query ,until,since ,type=0, count=100):
        msgs = []
        i=1
        if type == 0 :
            try:
                for tweet in tweepy.Cursor(self.api.search,until =until,since =since, lang='en', count=100, q=query).items(count):
                    print(i)
                    i = i + 1
                    msgs.append(tweet)
            except:
                pass
            return msgs

    def detget_tweets(self, query,until,since ,type=0, count=100):
        tweets = []
        try:
            fetched_tweets = self.detfetching_tweets(query,until,since, type, count)
            for tweet in fetched_tweets:

                parsed_tweet = {}
                parsed_tweet['status'] = f'https://twitter.com/{tweet.user.screen_name}/status/{tweet.id}'
                y = self.clean_tweet(tweet.text)
                parsed_tweet['text'] = y
                parsed_tweet['sentiment'] = sentiment_analyzer_scores(y)
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
            tweets = api.simget_tweets(query=hashtag2 ,type=0, count=tweetcounting)
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
def detailedanalysis(request):
    api = TwitterClient()
    if request.method == 'GET':
        hashtag1 = request.GET['hashtag']
        hashtag2 = '#' + hashtag1
        dorm = int(request.GET['dorm'])
        countofdorm = 6
        try:
            countofdorm = int(request.GET['countofdorm'])
        except:
            pass
        tweetcounting = 100
        try:
            tweetcounting = int(request.GET['tcount'])
        except:
            pass
        resobj = Detailed(hashtag=hashtag1, time=to_integer(datetime.now()), tweetcount=tweetcounting, dorm=dorm,countofdorm=countofdorm,positive=0,negative=0)
        tcountp=0
        tcountn=0
        ttcount=0
        label = []
        count = []
        poslist = []
        neglist = []
        postweet = []
        negtweet= []
        if dorm == 0:
            x = datetime.today()
            for i in range(countofdorm):
                edate = x - timedelta(days=i)
                sdate = x - timedelta(days=i+1)
                tweets = api.detget_tweets(query=hashtag2, type=0,until=edate.strftime('%Y-%m-%d'),since=sdate.strftime('%Y-%m-%d') ,count=tweetcounting)
                positive = 0
                negative = 0
                if len(tweets) > 0:
                    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 1]
                    positive = 100 * len(ptweets) / len(tweets)
                    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == -1]
                    negative = 100 * len(ntweets) / len(tweets)

                label.append(edate.strftime('%d/%m'))
                count.append(len(tweets))
                poslist.append(positive)
                neglist.append(negative)
                ttcount+=len(tweets)
                tcountp+=len(ptweets)
                tcountn+=len(ntweets)
                if i == 0:
                    try:
                        postweet.append(ptweets[len(ptweets) - 1]['status'])
                    except:
                        pass
                    try:
                        negtweet.append(ntweets[len(ntweets) - 1]['status'])
                    except:
                        pass
                    try:
                        postweet.append(ptweets[len(ptweets) - 2]['status'])
                    except:
                        pass
                    try:
                        negtweet.append(ntweets[len(ntweets) - 2]['status'])
                    except:
                        pass
        if ttcount>0:
            resobj.positive = 100 * tcountp / ttcount
            resobj.negative = 100 * tcountn / ttcount
            resobj.save()

        return {"hashtage": hashtag1, 'positive': resobj.positive, 'negative': resobj.negative,
             'tweetcount': ttcount, "time": resobj.time, "label":label , "count":count, "poslist":poslist, "neglist":neglist , 'postweet':postweet, "negtweet":negtweet}


def index(request):

    print(request.GET['hashtag'])
    print(to_integer(datetime.now()))
    res=''
    if request.method == 'GET':
        reqtype = 0
        try:reqtype = int(request.GET['type'])
        except:pass
        if reqtype==1:
            res = detailedanalysis(request)
        else:
            res = simpleanalysis(request)
    print(res)
    response = HttpResponse(json.dumps(res))
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Methods'] = 'GET'
    return response








