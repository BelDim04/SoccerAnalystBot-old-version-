# -*- coding: utf-8 -*-
"""
Created on Mon Jul 26 01:56:04 2021

@author: beldi
"""
import math

sports_odds = ['soccer_sweden_allsvenskan', 'soccer_norway_eliteserien']

sport_title_odds = ['Allsvenskan - Sweden', 'Eliteserien - Norway']

leagues_fte = [1874, 1859]

leagues_apifootball = [113, 103]

teams_odds_to_apifootball=[{
    'Djurgardens IF':'Djurgardens IF',
    'AIK':'AIK stockholm',
    'BK Hacken':'BK Hacken',
    'Ostersunds FK':'Ostersunds FK',
    'IF Elfsborg':'IF elfsborg',
    'Degerfors IF':'Degerfors IF',
    'IFK Goteborg':'IFK Goteborg',
    'Hammarby IF':'Hammarby FF',
    'Halmstads BK':'Halmstad',
    'Malmo FF':'Malmo FF',
    'Orebro SK':'Orebro SK',
    'Mjällby AIF':'Mjallby AIF',
    'IFK Norrkoping':'IFK Norrkoping',
    'Kalmar FF':'kalmar FF',
    'Varbergs BoIS':'Varbergs BoIS FC',
    'IK Sirius':'Sirius'
    },{
     'Kristiansund BK':'Kristiansund BK',
     'Stabaek':'Stabaek',
     'Lillestrom':'Lillestrom',
     'Bodø/Glimt':'Bodo/Glimt',
     'Odds BK':'ODD Ballklubb',
     'Haugesund':'Haugesund',
     'Mjøndalen':'Mjondalen',
     'Rosenborg':'Rosenborg',
     'Viking FK':'Viking',
     'Molde':'Molde',
     'SK Brann':'Brann',
     'Sandefjord':'Sandefjord',
     'Tromso':'Tromso',
     'Vålerenga':'Valerenga',
     'Sarpsborg FK':'Sarpsborg 08 FF',
     'Stromsgodset':'Stromsgodset'
    }]





bookmaker = 'onexbet'

bookmaker_name = '1xBet'

min_mat = 1.1

min_prob = 0.5

gamma = 0.75

mu = 0.04

alpha = 1 - gamma**(1/math.log(mu, 1 - min_prob))