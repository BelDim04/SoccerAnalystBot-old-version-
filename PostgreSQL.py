# -*- coding: utf-8 -*-
"""
Created on Tue Jul 27 01:50:17 2021

@author: beldi
"""

import psycopg2

DB_NAME='name'
USER='user'
PASSWORD='password'
HOST='host'

#-----------------------------------------------------------------------------
ID = 0
CHAT_ID = 1
STATUS = 2


def get_subscriptions(status = True):
    con = psycopg2.connect(dbname=DB_NAME, user=USER, 
                        password=PASSWORD, host=HOST)
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE status = %s", (status,))
    ans = cur.fetchall()
    cur.close()
    con.close()
    return ans

def subscriber_exists(chat_id):
    con = psycopg2.connect(dbname=DB_NAME, user=USER, 
                        password=PASSWORD, host=HOST)
    cur = con.cursor()
    cur.execute('SELECT * FROM users WHERE chat_id = %s', (chat_id,))
    result = cur.fetchall()
    cur.close()
    con.close()
    return bool(len(result))
        
def add_subscriber(chat_id, status = True):
    con = psycopg2.connect(dbname=DB_NAME, user=USER, 
                        password=PASSWORD, host=HOST)
    cur = con.cursor()
    cur.execute("INSERT INTO users (chat_id, status) VALUES(%s,%s)", (chat_id,status))
    ans = cur.rowcount
    con.commit()
    cur.close()
    con.close()
    return bool(ans)


def update_subscription(chat_id, status):
    con = psycopg2.connect(dbname=DB_NAME, user=USER, 
                        password=PASSWORD, host=HOST)
    cur = con.cursor()
    cur.execute("UPDATE users SET status = %s WHERE chat_id = %s", (status, chat_id))
    ans = cur.rowcount
    con.commit()
    cur.close()
    con.close()
    return bool(ans)
#-----------------------------------------------------------------------------
BET_ID=0
DATE=1
LEAGUE=2
HT=3
AT=4
TYPE=5
NAME=6
POINT=7
PRICE=8
PROB=9
BET_STATUS=10

def addMatchBets(date,league,ht,at,t,name,point,price,prob):
    con = psycopg2.connect(dbname=DB_NAME, user=USER, 
                        password=PASSWORD, host=HOST)
    cur = con.cursor()
    cur.execute("INSERT INTO bets (date,league,ht,at,type,name,point,price,prob) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)", (date,league,ht,at,t,name,point,price,prob))
    ans = cur.rowcount
    con.commit()
    cur.close()
    con.close()
    return bool(ans)

def getBetsByDate(date, league=''):
    con = psycopg2.connect(dbname=DB_NAME, user=USER, 
                        password=PASSWORD, host=HOST)
    cur = con.cursor()
    if(league!=''):
        cur.execute("SELECT * FROM bets WHERE date = %s AND league = %s", (date.strftime('%Y-%m-%d'),league))
    else:
        cur.execute("SELECT * FROM bets WHERE date = %s", (date.strftime('%Y-%m-%d'),))
    ans = cur.fetchall()
    cur.close()
    con.close()
    return ans

def setBetStatus(idbs, date,ht,at,status):
    con = psycopg2.connect(dbname=DB_NAME, user=USER, 
                        password=PASSWORD, host=HOST)
    cur = con.cursor()
    cur.execute("UPDATE bets SET status = %s WHERE id=%s AND date = %s AND ht = %s AND at = %s", (status, idbs, date.strftime('%Y-%m-%d'), ht, at))
    ans = cur.rowcount
    con.commit()
    cur.close()
    con.close()
    return bool(ans)

def getAllBets():
    con = psycopg2.connect(dbname=DB_NAME, user=USER, 
                        password=PASSWORD, host=HOST)
    cur = con.cursor()
    cur.execute("SELECT * FROM bets")
    ans = cur.fetchall()
    cur.close()
    con.close()
    return ans
