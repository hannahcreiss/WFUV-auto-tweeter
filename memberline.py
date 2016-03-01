from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import tweepy
import re
import datetime

def formatTweet(show):
    regexp = re.compile('(new\s?dig)', re.IGNORECASE)
    match = re.search(regexp, show.h3.text)
    what = show.h3.text.strip()
    date = datetime.datetime.now().strftime("%-m/%-d")
    tweet = ("MEMBERLINE %s: " % date)
    # if offer is a new dig
    if match is not None:
        tweet += show.h3.text + "! #wfuv @wfuv"
    else:
        location = show.findAll("p")[1].text
        where = re.split('\s?[\(:-]\s?[0-9]', location)[0]    
        when = show.findAll("p")[0].text.split(' at')[0]
        tweet += what + " at " + where + " on " + when + "! #livemusic #wfuv @wfuv"
    if (140-len(tweet)<0):    
        days = ["Friday, ", "Saturday, ", "Sunday, ", "Monday, ", "Tuesday, ", "Wednesday, ", "Thursday, "]
        for day in days:
            if day in tweet:
                tweet = tweet.replace(day, '')
                break       
    if (140-len(tweet)<0):
        tweet = tweet.replace('#livemusic ','')
    
    return tweet          


def getShows(url, api):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    data = urlopen(req).read()
  
    soup = BeautifulSoup(data,'html.parser')

    for s in soup.findAll('script'):
        s.replaceWith('')
    shows = soup("article", { "class" : re.compile(r"(odd)|(even)") })
    tweets = []
    for show in shows:
        api.update_status(formatTweet(show))

def main():
    url = "http://www.wfuv.org/content/member-line-offers"

    auth = tweepy.OAuthHandler("CONSUMER_KEY", "CONSUMER_SECRET")

    auth.set_access_token("ACCESS_KEY", "ACCESS_TOKEN")

    api = tweepy.API(auth)

    getShows(url, api)


if __name__=="__main__":
    main()