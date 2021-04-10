#!/usr/bin/env python
# coding: utf-8
#
# This source code is distributed under the terms of the Bad Code License.
# You are forbidden to distribute software containing this code to end users, because it is bad.
#
#
# The_eye_loop:
#    This is bad and you should feel bad about it
# Mr P:
#    Lucas qué hiciste
#    LUCAS QUE HICISTE PORFAVOR PARALOOOAAAAAAAA
#    You need to stop.
# Meggg:
#    Por que hiciste esto
# Luxter77:
#    Por que hice esto

from tempfile import SpooledTemporaryFile as EphFile
from bs4 import BeautifulSoup as bs4
from typing import Generator, Callable, Union, Any, Tuple, List
from urllib.request import urlopen
from urllib.parse import urlencode
from dateutil import parser
from tqdm.auto import tqdm
from pprint import pprint
from uwuify import uwu

import requests as req
import datetime as dt
import dateutil as du
import tweepy as tw
import random as rd
import pickle as pk

import unicodedata
import contextlib
import tweepy
import time
import math
import pytz
import sys
import os


from secrets import api_token, user


def loadprogress() -> dt.datetime: # Try to load last saved progress, else start from scratch
    try:
        return(pk.load(open('last_time', 'rb')))
    except pk.UnpicklingError:
        return(pk.load(open('last_time.bkp', 'rb')))
    except FileNotFoundError:
        return(pytz.utc.localize(dt.datetime.now()), [])


def saveprogress(last_time: dt.datetime, done: List[dt.datetime]) -> None:
    pk.dump((last_time, done,), open('last_time', 'wb'))
    pk.dump((last_time, done,), open('last_time.bkp', 'wb'))


def owo(victim: str, out: str = ''):
    rd.seed(int.from_bytes(bytes(victim.encode()), 'big', signed=True))
    
    for char in uwu(victim):
        if not(char.isalnum()) or char.isnumeric():
            out += char
        elif(char in ['a', 'e', 'i', 'o', 'u']):
            if(16 > rd.randint(0, 100)):
                if (char.islower()):
                    out += 'y' + char
                else:
                    out += 'Y' + char.lower()
            else:
                out += char
        elif(16 > rd.randint(0, 100)):
            out += 'w' if (char.islower()) else 'W'
        else:
            out += char
    
    out.replace('pa', 'paw').replace('Pa', 'Paw')
    
    out += ' ' + rd.choice(['(・`ω´・)', ';;w;;', 'OwO', 'UwU', '>w<', '^w^', 'ÚwÚ', '^-^', ':3', 'x3'])
    
    return(out)


def tiny(url: str) -> str:
    with contextlib.closing(urlopen('http://tinyurl.com/api-create.php?' + urlencode({'url':url}))) as response:
        return response.read().decode('utf-8 ')


def columns() -> bool:
    try:
        return(os.get_terminal_size().columns)
    except OSError:
        return(120)


def get_attrs(soup: bs4):
    try:
        raw_title = soup.find("meta", property="og:title")['content'].split(' - ABC', 1)[0]
        raw_title = raw_title.split(' - ABC', 1)[0].split('La Nación /', 1)[-1].split('| .::', 1)[0]
        nkfd_title = unicodedata.normalize('NFKD', raw_title)
        title = owo(u"".join([c for c in nkfd_title if not unicodedata.combining(c)]))
        
        try:
            description = owo(soup.find("meta", property="og:description")['content'].replace(' - ABC Color', ''))
        except:
            description = '' # meh
        return({
            'title':       title,
            'description': description,
        })
    except Exception as e:
        raise(e)


set_lanacion = set(["Política", "País", "Negocios", "Investigación", "Impreso", "Tendencias", "Judiciales", "Reportaje"])
def get_lanacion(last_time: dt.datetime, done: List[dt.datetime]) -> Generator[dict, None, None]:
    soup = bs4(req.get("https://www.lanacion.com.py/arcio/sitemap/").content, "xml")
    for url in tqdm(soup.findAll('url'), leave=True, desc="Reading La Nacion"):
        art_time = du.parser.parse(url.lastmod.text)
        if(art_time.date() == dt.date.today()) and (art_time > last_time) and not(art_time in done):
            #if(rd.random() < .85):
            #    continue # 50% probability of not tweeting the ting
            try:
                article = get_attrs(bs4(req.get(url.loc.text).content, "html.parser"))
                article['url']  = tiny(url.loc.text)
                article['date'] = art_time
                yield(article)
            except Exception as e:
                continue


def get_ultimahora(last_time: dt.datetime, done: List[dt.datetime]) -> Generator[dict, None, None]:
    soup = bs4(req.get("https://www.ultimahora.com/sitemap.xml").content, "xml")
    for url in tqdm(soup.findAll('url'), leave=True, desc='Reading Ultima Hora'):
        art_time = du.parser.parse(url.lastmod.text)
        if(art_time.date() == dt.date.today()) and (art_time > last_time) and not(art_time in done):
            #if(rd.random() < .85):
            #    continue # 85% probability of not tweeting the ting
            try:
                article = get_attrs(bs4(req.get(url.loc.text).content, "html.parser"))
                article['url']  = tiny(url.loc.text)
                article['date'] = art_time
                yield(article)
            except Exception as e:
                continue


