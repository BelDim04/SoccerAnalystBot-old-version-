# -*- coding: utf-8 -*-
"""
Created on Mon Jul 26 13:00:58 2021

@author: beldi
"""
from scipy.stats import poisson
import numpy as np
import SPORTS

MAT = 'mat'
PROB = 'prob'
ANALYZE = 'analayze'
TYPE = 'type'


def goalMatrix(proj_score1, proj_score2):
    d1 = []
    d2 = []
    for c in range(int(poisson(proj_score1).interval(0.999)[1])):
        d1.append(poisson(proj_score1).pmf(c))
    for c in range(int(poisson(proj_score2).interval(0.999)[1])):
        d2.append(poisson(proj_score2).pmf(c))
    s = 0
    for i in range(len(d1)):
        s += d1[i]
    d1.append(1-s)
    s = 0
    for i in range(len(d2)):
        s += d2[i]
    d2.append(1-s)
    ans = np.zeros((len(d1), len(d2)))
    for i in range(len(d1)):
        for j in range(len(d2)):
            ans[i][j] = d1[i]*d2[j]
    return ans


def h2hMatprob(fte_prob, odds_price):
    return {
        MAT: fte_prob*odds_price,
        PROB: fte_prob
    }


# team: home-0, away-1
def matprobSpreads(goal_matrix, team, point, price):
    win = 0
    ret = 0
    if(team == 0):
        for i in range(len(goal_matrix)):
            for j in range(len(goal_matrix[i])):
                if(i+point > j):
                    win += goal_matrix[i][j]
                if(i+point == j):
                    ret += goal_matrix[i][j]
    if(team == 1):
        for i in range(len(goal_matrix)):
            for j in range(len(goal_matrix[i])):
                if(j+point > i):
                    win += goal_matrix[i][j]
                if(j+point == i):
                    ret += goal_matrix[i][j]
    return {
        MAT: win*price+ret,
        PROB: win+ret
    }


def matprobTotals(goal_matrix, name, point, price):
    win = 0
    ret = 0
    if(name == 'Over'):
        for i in range(len(goal_matrix)):
            for j in range(len(goal_matrix[i])):
                if(i+j > point):
                    win += goal_matrix[i][j]
                if(i+j == point):
                    ret += goal_matrix[i][j]
    if(name == 'Under'):
        for i in range(len(goal_matrix)):
            for j in range(len(goal_matrix[i])):
                if(i+j < point):
                    win += goal_matrix[i][j]
                if(i+j == point):
                    ret += goal_matrix[i][j]
    return {
        MAT: win*price+ret,
        PROB: win+ret
    }


def check(fte_matchdata, odds_event):
    ans = []
    ht = odds_event['home_team']
    at = odds_event['away_team']
    goal_matrix = goalMatrix(
        fte_matchdata['proj_score1'], fte_matchdata['proj_score2'])
    books = odds_event['bookmakers']
    mb = -1
    for b in books:
        if(b['key'] == SPORTS.bookmaker):
            mb = b
            break
    if(mb == -1):
        return []
    markets = mb['markets']
    for m in markets:
        outcomes = m['outcomes']
        for r in outcomes:
            if(m['key'] == 'h2h'):
                if(r['name'] == ht):
                    h2h_pred = h2hMatprob(fte_matchdata['prob1'], r['price'])
                    if(h2h_pred[MAT] > SPORTS.min_mat and h2h_pred[PROB] > SPORTS.min_prob):
                        t = r
                        t[ANALYZE] = h2h_pred
                        t[TYPE] = m['key']
                        ans.append(t)
                if(r['name'] == at):
                    h2h_pred = h2hMatprob(fte_matchdata['prob2'], r['price'])
                    if(h2h_pred[MAT] > SPORTS.min_mat and h2h_pred[PROB] > SPORTS.min_prob):
                        t = r
                        t[ANALYZE] = h2h_pred
                        t[TYPE] = m['key']
                        ans.append(t)
                if(r['name'] == 'Draw'):
                    h2h_pred = h2hMatprob(fte_matchdata['probtie'], r['price'])
                    if(h2h_pred[MAT] > SPORTS.min_mat and h2h_pred[PROB] > SPORTS.min_prob):
                        t = r
                        t[ANALYZE] = h2h_pred
                        t[TYPE] = m['key']
                        ans.append(t)

            if(m['key'] == 'spreads'):
                if(r['name'] == ht):
                    spreads_pred = matprobSpreads(
                        goal_matrix, 0, r['point'], r['price'])
                    if(spreads_pred[MAT] > SPORTS.min_mat and spreads_pred[PROB] > SPORTS.min_prob):
                        t = r
                        t[ANALYZE] = spreads_pred
                        t[TYPE] = m['key']
                        ans.append(t)
                if(r['name'] == at):
                    spreads_pred = matprobSpreads(
                        goal_matrix, 1, r['point'], r['price'])
                    if(spreads_pred[MAT] > SPORTS.min_mat and spreads_pred[PROB] > SPORTS.min_prob):
                        t = r
                        t[ANALYZE] = spreads_pred
                        t[TYPE] = m['key']
                        ans.append(t)

            if(m['key'] == 'totals'):
                totals_pred = matprobTotals(
                    goal_matrix, r['name'], r['point'], r['price'])
                if(totals_pred[MAT] > SPORTS.min_mat and totals_pred[PROB] > SPORTS.min_prob):
                    t = r
                    t[ANALYZE] = totals_pred
                    t[TYPE] = m['key']
                    ans.append(t)
    return ans


def checkResStatus(ht, at, hg, ag, t, name, point):
    if(t=='h2h'):
        if(name == ht):
            if(hg>ag):
                return 1
            else:
                return -1
        if(name == at):
            if(hg<ag):
                return 1
            else:
                return -1
    if(t=='spreads'):
        if(name == ht):
            if(hg+point>ag):
                return 1
            if(hg+point==ag):
                return 0
            else:
                return -1
        if(name == at):
            if(hg<ag+point):
                return 1
            if(hg==ag+point):
                return 0
            else:
                return -1
    if(t=='totals'):
        if(name == 'Over'):
            if(hg+ag>point):
                return 1
            if(hg+ag==point):
                return 0
            else:
                return -1
        if(name == 'Under'):
            if(hg+ag<point):
                return 1
            if(hg+ag==point):
                return 0
            else:
                return -1