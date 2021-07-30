# -*- coding: utf-8 -*-
"""
Created on Mon Jul 26 01:04:51 2021

@author: beldi
"""

import requests
import SPORTS
from datetime import datetime


f = open('ODDS_TOKEN.txt')
API_KEY = f.read()

SPORT = SPORTS.sports_odds

REGIONS = 'eu'

MARKETS = 'h2h,spreads,totals'

REQUESTS_REMAINING = 500

REQUESTS_USED = 0


def matchList(sport):
    return requests.get(f'https://api.the-odds-api.com/v4/sports/{sport}/odds', params={
            'api_key': API_KEY,
            'regions': REGIONS,
            'markets': MARKETS})


def todayMatchList():
    ans = [] 
    for sport in SPORT:
        ans.append([])
        odds_response = matchList(sport)
        if odds_response.status_code == 200:
            odds_json = odds_response.json()
            date = datetime.utcnow()
            for event in odds_json:
                if(event['commence_time'].__contains__(date.strftime('%Y-%m-%d'))):
                    ans[-1].append(event)

    global REQUESTS_REMAINING, REQUESTS_USED
    REQUESTS_REMAINING = odds_response.headers['x-requests-remaining']
    REQUESTS_USED = odds_response.headers['x-requests-used']
    return ans

