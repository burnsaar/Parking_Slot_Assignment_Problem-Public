# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 15:08:50 2023

@author: Aaron
"""


#load standard python packages
import numpy as np
import pandas as pd
import time

#load user created functions
import gen_veh_arrivals as gen
import gen_Pitt_arrivals as gen_Pitt
import seq_arrival_new as seq_curb

import PAP as MOD_flex
import AP as AP

import genBids as genBids


# Variable initialization
np.random.seed(335)

tic = time.time()

dataset = 'Aspen'

start = 0
end = 660  #also know as T, for the Aspen data this needs to be 11hrs or 660 minutes, 7am-6pm
            #for the Pitt data this should be set at 1200, represents 4am - Midnight

iterations = 1

#baseline case
c = 4 #num parking spaces
phi = 5 #flexibility
demand = c*2*11 #total vehicles to draw veh/hr/parking space
buffer = 5 #buffer space between reservations


runtime_PAP = []
runtime_AP = []
runtime_hybrid_PAP = []
runtime_hybrid_AP = []
runtime_hybrid_both = []

status_PAP = []
status_AP = []
status_hybrid_PAP = []
status_hybrid_AP = []


for i in range(0, iterations):
    
    #create the vehicle request matrix
    if dataset == 'Aspen':
        Q, sum_service = gen.gen_veh_arrivals(demand, end)
    elif dataset == 'Pitt':
        Q, sum_service = gen_Pitt.gen_Pitt_arrivals(demand, end)
        
    #run FCFS for fun
    dbl_park_seq, dbl_parked_events, legal_parked_events, park_events_FCFS = seq_curb.seq_curb(c, Q, end)
    

    ########################## MILP runtime only
    t_initialize = [None] #added for buffer case
    x_initialize = [None] #added for buffer case
    runtime, status, obj, count_b_i, end_state_t_i, end_state_x_ij, dbl_park_events, park_events \
        = MOD_flex.MOD_flex(phi, demand, c, Q, buffer, start, end, t_initialize, x_initialize, timelimit = 60)
    
    runtime_PAP.append(runtime)
    status_PAP.append(status)

    ########################### ILP runtime only
    x_initialize = [None] #added for buffer case
    bids = genBids.genBids(demand, end, Q, phi)
    runtime, status, obj, dbl_park_Opt, park_demand, end_state_x_i_j, dbl_park_events, park_events \
        = AP.AP(demand, end, Q, c, bids, phi, buffer, x_initialize, timelimit = 300)
    
    runtime_AP.append(runtime)
    status_AP.append(status)
    
    ########################### both runtime
    t_initialize = [None] #added for buffer case
    x_initialize = [None] #added for buffer case
    
    runtime_1, status, obj, count_b_i, end_state_t_i, end_state_x_ij, dbl_park_events, park_events \
        = MOD_flex.MOD_flex(phi, demand, c, Q, buffer, start, end, t_initialize, x_initialize, timelimit = 45)
    
    x_initialize = end_state_x_ij
    
    runtime_hybrid_PAP.append(runtime_1)
    status_hybrid_PAP.append(status)


    #if the PAP times out, set the flag as true
    if status == 9:
        
        #execute the AP
        #x_initialize = [None] #* n_index

        bids = genBids.genBids(demand, end, Q, phi)

        runtime_2, status, obj, dbl_park_Opt, park_demand, end_state_x_i_j, dbl_park_events, park_events \
            = AP.AP(demand, end, Q, c, bids, phi, buffer, x_initialize, timelimit = 120)

        runtime_hybrid_AP.append(runtime_2)
        runtime_hybrid_both.append(runtime_1 + runtime_2)
        status_hybrid_AP.append(status)
        
    else: #meaning we didn't need to go into the AP for the hybrid approach
        runtime_hybrid_both.append(runtime_1)
        status_hybrid_AP.append(-1) #-1 will represent "N/A"


