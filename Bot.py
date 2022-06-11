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
import ApiFootball
import FiveThirtyEight as FTE
import Checker
from datetime import datetime, timedelta

TIME = '8:30'
TIME_S = '08:00'

CH_ID = '-1001501114700'


TOKEN = '1815897690:AAHH3V0B_c4LzN97e4X95Z_fQtQonagw7wU'
bot = telebot.AsyncTeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Hello! Use /information and /figuresandfacts to learn more about me.')

@bot.message_handler(commands=['information'])
def inf(message):
    t = 'I am soccer analyst and I can send you my thoughts on soccer betting every day at '+TIME+' UTC (check @SoccerAnalystPublic). If I send nothing - there are no good deals. The following leagues are under my supervision: '
    for l in SPORTS.sport_title_odds:
        t+=l
        t+=', '
    t=t[:-2]
    t+='. Keep in mind that my recommendations and predictions are only advice and not a motivation for action!'
    bot.send_message(message.chat.id,  t)
    
@bot.message_handler(commands=['figuresandfacts'])
def figures(message):
    bot.send_message(message.chat.id, 'My strategy is based on math. I advise you an event if the mathematical expectation (m) of the bet > '+str(round(SPORTS.min_mat, 2))+' and the probability (p) of its success > '+str(round(SPORTS.min_prob,2))+'. Thus, with the recommended rate '+str(round(SPORTS.alpha*100, 2))+'% of the bank, the profit from one bet is on average not less than '+str(round((SPORTS.min_mat-1)*100,2))+'% of its value, and the probability of losing '+str(round((1-SPORTS.gamma)*100,2))+'% of the bank does not exceed '+str(round(SPORTS.mu,2))+'. Also, I advise you to check my predictions, paying attention to the latest news, such as injuries or disqualifications, because I am not good enough to take this into account.')

'''    
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
'''
        
@bot.message_handler(func=lambda m: True)
def echo_all(message):
    if(message.text == '=REQUESTS_REMAINING='):
        bot.send_message(message.chat.id, str(Odds.REQUESTS_REMAINING))
    else:
        bot.send_message(message.chat.id, 'I am hard at work and I don`t have time to chat now. Use commands to interact with me.')


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
            md = FTE.getMatchData(i,SPORTS.teams_odds_to_apifootball[i][tml[i][j]['home_team']],SPORTS.teams_odds_to_apifootball[i][tml[i][j]['away_team']])
            if md.size > 0:
                res = Checker.check(md, tml[i][j])
            else:
                res = []
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
        t+=f'{m[COMMENCE_TIME][:10]} '
        t+=f'{m[COMMENCE_TIME][11:16]} UTC\n'
        t+=f'{m[HOME_TEAM]} - {m[AWAY_TEAM]}\n\n'
        for p in m[PREDS]:
            if(p[Checker.TYPE] == 'h2h'):
                t+='Match result - '+p['name']+'  Kmin - '+str(round(1/p[Checker.ANALYZE][Checker.PROB],2)+0.01)+'  (Kcur - '+str(p['price'])+')'
                t+='  (m='+str(round(p[Checker.ANALYZE][Checker.MAT],3))+', p='+str(round(p[Checker.ANALYZE][Checker.PROB],3))+')'
                t+='\n'
            if(p[Checker.TYPE] == 'spreads'):
                t+=p['name']+' spread '+str(p['point'])+'  Kmin - '+str(round(1/p[Checker.ANALYZE][Checker.PROB],2)+0.01)+'  (Kcur - '+str(p['price'])+')'
                t+='  (m='+str(round(p[Checker.ANALYZE][Checker.MAT],3))+', p='+str(round(p[Checker.ANALYZE][Checker.PROB],3))+')'
                t+='\n'
            if(p[Checker.TYPE] == 'totals'):
                t+='Total '+p['name']+' '+str(p['point'])+'  Kmin - '+str(round(1/p[Checker.ANALYZE][Checker.PROB],2)+0.01)+'  (Kcur - '+str(p['price'])+')'
                t+='  (m='+str(round(p[Checker.ANALYZE][Checker.MAT],3))+', p='+str(round(p[Checker.ANALYZE][Checker.PROB],3))+')'
                t+='\n'
        t+='--------------------------------------\n'
    t+='Kcur - from '+SPORTS.bookmaker_name+'\n'
    t+='Recommended rate - '+str(round(SPORTS.alpha*100, 2))+'% of the bank.'
    return t
        

