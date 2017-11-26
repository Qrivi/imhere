#!/usr/bin/python
# -*- coding: utf-8 -*-

from apscheduler.schedulers.blocking import BlockingScheduler 
import argparse
import time
import json
import mechanize
import twitter

def fetch():
    br.open(br.open(sheet).read())

    fid = br.geturl()[-24:]
    url = 'https://api.foursquare.com/v2/venues/' + fid \
        + '?client_id=' + args.fid + '&client_secret=' + args.fsecret + '&v=' + date

    data = json.loads(br.open(url).read())
    name = data['response']['venue'].get('name')  # n
    address = data['response']['venue']['location'].get('address')  # a
    crossstreet = data['response']['venue']['location'].get('crossStreet')  # x
    city = data['response']['venue']['location'].get('city')  # t
    postalcode = data['response']['venue']['location'].get('postalCode')  # p
    countrycode = data['response']['venue']['location'].get('cc')  # s
    country = data['response']['venue']['location'].get('country')  # c
    coordinates = str(data['response']['venue']['location'].get('lat')) \
        + ',' + str(data['response']['venue']['location'].get('lng'))

    output = formatter.format( n = name,
        a = address,
        x = crossstreet,
        t = city,
        p = postalcode,
        s = countrycode,
        c = country,
        o = coordinates)

    tw.UpdateProfile(location = output)
    print '[', time.strftime('%H:%M:%s'), ']', output

parser = argparse.ArgumentParser()
parser.add_argument('--sid', type=str,
                    help='Google Sheet ID',
                    required=True)
parser.add_argument('--fid', type=str,
                    help='Foursquare Client ID',
                    required=True)
parser.add_argument('--fsecret', type=str,
                    help='Foursquare Client Secret',
                    required=True)
parser.add_argument('--tkey', type=str,
                    help='Twitter Consumer Key',
                    required=True)
parser.add_argument('--tsecret', type=str,
                    help='Twitter Consumer Secret',
                    required=True)
parser.add_argument('--atoken', type=str,
                    help='Twitter Access Token',
                    required=True)
parser.add_argument('--asecret', type=str,
                    help='Twitter Access Token Secret',
                    required=True)
parser.add_argument('--output', type=str,
                    help='Output string',
                    required=False)
parser.add_argument('--repeat', type=int,
                    help='Period after which script should re-execute (in minutes)',
                    required=False)
args = parser.parse_args()

date = time.strftime('%Y%m%d')
sheet = 'https://docs.google.com/spreadsheets/d/e/' + args.sid \
    + '/pub?gid=0&single=true&output=csv'

br = mechanize.Browser()
tw = twitter.Api(consumer_key = args.tkey,
                 consumer_secret = args.tsecret,
                 access_token_key = args.atoken,
                 access_token_secret = args.asecret)

if args.output is not None and len(args.output) > 1:
    formatter = args.output
else:
    formatter = '{t}, {c}'

print 'Location format has been set to: ', formatter

if args.repeat is not None and args.repeat > 0:
    print 'Location will update every ', args.repeat, 'minutes'
    scheduler = BlockingScheduler()
    scheduler.add_job(fetch, 'interval', minutes = args.repeat)
    scheduler.start()
else:
    print 'Location will be updated only once'
    fetch()
