# -*- coding: utf-8 -*-
"""
Created on Sun Jul 25 22:55:27 2021

@author: beldi
"""

from urllib.request import urlretrieve
import pandas as pd
import SPORTS

DATA_URL = 'https://projects.fivethirtyeight.com/soccer-api/club/spi_matches_latest.csv'

DATA_FILE_NAME = 'data.csv'

LEAGUES = SPORTS.leagues_fte

def updateData():
    urlretrieve(DATA_URL, DATA_FILE_NAME)

def getMatchData(league, ht, at):
    data = pd.read_csv (DATA_FILE_NAME)
    data = data.fillna(-1)
    return data[(data['league_id']==LEAGUES[league]) 
                & ((data['team1']==ht) | (data['team2']==at))
                & (data['score1']==-1)
                & (data['score2']==-1)].iloc[0]

def getMatchRes(ht, at):
    data = pd.read_csv (DATA_FILE_NAME)
    data = data.fillna(-1)
    return data[((data['team1']==ht) | (data['team2']==at))
                & (data['score1']!=-1)
                & (data['score2']!=-1)].iloc[-1]