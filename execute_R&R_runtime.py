# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 15:08:50 2023

@author: Aaron
"""

from datetime import datetime, date
import os
import pickle
import seaborn as sns
import matplotlib.pyplot as plt

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


def run_optimization(iterations, c, demand, start, end, phi, buffer, dataset):
    
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
        print('iteration ' + str(i))
        
        #create the vehicle request matrix
        if dataset == 'Aspen':
            Q, sum_service = gen.gen_veh_arrivals(demand, end)
        elif dataset == 'Pitt':
            Q, sum_service = gen_Pitt.gen_Pitt_arrivals(demand, end)
            
        #run FCFS for fun
        dbl_park_seq, dbl_parked_events, legal_parked_events, park_events_FCFS = seq_curb.seq_curb(c, Q, end)
        
    
        ########################## MILP runtime only
        t_initialize = [None] 
        x_initialize = [None] 
        runtime, status, obj, count_b_i, end_state_t_i, end_state_x_ij, dbl_park_events, park_events \
            = MOD_flex.MOD_flex(phi, demand, c, Q, buffer, start, end, t_initialize, x_initialize, timelimit = 300)
        
        runtime_PAP.append(runtime.total_seconds())
        status_PAP.append(status)
    
        ########################### ILP runtime only
        x_initialize = [None] 
        bids = genBids.genBids(demand, end, Q, phi)
        runtime, status, obj, dbl_park_Opt, park_demand, end_state_x_i_j, dbl_park_events, park_events \
            = AP.AP(demand, end, Q, c, bids, phi, buffer, x_initialize, timelimit = 300)
        
        runtime_AP.append(runtime.total_seconds())
        status_AP.append(status)
        
        ########################### both runtime
        t_initialize = [None] 
        x_initialize = [None] 
        
        runtime_1, status, obj, count_b_i, end_state_t_i, end_state_x_ij, dbl_park_events, park_events \
            = MOD_flex.MOD_flex(phi, demand, c, Q, buffer, start, end, t_initialize, x_initialize, timelimit = 45)
        
        x_initialize = end_state_x_ij
        
        runtime_hybrid_PAP.append(runtime_1.total_seconds())
        status_hybrid_PAP.append(status)
    
    
        #if the PAP times out, set the flag as true
        if status == 9:
            
            #execute the AP
            x_initialize = [None]
    
            bids = genBids.genBids(demand, end, Q, phi)
    
            runtime_2, status, obj, dbl_park_Opt, park_demand, end_state_x_i_j, dbl_park_events, park_events \
                = AP.AP(demand, end, Q, c, bids, phi, buffer, x_initialize, timelimit = 120)
    
            runtime_hybrid_AP.append(runtime_2.total_seconds())
            runtime_hybrid_both.append(runtime_1.total_seconds() + runtime_2.total_seconds())
            status_hybrid_AP.append(status)
            
        else: #meaning we didn't need to go into the AP for the hybrid approach
            runtime_hybrid_AP.append(0)    
            runtime_hybrid_both.append(runtime_1.total_seconds())
            status_hybrid_AP.append(-1) #-1 will represent "N/A"
    
    #compile the results
    
    
    results = {'runtime_PAP': runtime_PAP, 'runtime_AP': runtime_AP, 'runtime_hybrid_PAP': runtime_hybrid_PAP,
               'runtime_hybrid_AP': runtime_hybrid_AP, 'runtime_hybrid_both': runtime_hybrid_both,
               'status_PAP': status_PAP, 'status_AP': status_AP, 'status_hybrid_PAP': status_hybrid_PAP,
               'status_hybrid_AP': status_hybrid_AP}
    
    res_df = pd.DataFrame(results)

    return res_df


def save_res(res_df):
    #save the results file
    current_date = date.today().strftime('%Y-%m-%d') 
    # Define the base path for saving files
    base_path = 'C:/Users/Aaron/Documents/GitHub/Parking_Slot_Assignment_Problem-public/runtime/'
    current_date = current_date + '_Aaron Result'

    # Create a folder with the formatted date if it doesn't exist
    folder_path = os.path.join(base_path, current_date)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Define the file path for saving
    saveFile = os.path.join(folder_path, 'Res_df.dat')

    try:
        with open(saveFile, 'wb') as file:
            pickle.dump(res_df, file)
    except TypeError as e:
        print(e)
    return

def load_res():
    file = open('C:/Users/Aaron/Documents/GitHub/Parking_Slot_Assignment_Problem-Public/runtime/2024-01-16_Aaron Result (good data 3 spaces 4 demand)/Res_df.dat', 'rb')
    res_df = pickle.load(file)
    file.close()
    return res_df

def convert_for_sns(data):
    df_PAP = pd.concat([res_df['runtime_PAP'], res_df['status_PAP']], axis=1)
    df_PAP['label'] = 'PAP only'
    df_PAP.rename(columns = {'runtime_PAP': 'runtime', 'status_PAP': 'status'}, inplace = True)
    
    df_AP = pd.concat([res_df['runtime_AP'], res_df['status_AP']], axis=1)
    df_AP['label'] = 'AP only'
    df_AP.rename(columns = {'runtime_AP': 'runtime', 'status_AP': 'status'}, inplace = True)
    
    df_both = pd.concat([res_df['runtime_hybrid_both'], res_df['status_hybrid_AP']], axis=1)
    df_both['label'] = 'Hybrid\n(PAP and AP)'
    df_both.rename(columns = {'runtime_hybrid_both': 'runtime', 'status_hybrid_AP': 'status'}, inplace = True)
    
    df = pd.concat([df_PAP, df_AP, df_both], axis = 0)
    df['status'] = df['status'].map({-1: 'Optimal (only needed PAP)', 2: 'Optimal', 9: 'Time Limit (Not Optimal)'})
    
    return df

def gen_boxplot(data):
    plt.figure()
    sns.boxplot(data = data, x = 'runtime', y = 'label', color = 'white', showfliers = False) #, hue = 'status', outliers removed with showfliers
    sns.stripplot(data = data, x = 'runtime', y = 'label', hue = 'status', hue_order=['Optimal', 'Optimal (only needed PAP)', 'Time Limit (Not Optimal)'],
                  edgecolor='black', jitter = .20, linewidth = 0.75)    #, 'Time Limit (Not Optimal)'
    plt.xlabel('Optimization Runtime (seconds)')
    plt.ylabel('Optimization Method')
    #plt.suptitle('Runtime Comparison')
    plt.title('3 spaces, 4 vehices/hr/space (132 vehicles), $\Psi = 5$, $\Phi = 5$')
    plt.legend(title = 'Algorithm Result', loc = 'lower right', fontsize = '9')
    
    return

if __name__ == '__main__':

    # Variable initialization
    np.random.seed(335)
    
    plt.rcParams['figure.dpi'] = 500
    
    dataset = 'Aspen'
    
    start = 0
    end = 660  #also know as T, for the Aspen data this needs to be 11hrs or 660 minutes, 7am-6pm
                #for the Pitt data this should be set at 1200, represents 4am - Midnight
    
    iterations = 50
    
    
    #baseline case
    c = 3 #num parking spaces
    phi = 5 #flexibility
    demand = c*4*11 #total vehicles to draw veh/hr/parking space
    buffer = 5 #buffer space between reservations
    
    
    #run the optimization models
    tic = time.time()
    res_df = run_optimization(iterations, c, demand, start, end, phi, buffer, dataset)
    toc = time.time()
    runtime = toc-tic
    print('optimization runtime: ' + str(runtime))
    
    #save the model results
    save_res(res_df)
    
    #load the results if needed
    #res_df = load_res()
    
    #start generating graphics!
    data_df = convert_for_sns(res_df)
    
    gen_boxplot(data_df)
    



