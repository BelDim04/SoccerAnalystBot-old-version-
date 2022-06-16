# -*- coding: utf-8 -*-
"""
Created on Mon Jul 26 01:56:04 2021

@author: beldi
"""
import math

sports_odds = ['soccer_italy_serie_b', 'soccer_sweden_allsvenskan', 'soccer_norway_eliteserien','soccer_brazil_campeonato','soccer_japan_j_league']

sport_title_odds = ['Serie B - Italy', 'Allsvenskan - Sweden', 'Eliteserien - Norway','MLS', 'Brazil S\u00e9rie A','J League']

leagues_fte = [1856, 1874, 1859, 2105, 1947]

leagues_apifootball = [136, 113, 103, 71, 98]

teams_odds_to_apifootball=[{
    'Parma':'Parma',
    'Alessandria':'Alessandria',
    'Cosenza':'Nuova Cosenza',
    'Brescia':'Brescia',
    'Como':'como',
    'Monza':'Monza',
    'SPAL':'Spal',
    'Perugia':'Perugia',
    'Vicenza':'Vicenza Virtus',
    'Lecce':'Lecce',
    'Frosinone':'Frosinone',
    'Benevento':'Benevento',
    'Ascoli':'Ascoli',
    'Ternana':'Ternana',
    'Crotone':'Crotone',
    'Reggina':'Reggina',
    'Pisa':'Pisa',
    'Pordenone':'Pordenone',
    'Cittadella':'Cittadella',
    'Cremonese':'Cremonese'
    },{
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
    },
      {
     'Internacional':'Internacional',
     'Botafogo':'Botafogo',
     'Palmeiras':'Palmeiras',
     'Fluminense':'Fluminense',
     'Am\u00e9rica Mineiro':'America Mineiro',
     'Sao Paulo':'Sao Paulo',
     'Flamengo':'Flamengo',
     'Santos':'Santos',
     'Cear\u00e1':'Ceara',
     'Corinthians':'Corinthians',
     'Atletico Paranaense':'Atletico Paranaense',
     'Atletico Goianiense':'Atletico Goianiense',
     'Avai':'Avai',
     'Coritiba':'Coritiba',
     'Goi\u00e1s':'Goias',
     'Juventude':'Juventude',
     'Fortaleza':'"Fortaleza EC',
     'Bragantino-SP':'RB Bragantino',
     'Atletico Mineiro':'Atletico-MG',
     'Cuiab\u00e1':'Cuiaba'
    },{
     'Consadole Sapporo':'Consadole Sapporo',
     'Jubilo Iwata':'Jubilo Iwata',
     'Kashiwa Reysol':'Kashiwa Reysol',
     'Hiroshima Sanfrecce FC':'Sanfrecce Hiroshima',
     'Shimizu S Pulse':'Shimizu S-pulse',
     'Shonan Bellmare':'Shonan Bellmare',
     'Urawa Red Diamonds':'Urawa',
     'Nagoya Grampus':'Nagoya Grampus',
     'Vissel Kobe':'Vissel Kobe',
     'Kashima Antlers':'Kashima',
     'Cerezo Osaka':'Cerezo Osaka',
     'FC Tokyo':'FC Tokyo',
     'Gamba Osaka':'Gamba Osaka',
     'Kawasaki Frontale':'Kawasaki Frontale',
     'Sagan Tosu':'Sagan Tosu',
     'Yokohama F Marinos':'Yokohama F. Marinos',
     'Kyoto Purple Sanga':'Kyoto Sanga',
     'Avispa Fukuoka':'Avispa Fukuoka'
    }]





bookmaker = 'onexbet'

bookmaker_name = '1xBet'

min_mat = 1.05

min_prob = 0.55

gamma = 0.75

mu = 0.04

alpha = 1 - gamma**(1/math.log(mu, 1 - min_prob))

'''
,{
     'Seattle Sounders FC':'Seattle Sounders',
     'San Jose Earthquakes':'San Jose Earthquakes',
     'Orlando City SC':'Orlando City SC',
     'New York Red Bulls':'New York Red Bulls',
     'Vancouver Whitecaps FC':'Vancouver Whitecaps',
     'New England Revolution':'New England Revolution',
     'Sporting Kansas City':'Sporting Kansas City',
     'Nashville SC':'Nashville SC',
     'Charlotte FC':'Charlotte'
    }

,'soccer_usa_mls'

 1951,
 
 , 253
'''