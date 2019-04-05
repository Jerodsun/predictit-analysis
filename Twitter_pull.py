# -*- coding: utf-8 -*-
"""
Created on Feb 17

@author: Jerod

Vertical pull for data analysis

"""
from datetime import timedelta
import tweepy
import matplotlib.pyplot as plt
import numpy as np
import pickle

#Obtain your consumer_key, consumer_secret, access_token, access_token_secret from Twitter Oauth
from api_keys import consumer_key, consumer_secret, access_token, access_token_secret

handle = "realDonaldTrump"


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
User = api.get_user(handle)


def picklesave(l, filename = "Pickle.p"):
    """Save to pickle file for reference"""
    with open(filename, "wb") as fp:
        pickle.dump(l, fp)
    
def pickleread(filename = "Pickle.p"):
    """Read from pickle file"""
    r = pickle.load(open(filename, "rb"))
    return r

#-------------------- backend methods ------------------------------#
def htweet():
    """Get maximum 3200 tweets from twitter. Return as list with type Status"""
    alltweets = []
    for tweet in tweepy.Cursor(api.user_timeline,id=handle).items():
        alltweets.append(tweet)
    return alltweets


def extractdt(l):
    """Extract datetime list from htweet list, return as list. Time in EST"""

    dt = []
    for i in l:
        obj = i.created_at
        EST = obj - timedelta(hours=5)
        dt.append(EST)
    return dt

def pullplot():
    """Get historical tweets, extract date"""
    m = htweet()
    k = extractdt(m)
    k.sort()
    return k
#------------------- Extraneous Functions -----------------------#
        
        
def dateonly(l):
    """Make datetime list a date-only list"""
    d = []
    for i in l:
        d.append(i.date())
    return d
        
def timeonly(l):
    """Make datetime list a time-only list"""
    t = []
    for i in l:
        t.append(i.time())
    
    return t
    
def extracttime(l):
    """Make datetime list format in range 0.0 to 24
    ex. 16:32am = 16.5333..."""
    hourstore = []
    for i in l:
        hourstore.append(i.hour + i.minute / 60)
    
    return hourstore

#----------------------------------------------------------------#

def plotit(list):
    """Plot as step... reverses x and y axis"""
    list.sort() #always make sure sorted?
    x = np.asarray(list)
    y = np.arange(len(list))
    fig, ax = plt.subplots()
    plt.xlabel("Time (Wednesday 12pm to Wednesday 12pm)")
    plt.ylabel("Tweet count")
    plt.step(x, y)
    for label in ax.get_xticklabels()[::2]:
        label.set_visible(False)

def plotit2(list):
    """Plot function as dot... reverses x and y axis"""
    list.sort() #always make sure sorted?
    x = np.asarray(list)
    y = np.arange(len(list))
    fig, ax = plt.subplots()
    plt.xlabel("Time (Wed to Wed 12pm)")
    plt.ylabel("Tweet count")
    plt.plot(x, y, 'b.')
    for label in ax.get_xticklabels()[::2]:
        label.set_visible(False)
        
        

def plotit3(list, top = 100):
    """Plot function... reverses x and y axis. Scales each to the top."""
    list.sort() #always make sure sorted?
    x = np.asarray(list)
    y = np.arange(len(list))
    fig, ax = plt.subplots()
    plt.ylim(top = top)
    
    plt.xlabel("Time (Wed to Wed 12pm)")
    plt.ylabel("Tweet count")
    plt.plot(x, y, 'b.')
    for label in ax.get_xticklabels()[::2]:
        label.set_visible(False)

def start(l):
    """Start operation on a preparsed list"""
    for i in range(len(l)):
        plotit(l[i])
        num = "Plot "+ str(i) + ".svg"
        plt.savefig(num, format = 'svg', dpi=600)
        plt.show()
        input("This is plot number " + str(i) + ".")



def barplot(input, bins = 23):
    """Input: hours objects. Goal: frequency of each time
    Use multiples of 24, minus 1"""
    plt.hist(input, bins = bins)
   


def deltatime(data):
    """From datatime list return the time between each tweet"""
    deltastore = []
    for i in range((len(data)) - 1):
        a = data[i+1] - data[i] #timedelta object
        deltastore.append(a.total_seconds())
    
    return deltastore


def separatebydate(l):
    """From data, separate by day of the week"""
    container = [0] * 7
    for i in l:
        index = i.weekday()
        container[index] += 1
    
    return container
    


def wednesdaycount(l):
    """From data, count number of tweets in each wednesday period."""
    container = []
    
    init = l[0] + timedelta(days=( (9 - (l[0].weekday()) % 7) )) # first Wednesday after @ 12pm ET
    init = init.replace(hour=12, minute=0, second = 0)

    start = init
    counter = 0
    for i in range(len(l)):
        if l[i] < start:
            counter += 1
        else:
            container.append(counter)
            counter = 0
            start = start + timedelta(days=7)
    container.append(counter)
    
    del container[0] #not full
    return container


def separatebyweekday(l, weekday = 2):
    """From data, separate into buckets by week. Specify weekday: 0 for Monday, 6 for Sunday. End time always 12pm (EST)."""
    container = []
    
    init = l[0] + timedelta(days=( ((7 + weekday) - (l[0].weekday()) % 7) )) # first @ 12pm ET. If on the day, start from the next week for consistency.
    init = init.replace(hour=12, minute=0, second = 0)

    start = init
    counter = []
    for i in range(len(l)):
        if l[i] < start:
            counter.append(l[i])
        else:
            container.append(counter)
            counter = []
            start = start + timedelta(days=7)
    container.append(counter)
    
    del container[0] #not full
    
    return container
