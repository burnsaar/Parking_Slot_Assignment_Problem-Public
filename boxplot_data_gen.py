# -*- coding: utf-8 -*-
"""
Created on Tue Jul 19 09:26:57 2022

@author: Aaron
"""



import numpy as np
import pandas as pd
import pickle
import time
import matplotlib.pyplot as plt
import seaborn as sns

tic = time.time()


# #new, random uniform number of DVs, 100 iteration, run for record
# with open('pub_Aspen_run_for_record_12_Nov_2022_reversed_scaling.pkl', 'rb') as file:
#     n_index_lst_df, \
#     n_index_norm_lst_df, \
#     arrival_dfs_df, \
#     sum_service_df, \
#     dbl_park_FCFS_instance_df, \
#     dbl_park_FCFS_cancelled_inst_df, \
#     dbl_park_events_df_inst_FCFS_df, \
#     legal_park_events_df_inst_FCFS_df, \
#     park_events_df_inst_FCFS_df, \
#     dbl_park_Opt_status_inst_phi0_df, \
#     dbl_park_Opt_status_inst_phi1_df, \
#     dbl_park_Opt_status_inst_phi2_df, \
#     dbl_park_Opt_status_inst_phi5_df, \
#     dbl_park_Opt_status_inst_phi10_df, \
#     dbl_park_Opt_status_inst_phi15_df, \
#     dbl_park_Opt_status_inst_phi30_df, \
#     PAPvAP_inst_phi0_df, \
#     PAPvAP_inst_phi1_df, \
#     PAPvAP_inst_phi2_df, \
#     PAPvAP_inst_phi5_df, \
#     PAPvAP_inst_phi10_df, \
#     PAPvAP_inst_phi15_df, \
#     PAPvAP_inst_phi30_df, \
#     dbl_park_Opt_inst_phi0_df, \
#     dbl_park_Opt_inst_phi1_df, \
#     dbl_park_Opt_inst_phi2_df, \
#     dbl_park_Opt_inst_phi5_df, \
#     dbl_park_Opt_inst_phi10_df, \
#     dbl_park_Opt_inst_phi15_df, \
#     dbl_park_Opt_inst_phi30_df, \
#     dbl_park_Diff_inst_phi0_df, \
#     dbl_park_Diff_inst_phi1_df, \
#     dbl_park_Diff_inst_phi2_df, \
#     dbl_park_Diff_inst_phi5_df, \
#     dbl_park_Diff_inst_phi10_df, \
#     dbl_park_Diff_inst_phi15_df, \
#     dbl_park_Diff_inst_phi30_df, \
#     park_demand_Opt_inst_phi0_df, \
#     park_demand_Opt_inst_phi1_df, \
#     park_demand_Opt_inst_phi2_df, \
#     park_demand_Opt_inst_phi5_df, \
#     park_demand_Opt_inst_phi10_df, \
#     park_demand_Opt_inst_phi15_df, \
#     park_demand_Opt_inst_phi30_df, \
#     dbl_park_events_df_inst_phi0_df, \
#     dbl_park_events_df_inst_phi1_df, \
#     dbl_park_events_df_inst_phi2_df, \
#     dbl_park_events_df_inst_phi5_df, \
#     dbl_park_events_df_inst_phi10_df, \
#     dbl_park_events_df_inst_phi15_df, \
#     dbl_park_events_df_inst_phi30_df, \
#     park_events_df_inst_phi0_df, \
#     park_events_df_inst_phi1_df, \
#     park_events_df_inst_phi2_df, \
#     park_events_df_inst_phi5_df, \
#     park_events_df_inst_phi10_df, \
#     park_events_df_inst_phi15_df, \
#     park_events_df_inst_phi30_df, \
#     runtime, \
#     buffer, \
#     end, \
#     iterations, \
#     max_parking_spaces, \
#     phi \
#         = pickle.load(file)

