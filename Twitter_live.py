# -*- coding: utf-8 -*-
"""
Created on Mon Feb 11 19:48:36 2019

@author: Jerod


Twitter pull RDT
"""

import time
from datetime import datetime
import tweepy
from pygame import mixer
from gtts import gTTS
from api_keys import consumer_key, consumer_secret, access_token, access_token_secret


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

class TwitterPull:
    def __init__(self, handle = "RealDonaldTrump", first = 0):
        self._handle = handle
        self._a = None
        self._b = None
        self._stat = None
        self._first = first
        
    def pull(self):
        """Function to refresh and check for updates; get_user refreshes data.
        If user tweets, then the counter updates and plays a sound notification."""
        read = []
        User = api.get_user(self._handle) 
        if User.statuses_count == self._stat:
            pass
        else:
            diff = User.statuses_count - self._stat
            self._stat = User.statuses_count
            text = "New tweet from " + self._handle + "! Currently at " + str(self._stat - self._first)
            print(self._timerefresh(), text)
            tts = gTTS(text)
            tts.save("RDTs.mp3")
            self.play("RDTs.mp3")
            
            for tweet in tweepy.Cursor(api.user_timeline, id="realdonaldtrump", tweet_mode = "extended").items(diff):
                read.append(tweet)
            read.reverse()
            tts = gTTS("".join(read))
            tts.save("Trumptext.mp3")
            self.play("Trumptext.mp3")
            
            
    def sleep(self, t = 60):
        """Sleep t seconds."""
        time.sleep(t)
    
    def play(self, file):
            mixer.init()
            mixer.music.load(file)
            mixer.music.play()
    
    def _timerefresh(self):
        """Refresh the current time, Return a timestamp string: day/hour/min
        Ex:
            '02/05 19:49'
        """
        timestamp = datetime.now().strftime('%m/%d %H:%M')
        return timestamp
            
    
    def continuouspull(self, n = 60*12*3):
        #default: half a day
        User = api.get_user("RealDonaldTrump"); self._stat = User.statuses_count

        print(str(User.statuses_count) + " currently.")

        for i in range(n):
            try:
                self.pull()
            except:
                input("pull failed.." + str(self._timerefresh()))
            self.sleep(20)

