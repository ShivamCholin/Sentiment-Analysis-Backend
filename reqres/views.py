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
resobj = Searchres(hashtag='',time=0,positive=0,negative=0,tweetcount=0)
class ObjectEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

class responsejson():
    hashtag=''
    tweetcount=0
    label = []
    positive=0
    negetive=0
    postweet=[]
    negtweet=[]
    poslist=[]
    neglist=[]
    dorm=0
    countofdorm=0
    tweetcountl=[]
    time=0

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
        
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])| (\w+:\ / \ / \S+)", " ", tweet).split())

    def get_tweet_sentiment(self, tweet):
        

        analysis = TextBlob(self.clean_tweet(tweet))

        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'
    def fetching_tweets(self, query,until,since, count=100):
        msgs = []
        i=1
        try:
            for tweet in tweepy.Cursor(self.api.search,lang='en', count=100, q=query, until=until,since=since).items(count):
                print(i)
                i=i+1
                msgs.append(tweet)
        except:
            pass
        return msgs

    def get_tweets(self, query,until,since='2001-01-01', count=100):
        

        tweets = []

        try:

            fetched_tweets=self.fetching_tweets(query,until,since,count)
            for tweet in fetched_tweets:

                parsed_tweet = {}
                parsed_tweet['status'] = f"https://twitter.com/{tweet.user.screen_name}/status/{tweet.id}"
                parsed_tweet['text'] = tweet.text
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)

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
            resobj.hashtag = hashtag1
            time = datetime.now()
            tweets = api.get_tweets(query=hashtag2, until =str(time.year)+'-'+str(time.month)+'-'+str(time.day) ,count=tweetcounting)
            ptweets = []
            ntweets = []
            resobj.positive=0
            resobj.negetive=0
            if len(tweets) > 0:
                ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
                resobj.positive = 100 * len(ptweets) / len(tweets)
                ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
                resobj.negative = 100 * len(ntweets) / len(tweets)
                try:
                    resobj.postweet1 = ptweets[0]['status']
                    resobj.postweet2 = ptweets[1]['status']
                    resobj.negtweet1 = ntweets[0]['status']
                    resobj.negtweet2 = ntweets[1]['status']
                    print(ptweets[0]['status'],ntweets[0]['status'])
                except:
                    pass
            resobj.time = to_integer(datetime.now())
            resobj.tweetcount = len(tweets)
            resobj.save()
            print("helllo", len(tweets))
            print(resobj)
            resobj1 = to_dictsim(resobj)
            return resobj1
def index(request):

    print(request.GET['hashtag'])
    print(to_integer(datetime.now()))
    resobj=''
    if request.method == 'GET':
        reqtype = request.GET['type']
        if reqtype==1:
            pass #detailedanalysis(request)
        else:
            resobj = simpleanalysis(request)
    print(resobj)
    response = HttpResponse(json.dumps(resobj))
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Methods'] = 'GET'
    return response