#new Pitt, random uniform number of DVs, 100 iteration, run for record
with open('pub_Pitt_run_for_record_24_Nov_2022.pkl', 'rb') as file:
    n_index_lst_df, \
    n_index_norm_lst_df, \
    arrival_dfs_df, \
    sum_service_df, \
    dbl_park_FCFS_instance_df, \
    dbl_park_FCFS_cancelled_inst_df, \
    dbl_park_events_df_inst_FCFS_df, \
    legal_park_events_df_inst_FCFS_df, \
    park_events_df_inst_FCFS_df, \
    dbl_park_Opt_status_inst_phi0_df, \
    dbl_park_Opt_status_inst_phi1_df, \
    dbl_park_Opt_status_inst_phi2_df, \
    dbl_park_Opt_status_inst_phi5_df, \
    dbl_park_Opt_status_inst_phi10_df, \
    dbl_park_Opt_status_inst_phi15_df, \
    dbl_park_Opt_status_inst_phi30_df, \
    PAPvAP_inst_phi0_df, \
    PAPvAP_inst_phi1_df, \
    PAPvAP_inst_phi2_df, \
    PAPvAP_inst_phi5_df, \
    PAPvAP_inst_phi10_df, \
    PAPvAP_inst_phi15_df, \
    PAPvAP_inst_phi30_df, \
    dbl_park_Opt_inst_phi0_df, \
    dbl_park_Opt_inst_phi1_df, \
    dbl_park_Opt_inst_phi2_df, \
    dbl_park_Opt_inst_phi5_df, \
    dbl_park_Opt_inst_phi10_df, \
    dbl_park_Opt_inst_phi15_df, \
    dbl_park_Opt_inst_phi30_df, \
    dbl_park_Diff_inst_phi0_df, \
    dbl_park_Diff_inst_phi1_df, \
    dbl_park_Diff_inst_phi2_df, \
    dbl_park_Diff_inst_phi5_df, \
    dbl_park_Diff_inst_phi10_df, \
    dbl_park_Diff_inst_phi15_df, \
    dbl_park_Diff_inst_phi30_df, \
    park_demand_Opt_inst_phi0_df, \
    park_demand_Opt_inst_phi1_df, \
    park_demand_Opt_inst_phi2_df, \
    park_demand_Opt_inst_phi5_df, \
    park_demand_Opt_inst_phi10_df, \
    park_demand_Opt_inst_phi15_df, \
    park_demand_Opt_inst_phi30_df, \
    dbl_park_events_df_inst_phi0_df, \
    dbl_park_events_df_inst_phi1_df, \
    dbl_park_events_df_inst_phi2_df, \
    dbl_park_events_df_inst_phi5_df, \
    dbl_park_events_df_inst_phi10_df, \
    dbl_park_events_df_inst_phi15_df, \
    dbl_park_events_df_inst_phi30_df, \
    park_events_df_inst_phi0_df, \
    park_events_df_inst_phi1_df, \
    park_events_df_inst_phi2_df, \
    park_events_df_inst_phi5_df, \
    park_events_df_inst_phi10_df, \
    park_events_df_inst_phi15_df, \
    park_events_df_inst_phi30_df, \
    runtime, \
    buffer, \
    end, \
    iterations, \
    max_parking_spaces, \
    phi \
        = pickle.load(file)


#calc the minutes of double parking with FCFS for 2 parking spaces versus 1

import seq_arrival_new as seq_curb

end = 1200 #660 for the Aspen dataset,  1200 for the Pittsburgh dataset


dbl_park_FCFS_instance_df_1_2 = pd.DataFrame()
dbl_park_FCFS_instance_df_2_3 = pd.DataFrame()
dbl_park_FCFS_instance_df_3_4 = pd.DataFrame()
dbl_park_FCFS_instance_df_4_5 = pd.DataFrame()
dbl_park_FCFS_instance_df_5_6 = pd.DataFrame()
dbl_park_FCFS_instance_df_6_7 = pd.DataFrame()
dbl_park_FCFS_instance_df_7_8 = pd.DataFrame()


#c_index = 1
#for c_index in range(1, max_parking_spaces +1):
for c_index in range(7,8):
    
    dbl_park_FCFS_instance = []
    
    #for i_index in range(0, iterations):
    for i_index in range(16,17):
        print('c = ' + str(c_index) + ' i = ' + str(i_index))
        Q = arrival_dfs_df.iloc[i_index, c_index -1]
        
        #drop the trucks column so that the seq.curb can insert the column again...
        #not super efficient, but seq_curb is set up for running with the execute 
        #loop as the priority, not this extra data gen loop
        Q.drop(['Trucks'], axis = 1, inplace = True)
    
        #dbl_park_seq, dbl_parked_events, legal_parked_events, park_events_FCFS = seq_curb.seq_curb(c_index +1, Q, end)
        dbl_park_seq, dbl_parked_events, legal_parked_events, park_events_FCFS = seq_curb.seq_curb(c_index, Q, end)
    
        dbl_park_FCFS_instance.append(dbl_park_seq)


    if c_index == 1:
        dbl_park_FCFS_instance_df_1_2[c_index +1] = dbl_park_FCFS_instance
    elif c_index == 2:
        dbl_park_FCFS_instance_df_2_3[c_index +1] = dbl_park_FCFS_instance
    elif c_index == 3:
        dbl_park_FCFS_instance_df_3_4[c_index +1] = dbl_park_FCFS_instance
    elif c_index == 4:
        dbl_park_FCFS_instance_df_4_5[c_index +1] = dbl_park_FCFS_instance
    elif c_index == 5:
        dbl_park_FCFS_instance_df_5_6[c_index +1] = dbl_park_FCFS_instance
    elif c_index == 6:
        dbl_park_FCFS_instance_df_6_7[c_index +1] = dbl_park_FCFS_instance
    elif c_index == 7:
        dbl_park_FCFS_instance_df_7_8[c_index +1] = dbl_park_FCFS_instance


#save data from the run
# import pickle
# with open('pub_Pitt_boxplot_data_gen_25_Nov_2022.pkl', 'wb') as file:
#     pickle.dump([dbl_park_FCFS_instance_df_1_2,
#                   dbl_park_FCFS_instance_df_2_3,
#                   dbl_park_FCFS_instance_df_3_4,
#                   dbl_park_FCFS_instance_df_4_5,
#                   dbl_park_FCFS_instance_df_5_6,
#                   dbl_park_FCFS_instance_df_6_7,
#                   dbl_park_FCFS_instance_df_7_8],
#                 file)





