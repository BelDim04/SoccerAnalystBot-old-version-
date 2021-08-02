# -*- coding: utf-8 -*-
"""
Created on Tue Jul 27 01:50:17 2021

@author: beldi
"""

import psycopg2

DB_NAME='socceranalysttgbotdb'
USER='postgres'
PASSWORD='3928074Dd'
HOST='localhost'

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
