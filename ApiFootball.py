# -*- coding: utf-8 -*-
"""
Created on Tue Aug  3 17:30:06 2021

@author: beldi
"""

import SPORTS
import http.client
import json

TOKEN = 'cc1db6a03b8d7b4e47ff6beaee4a8e16'
SEASON = '2021'

def dateMatches(date, leaguen):
    lid = SPORTS.leagues_apifootball[leaguen]
    conn = http.client.HTTPSConnection("v3.football.api-sports.io")
    headers = {
        'x-rapidapi-host': "v3.football.api-sports.io",
        'x-rapidapi-key': TOKEN
        }
    conn.request("GET", "/fixtures?league="+str(lid)+"&season="+SEASON+"&date="+date.strftime('%Y-%m-%d'), headers=headers)
    res = conn.getresponse()
    return json.loads(res.read().decode())["response"]