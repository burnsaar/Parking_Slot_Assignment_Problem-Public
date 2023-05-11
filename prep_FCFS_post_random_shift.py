# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 18:58:37 2022

@author: Aaron
"""




import numpy as np
import pandas as pd
import seq_arrival_new as seq_curb



import pickle
with open('pub_Pitt_shifted_27_Nov_2022_buffer_5.pkl', 'rb') as file:
    n_index_lst_df, \
    n_index_norm_lst_df, \
    arrival_dfs_df, \
    sum_service_df, \
    dbl_park_Opt_status_inst_phi5_df, \
    PAPvAP_inst_phi5_df, \
    park_demand_Opt_inst_phi5_df, \
    park_events_df_inst_FCFS_shifted, \
    park_events_df_inst_phi5_shifted, \
    runtime, \
    buffer, \
    end, \
    iterations, \
    max_parking_spaces, \
    phi \
        = pickle.load(file)
        

dbl_park_events_df_inst_FCFS_df = pd.DataFrame()


for c in range(1, max_parking_spaces +1):
    dbl_park_events_df_inst_FCFS_lst = []
    
    for i in range(0, iterations):
        print('c =', c, 'i =', i)
        
        #pull the shifted vehicle arrival schedule
        shifted_sched = park_events_df_inst_FCFS_shifted.iloc[i, c][0]
        
        #prep the Q data to match the required input for seq_curb
        Q = shifted_sched[['t_i', 's_i', 'd_i']]
        Q = Q.rename(columns = {'t_i': 'a_i'})
        Q.insert(1, 'b_i', Q['a_i'])
        Q.insert(3, 't_i', Q['a_i'])
        Q = Q.set_index(shifted_sched['Truck'])
       
        

        #input the schedule into the sequential arrival function
        dbl_park_seq, dbl_parked_events, legal_parked_events, park_events_FCFS = seq_curb.seq_curb(c, Q, end)
        
        #store the park_event_FCFS
        dbl_park_events_df_inst_FCFS_lst.append(dbl_parked_events)
        
        
    dbl_park_events_df_inst_FCFS_df[c] = dbl_park_events_df_inst_FCFS_lst
    
    
    
    
    

# #save data from the run
# import pickle
# with open('pub_Pitt_reassessed_FCFS_2_Dec_2022_buffer_5.pkl', 'wb') as file:
#     pickle.dump(
#         [n_index_lst_df, 
#           n_index_norm_lst_df, 
#           arrival_dfs_df, 
#           sum_service_df, 
#           dbl_park_Opt_status_inst_phi5_df, 
#           PAPvAP_inst_phi5_df, 
#           park_demand_Opt_inst_phi5_df, 
#           park_events_df_inst_FCFS_shifted,
#           park_events_df_inst_phi5_shifted,
#           dbl_park_events_df_inst_FCFS_df,
#           runtime, 
#           buffer,
#           end,
#           iterations,
#           max_parking_spaces,
#           phi],
#             file)
