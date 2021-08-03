# -*- coding: utf-8 -*-
"""
Created on Tue Jul 27 01:50:17 2021

@author: beldi
"""

import psycopg2

DB_NAME='ddvai2bm0li6i0'
USER='dntyphvnezrncl'
PASSWORD='e2582bff920eb3d8772ad2345c2ec6d7666efc435c62a47ab297219992222e76'
HOST='ec2-108-128-104-50.eu-west-1.compute.amazonaws.com'

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
HT=2
AT=3
TYPE=4
NAME=5
POINT=6
PRICE=7
STATUS=8
LEAGUE=9

def addMatchBets(date,ht,at,t,name,point,price,league):
    con = psycopg2.connect(dbname=DB_NAME, user=USER, 
                        password=PASSWORD, host=HOST)
    cur = con.cursor()
    cur.execute("INSERT INTO bets (date,ht,at,type,name,point,price,league) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)", (date,ht,at,t,name,point,price,league))
    ans = cur.rowcount
    con.commit()
    cur.close()
    con.close()
    return bool(ans)

def getBetsByDate(date, league):
    con = psycopg2.connect(dbname=DB_NAME, user=USER, 
                        password=PASSWORD, host=HOST)
    cur = con.cursor()
    cur.execute("SELECT * FROM bets WHERE date = %s AND league = %s", (date.strftime('%Y-%m-%d'),league))
    ans = cur.fetchall()
    cur.close()
    con.close()
    return ans

def setBetStatus(date,ht,at,status):
    con = psycopg2.connect(dbname=DB_NAME, user=USER, 
                        password=PASSWORD, host=HOST)
    cur = con.cursor()
    cur.execute("UPDATE bets SET status = %s WHERE date = %s AND ht = %s AND at = %s", (status, date.strftime('%Y-%m-%d'), ht, at))
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