def sendAll():
    adv = todayAdv()
    if(len(adv) == 0):
        return
    for a in adv:
        mToBets(a)
    adv_text = advToText(adv)
    #subscribers = PostgreSQL.get_subscriptions()
    #for s in subscribers:
    #    bot.send_message(s[PostgreSQL.CHAT_ID], adv_text)
    bot.send_message(CH_ID, adv_text)
        
        
def mToBets(match):
    date = match[COMMENCE_TIME][:10]
    ht = match[HOME_TEAM]
    at = match[AWAY_TEAM]
    league = match[SPORT_TITLE]
    preds = match[PREDS]
    for p in preds:
        if(p[Checker.TYPE]=='h2h'):
            PostgreSQL.addMatchBets(date, league, ht, at, p[Checker.TYPE], p['name'], -0.5, p['price'], p[Checker.ANALYZE][Checker.PROB])
        else:
            PostgreSQL.addMatchBets(date, league, ht, at, p[Checker.TYPE], p['name'], p['point'], p['price'], p[Checker.ANALYZE][Checker.PROB])
  

def setStat():
    date = datetime.utcnow()+timedelta(days=-1)
    for i in range(len(SPORTS.sport_title_odds)):
        l = SPORTS.sport_title_odds[i]
        ms = PostgreSQL.getBetsByDate(date, l)
        if(len(ms)==0):
            continue
        rs = ApiFootball.dateMatches(date, i)
        for m in ms:
            ht = m[PostgreSQL.HT]
            at = m[PostgreSQL.AT]
            idbs = m[PostgreSQL.BET_ID]
            for r in rs:
                if(r['teams']['home']['name']==SPORTS.teams_odds_to_apifootball[i][ht] and r['teams']['away']['name']==SPORTS.teams_odds_to_apifootball[i][at]):
                    hg = r['goals']['home']
                    ag = r['goals']['away']
                    status = Checker.checkResStatus(ht, at, hg, ag, m[PostgreSQL.TYPE], m[PostgreSQL.NAME], m[PostgreSQL.POINT])
                    PostgreSQL.setBetStatus(idbs, date, ht, at, status)
                    break
                
def sendStat():
    bets = PostgreSQL.getAllBets()
    cb=1
    nb=1
    ss=0
    wb=0
    lb=0
    rb=0
    p=bets[0]
    u=SPORTS.alpha*cb
    for b in bets:
        if(b[PostgreSQL.DATE]!=p[PostgreSQL.DATE]):
            u=SPORTS.alpha*cb
        if(b[PostgreSQL.BET_STATUS]==1):
            cb+=u*(b[PostgreSQL.PRICE]-1)
            wb+=1
            ss+=u
            p=b
        elif(b[PostgreSQL.BET_STATUS]==-1):
            cb-=u
            lb+=1
            ss+=u
            p=b
        elif(b[PostgreSQL.BET_STATUS]==0):
            rb+=1
            ss+=u
            p=b
    if(ss==0):
        return
    text = '-----Statistics-----\n Total:\n  Wins - '+str(wb)+'\n  Returns - '+str(rb)+'\n  Losses - '+str(lb)+'\n'#+'  ROI - '+str(round((cb-nb)/nb,3))+'\n  YIELD - '+str(round((cb-nb)/ss,3))
    date = datetime.utcnow()+timedelta(days=-1)
    bets = PostgreSQL.getBetsByDate(date)
    wb=0
    lb=0
    rb=0
    k=0
    for b in bets:
        if(b[PostgreSQL.BET_STATUS]==1):
            wb+=1
            k+=1
        elif(b[PostgreSQL.BET_STATUS]==-1):
            lb+=1
            k+=1
        elif(b[PostgreSQL.BET_STATUS]==0):
            rb+=1
            k+=1
    if(k==0):
        return
    text+='\n\n---Yesterday---\n  Wins - '+str(wb)+'\n  Returns - '+str(rb)+'\n  Losses - '+str(lb)
    #subscribers = PostgreSQL.get_subscriptions()
    #for s in subscribers:
    #    bot.send_message(s[PostgreSQL.CHAT_ID], text)
    bot.send_message(CH_ID, text)

def targetF():
    while True:
        if(datetime.utcnow().strftime('%H:%M') == TIME):
            sendAll()
        if(datetime.utcnow().strftime('%H:%M') == TIME_S):
            setStat()
            sendStat()
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