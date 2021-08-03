# -*- coding: utf-8 -*-
"""
Created on Mon Jul 26 01:04:51 2021

@author: beldi
"""

import requests
import SPORTS
import ApiFootball
from datetime import datetime


API_KEY = 'b93d870cbb382d6f225416897686a12c'

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
    i=0
    for sport in SPORT:
        ans.append([])
        date = datetime.utcnow()
        if(len(ApiFootball.dateMatches(date, i))==0):
            continue
        odds_response = matchList(sport)
        if odds_response.status_code == 200:
            odds_json = odds_response.json()
            for event in odds_json:
                if(event['commence_time'].__contains__(date.strftime('%Y-%m-%d'))):
                    ans[-1].append(event)
        global REQUESTS_REMAINING, REQUESTS_USED
        REQUESTS_REMAINING = odds_response.headers['x-requests-remaining']
        REQUESTS_USED = odds_response.headers['x-requests-used']
        i+=1
    return ans

