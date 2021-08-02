# -*- coding: utf-8 -*-
"""
Created on Tue Jul 27 02:26:12 2021

@author: beldi
"""
from threading import Thread
import telebot
import time
import PostgreSQL
import Odds
import SPORTS
import FiveThirtyEight as FTE
import Checker
from datetime import datetime


TIME = '08:00'


TOKEN = '1815897690:AAHH3V0B_c4LzN97e4X95Z_fQtQonagw7wU'
bot = telebot.AsyncTeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Hello! Use /information and /figuresandfacts to learn more about me.')

@bot.message_handler(commands=['information'])
def inf(message):
    bot.send_message(message.chat.id, 'Hello! I am soccer analyst and I can send you my thoughts on soccer betting every day at '+TIME+' UTC. If I send nothing - there are no good deals.')
    
@bot.message_handler(commands=['figuresandfacts'])
def figures(message):
    bot.send_message(message.chat.id, 'My strategy is based on math. I advise you an event if the mathematical expectation of the bet > '+str(round(SPORTS.min_mat, 2))+' and the probability of is success > '+str(round(SPORTS.min_prob,2))+'. Thus, with the recommended rate '+str(round(SPORTS.alpha*100, 2))+'% of the bank, the profit frome one bet is on average not less than '+str(round((SPORTS.min_mat-1)*100,2))+'% of its value, and the probability of losing '+str(round((1-SPORTS.gamma)*100,2))+'% of the bank does not exceed '+str(round(SPORTS.mu,2))+'.')
    
@bot.message_handler(commands=['subscribe'])
def subscribe(message):
    ans = 0
    if(not PostgreSQL.subscriber_exists(message.chat.id)):
        ans = PostgreSQL.add_subscriber(message.chat.id)
    else:
        ans = PostgreSQL.update_subscription(message.chat.id, True)
    if(ans):
        bot.reply_to(message, "You have successfully subscribed!")
    else:
        bot.reply_to(message, "Error")

@bot.message_handler(commands=['unsubscribe'])
def unsubscribe(message):
    ans = 0
    if(not PostgreSQL.subscriber_exists(message.from_user.id)):
        ans = PostgreSQL.add_subscriber(message.chat.id, False)
    else:
        ans = PostgreSQL.update_subscription(message.chat.id, False)
    if(ans):
        bot.reply_to(message, "You have unsubscribed.")
    else:
        bot.reply_to(message, "Error")
        
@bot.message_handler(func=lambda m: True)
def echo_all(message):
    if(message.text=='_._ForceUpdate_!_'):
        if(int(Odds.REQUESTS_REMAINING)>200):
            adv = todayAdv()
            if(len(adv) == 0):
                bot.send_message(message.chat.id, 'Nothing for now')
            adv_text = advToText(adv)
            bot.send_message(message.chat.id, adv_text)
            bot.send_message(message.chat.id, 'Requests remaining '+str(Odds.REQUESTS_REMAINING))
        else:
            bot.send_message(message.chat.id, 'Requests remaining '+str(Odds.REQUESTS_REMAINING))
    elif(message.text=='_._RequestsRemaining_!_'):
        bot.send_message(message.chat.id, 'Requests remaining '+str(Odds.REQUESTS_REMAINING))
    else:
        bot.send_message(message.chat.id, 'Wait '+TIME+' UTC')


#---------------------------------------------------------
SPORT_TITLE = 'sport_title'
COMMENCE_TIME = 'commence_time'
HOME_TEAM = 'home_team'
AWAY_TEAM = 'away_team'
PREDS = 'preds'


def todayAdv():
    ans=[]
    FTE.updateData()
    tml = Odds.todayMatchList()
    for i in range(len(tml)):
        for j in range(len(tml[i])):
            res = Checker.check(FTE.getMatchData(i,tml[i][j]['home_team'],tml[i][j]['away_team']), tml[i][j])
            if(len(res)>0):
                ans.append({
                    SPORT_TITLE:tml[i][j]['sport_title'],
                    COMMENCE_TIME:tml[i][j]['commence_time'],
                    HOME_TEAM:tml[i][j]['home_team'],
                    AWAY_TEAM:tml[i][j]['away_team'],
                    PREDS:res
                    })
    return ans

def advToText(adv):
    t = ''
    for m in adv:
        t+=f'{m[SPORT_TITLE]}\n'
        t+=f'{m[COMMENCE_TIME]}\n'
        t+=f'{m[HOME_TEAM]} - {m[AWAY_TEAM]}\n\n'
        for p in m[PREDS]:
            if(p[Checker.TYPE] == 'h2h'):
                t+='Match result - '+p['name']+'  k - '+str(p['price'])
                t+='  (m='+str(round(p[Checker.ANALYZE][Checker.MAT],3))+', p='+str(round(p[Checker.ANALYZE][Checker.PROB],3))+')'
                t+='\n'
            if(p[Checker.TYPE] == 'spreads'):
                t+=p['name']+' spread '+str(p['point'])+'  k - '+str(p['price'])
                t+='  (m='+str(round(p[Checker.ANALYZE][Checker.MAT],3))+', p='+str(round(p[Checker.ANALYZE][Checker.PROB],3))+')'
                t+='\n'
            if(p[Checker.TYPE] == 'totals'):
                t+='Total '+p['name']+' '+str(p['point'])+'  k - '+str(p['price'])
                t+='  (m='+str(round(p[Checker.ANALYZE][Checker.MAT],3))+', p='+str(round(p[Checker.ANALYZE][Checker.PROB],3))+')'
                t+='\n'
        t+='--------------------------------------\n'
    t+='k - from '+SPORTS.bookmaker_name+'\n'
    t+='Recommended rate - '+str(round(SPORTS.alpha*100, 2))+'% of the bank.'
    return t
        

def sendAll():
    adv = todayAdv()
    if(len(adv) == 0):
        return
    adv_text = advToText(adv)
    subscribers = PostgreSQL.get_subscriptions()
    for s in subscribers:
        bot.send_message(s[PostgreSQL.CHAT_ID], adv_text)
    

def targetF():
    while True:
        if(datetime.utcnow().strftime('%H:%M') == TIME):
            sendAll()
        time.sleep(60)
        
th = Thread(target=targetF)
th.start()
#---------------------------------------------------------

#---------------------------------------------------------
import requests
odds_response = requests.get('https://api.the-odds-api.com/v4/sports/', params={
            'api_key': Odds.API_KEY
            })
Odds.REQUESTS_REMAINING = odds_response.headers['x-requests-remaining']
Odds.REQUESTS_USED = odds_response.headers['x-requests-used']
    
bot.polling()