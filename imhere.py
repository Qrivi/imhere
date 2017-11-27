#!/usr/bin/python
# -*- coding: utf-8 -*-

from apscheduler.schedulers.blocking import BlockingScheduler
import argparse
import time
import json
import mechanize
import twitter

def fetch():
    url = br.open(sheet).read()
    br.open(url)

    fid = br.geturl()[-24:]
    api = 'https://api.foursquare.com/v2/venues/' + fid \
        + '?client_id=' + args.fid + '&client_secret=' + args.fsecret + '&v=' + date

    data = json.loads(br.open(api).read())
    name = data['response']['venue'].get('name').encode('utf-8')
    address = data['response']['venue']['location'].get('address').encode('utf-8')
    crossstreet = data['response']['venue']['location'].get('crossStreet').encode('utf-8')
    city = data['response']['venue']['location'].get('city').encode('utf-8')
    postalcode = data['response']['venue']['location'].get('postalCode').encode('utf-8')
    countrycode = data['response']['venue']['location'].get('cc').encode('utf-8')
    country = data['response']['venue']['location'].get('country').encode('utf-8')
    coordinates = str(data['response']['venue']['location'].get('lat')) \
        + ',' + str(data['response']['venue']['location'].get('lng'))

    output = formatter.format( n = name,
        a = address,
        x = crossstreet,
        t = city,
        p = postalcode,
        s = countrycode,
        c = country,
        o = coordinates,
        u = url)

    tw.UpdateProfile(location = output)
    print time.strftime('[%H:%M:%s]'), output

parser = argparse.ArgumentParser('Updates your Twitter profile location with data from your last Swarm check-in.')
parser.add_argument('--sid', type = str,
                    metavar = 'Google Sheet ID',
                    help = 'The Google Sheet containing the venue url of your last Swarm check-in',
                    required = True)
parser.add_argument('--fid', type = str,
                    metavar = 'Foursquare Client ID',
                    help = 'Your Foursquare application Client ID',
                    required = True)
parser.add_argument('--fsecret', type = str,
                    metavar = 'Foursquare Client Secret',
                    help = 'Your Foursquare application Client Secret',
                    required = True)
parser.add_argument('--tkey', type = str,
                    metavar = 'Twitter Consumer Key',
                    help = 'Your Twitter application Consumer Key',
                    required = True)
parser.add_argument('--tsecret', type = str,
                    metavar = 'Twitter Consumer Secret',
                    help = 'Your Twitter application Consumer Secret',
                    required = True)
parser.add_argument('--atoken', type = str,
                    metavar = 'Twitter Access Token',
                    help = 'Your pregenerated Twitter Access Token',
                    required = True)
parser.add_argument('--asecret', type = str,
                    metavar = 'Twitter Access Token Secret',
                    help = 'Your pregenerated Twitter Access Token Secret',
                    required = True)
parser.add_argument('--output', type = str,
                    metavar = 'Output string format',
                    help = '{n} prints venue name, {a} address, {x} cross street, {t} city, {p} postal code, {c} country, {s} country code, {o} coordinates and {u} url',
                    required = False,
                    default = '{t}, {c}')
parser.add_argument('--repeat', type = int,
                    metavar = 'Repeat interval',
                    help = 'Delay (in minutes) until next automatic execution of the script',
                    default = 0)
args = parser.parse_args()

formatter = args.output
date = time.strftime('%Y%m%d')
sheet = 'https://docs.google.com/spreadsheets/d/e/' + args.sid \
    + '/pub?gid=0&single=true&output=csv'

br = mechanize.Browser()
tw = twitter.Api(consumer_key = args.tkey,
                 consumer_secret = args.tsecret,
                 access_token_key = args.atoken,
                 access_token_secret = args.asecret)

print 'Location format has been set to:', formatter

if args.repeat > 0:
    print 'Location will update every', args.repeat, 'minutes'
    fetch()

    scheduler = BlockingScheduler()
    scheduler.add_job(fetch, 'interval', minutes = args.repeat)
    scheduler.start()
else:
    print 'Location will be updated only once'
    fetch()