set_abc = set(['este', 'nembeweb', 'empresariales', 'internacionales', 'nacionales', 'deportes', 'edicion-impresa'])
def get_abc(last_time: dt.datetime, done: List[dt.datetime]) -> Generator[dict, None, None]:
    soup = bs4(req.get("https://www.abc.com.py/arcio/sitemap/").content, "xml")
    for url in tqdm(soup.findAll('url'), leave=True, desc="Reading ABC"):
        #if not(set(url.text.split('/')).isdisjoint(set_abc)):
        #    continue
        art_time = du.parser.parse(url.lastmod.text)
        if(art_time.date() == dt.date.today()) and (art_time > last_time) and not(art_time in done):
            if(rd.random() < .85):
                continue # 85% probability of not tweeting the ting
            try:
                article = get_attrs(bs4(req.get(url.loc.text).content, "html.parser"))
                article['url']  = tiny(url.loc.text)
                article['date'] = art_time
                yield(article)
            except Exception as e:
                tqdm.write(str(e))
                continue


def get_ip(last_time: dt.datetime, done: List[dt.datetime]) -> Generator[dict, None, None]:
    proto_soup  = bs4(req.get("https://www.ip.gov.py/ip/sitemap_index.xml").content, "xml")
    latest_date = pytz.utc.localize(dt.datetime(2005, 10, 10, 0, 0)) # MLP: FIM is released
    for sitemap in proto_soup.findAll('sitemap'):
        if('post-sitemap' in sitemap.loc.text.split('/')[-1]):
            if(latest_date < du.parser.parse(sitemap.lastmod.text)):
                latest_site = sitemap.loc.text
    soup = bs4(req.get(latest_site).content, "xml")
    for url in tqdm(soup.findAll('url'), leave=True, desc="Reading IP"):
        art_time = du.parser.parse(url.lastmod.text)
        if(art_time.date() == dt.date.today()) and (art_time > last_time) and not(art_time in done):
            #if(rd.random() < .85):
            #    continue # 85% probability of not tweeting the ting
            try:
                article = get_attrs(bs4(req.get(url.loc.text).content, "html.parser"))
                article['url']  = tiny(url.loc.text)
                article['date'] = art_time
                yield(article)
            except:
                continue


def get_articles(last_time: dt.datetime, done: List[dt.datetime], _wait: bool = True):
    while _wait:
        try:
            ultimahora = list(get_ultimahora(last_time, done))
            abc        = list(get_abc(last_time, done))
            latancion  = list(get_lanacion(last_time, done))
            ip         = list(get_ip(last_time, done))

            articles = (abc + latancion + ip + ultimahora)
            
            assert len(articles) != 0
            
            _wait = False
        except AssertionError:
            tqdm.write(' There are no news! '.center(columns(), '*'))
            wait_for(1000)

    articles = sorted(articles, key=lambda k: k['date'])
    
    return(articles)


def wait_for(t: float):
    try:
        for _ in tqdm(range(100), desc=f'Waiting for ~{str(int(t))}s', leave=False):
            time.sleep(t / 100)
    except KeyboardInterrupt:
        pass  # let us continue

def do_the_thing(last_time: dt.datetime, done: List[dt.datetime]):

    this_time = pytz.utc.localize(dt.datetime.now())

    articles  = get_articles(last_time, done)

    narticles = len(articles)
    time_mod = (1800 / max(100, min(10, math.sqrt(narticles)*narticles + narticles)))

    try:
        for headline in tqdm(articles, desc="Tweeting... "):
            head = (headline['title'] + '\n\n' + headline['url'])
                
            if (len(head) > 279):
                head = ''.join(
                    headline['title'][:(279 - len(headline['title'] + '...' + headline['url']))]
                ).rstrip(' ') + '…\n\n' + headline['url']
    
            try:
                twitter_api.update_status(head)
                
                tqdm.write('\n' + ' Tweet '.center(columns(), '-'))
                tqdm.write('\n' + str(headline['date']) + '\n')
                tqdm.write(head.center(columns(), ' '))
                
                done.append(headline['date'])
                saveprogress(headline['date'], done)
            except tweepy.TweepError as te:
                if  (te.api_code == 187): # You already tweeted that
                    done.append(headline['date'])
                elif(te.api_code == 429): # Too many requests
                    time.sleep(10 * 60)
                elif(te.api_code == 186): # Tweet is too long
                    raise # Something is wrong with the code!
                else:
                    tqdm.write(str(te))
                continue
            except Exception as e:
                raise
            wait_for(time_mod)
    except KeyboardInterrupt:
        saveprogress(headline['date'], done)
        raise
    return(this_time, done)


twitter_auth = tweepy.OAuthHandler(api_token['access'], api_token['secret'])
twitter_api  = tweepy.API(twitter_auth)

twitter_auth.set_access_token(user["access"], user["secret"])


print(f"Account ID: {str(twitter_api.me()._json['id'])}")
print(f"Username:   {twitter_api.me()._json['name']}")

# guess who has bad ideas and implements them badly
global last_time
global done

last_time, done = loadprogress()

def main(ilast_time: dt.datetime = False):
    # you guessed right, it's me
    global done
    if not(bool(ilast_time)):
        global last_time
    else:
        last_time = ilast_time

    try:
        while True:
            saveprogress(last_time, done)
            print(f'Last run was on {str(last_time)}\nNow is: {str(pytz.utc.localize(dt.datetime.now()))}')
            last_time, done = do_the_thing(last_time, done)
    except KeyboardInterrupt:
        print('Interrupted')
    except Exception as e:
        raise # print(e)

if __name__ == '__main__':
    main(last_time)
