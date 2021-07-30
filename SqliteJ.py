# -*- coding: utf-8 -*-
"""
Created on Tue Jul 27 01:50:17 2021

@author: beldi
"""

import sqlite3

DB_FILE_NAME = 'db.db'


#-----------------------------------------------------------------------------
ID = 0
CHAT_ID = 1
STATUS = 2


def get_subscriptions(status = True):
    con = sqlite3.connect(DB_FILE_NAME)
    cur = con.cursor()
    ans = cur.execute("SELECT * FROM `users` WHERE `status` = ?", (status,)).fetchall()
    con.close()
    return ans

def subscriber_exists(chat_id):
    con = sqlite3.connect(DB_FILE_NAME)
    cur = con.cursor()
    result = cur.execute('SELECT * FROM `users` WHERE `chat_id` = ?', (chat_id,)).fetchall()
    con.close()
    return bool(len(result))
        
def add_subscriber(chat_id, status = True):
    con = sqlite3.connect(DB_FILE_NAME)
    cur = con.cursor()
    ans = cur.execute("INSERT INTO `users` (`chat_id`, `status`) VALUES(?,?)", (chat_id,status))
    con.commit()
    con.close()
    return ans


def update_subscription(chat_id, status):
    con = sqlite3.connect(DB_FILE_NAME)
    cur = con.cursor()
    ans = cur.execute("UPDATE `users` SET `status` = ? WHERE `chat_id` = ?", (status, chat_id))
    con.commit()
    con.close()
    return ans
#-----------------------------------------------------------------------------
