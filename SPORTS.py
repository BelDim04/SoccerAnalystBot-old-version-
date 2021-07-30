# -*- coding: utf-8 -*-
"""
Created on Mon Jul 26 01:56:04 2021

@author: beldi
"""
import math

sports_odds = ['soccer_sweden_allsvenskan', 'soccer_norway_eliteserien']

leagues_fte = [1874, 1859]

bookmaker = 'onexbet'

min_mat = 1.05

min_prob = 0.35

gamma = 0.75

mu = 0.05

alpha = 1 - gamma**(1/math.log(mu, 1 - min_prob))