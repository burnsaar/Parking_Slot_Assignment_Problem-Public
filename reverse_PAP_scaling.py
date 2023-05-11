# -*- coding: utf-8 -*-
"""
Created on Sat Nov 12 09:26:44 2022

@author: Aaron
"""

#need to correct for the scaling issue in the objective function of the PAP.
#This issue is present in the run for record files from early Nov 2022.
#Need to bring in the run for record data and then update the objective function
#from the PAP runs to reverse the scaling by mean(s_i)



import numpy as np
import pandas as pd
import pickle


#new, random uniform number of DVs, 100 iteration, run for record
with open('pub_Pitt_run_for_record_9_Nov_2022.pkl', 'rb') as file:
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
        
        
        
#****phi5 only, used for the buffer scenarios**********************************
#new, random uniform number of DVs, 100 iteration, run for record, buffer 5
with open('pub_Pitt_run_for_record_7_Oct_2022_buffer_5.pkl', 'rb') as file:
    n_index_lst_df, \
    n_index_norm_lst_df, \
    arrival_dfs_df, \
    sum_service_df, \
    dbl_park_FCFS_instance_df, \
    dbl_park_FCFS_cancelled_inst_df, \
    dbl_park_events_df_inst_FCFS_df, \
    legal_park_events_df_inst_FCFS_df, \
    park_events_df_inst_FCFS_df, \
    dbl_park_Opt_status_inst_phi5_df, \
    PAPvAP_inst_phi5_df, \
    dbl_park_Opt_inst_phi5_df, \
    dbl_park_Diff_inst_phi5_df, \
    park_demand_Opt_inst_phi5_df, \
    dbl_park_events_df_inst_phi5_df, \
    park_events_df_inst_phi5_df, \
    runtime, \
    buffer, \
    end, \
    iterations, \
    max_parking_spaces, \
    phi \
        = pickle.load(file)



#*****************************Correcting for the scaling issue*****************
#************************Issue found on 12 Nov 2022****************************
       
#****all phi, needed for buffer = 0 and generating reduction graphics for the appendix  
for c in range(1, 8):
    for i in range(0, 100):
        #first, focus in on only the optimizations conducted by the PAP
        if PAPvAP_inst_phi0_df.iloc[i][c] == 'PAP':
            #pull the correct Q set of vehicle requests and grab the scaling factor
            Q = arrival_dfs_df.iloc[i][c]
            scale_s_i = np.mean(Q['s_i'])
            #identify the correct original objective value and reverse the scaling
            PAP_obj = dbl_park_Opt_inst_phi0_df.iloc[i][c]
            obj_reverse = PAP_obj * scale_s_i
            #identify the correct FCFS dbl parking value
            FCFS_dbl_park = dbl_park_FCFS_instance_df.iloc[i][c]
            #update the diff matrix
            dbl_park_Diff_inst_phi0_df.loc[i][c] = FCFS_dbl_park - obj_reverse
            #update the Opt matrix as well
            dbl_park_Opt_inst_phi0_df.loc[i][c] = obj_reverse

for c in range(1, 8):
    for i in range(0, 100):
        #first, focus in on only the optimizations conducted by the PAP
        if PAPvAP_inst_phi1_df.iloc[i][c] == 'PAP':
            #pull the correct Q set of vehicle requests and grab the scaling factor
            Q = arrival_dfs_df.iloc[i][c]
            scale_s_i = np.mean(Q['s_i'])
            #identify the correct original objective value and reverse the scaling
            PAP_obj = dbl_park_Opt_inst_phi1_df.iloc[i][c]
            obj_reverse = PAP_obj * scale_s_i
            #identify the correct FCFS dbl parking value
            FCFS_dbl_park = dbl_park_FCFS_instance_df.iloc[i][c]
            #update the diff matrix
            dbl_park_Diff_inst_phi1_df.loc[i][c] = FCFS_dbl_park - obj_reverse
            #update the Opt matrix as well
            dbl_park_Opt_inst_phi1_df.loc[i][c] = obj_reverse

for c in range(1, 8):
    for i in range(0, 100):
        #first, focus in on only the optimizations conducted by the PAP
        if PAPvAP_inst_phi2_df.iloc[i][c] == 'PAP':
            #pull the correct Q set of vehicle requests and grab the scaling factor
            Q = arrival_dfs_df.iloc[i][c]
            scale_s_i = np.mean(Q['s_i'])
            #identify the correct original objective value and reverse the scaling
            PAP_obj = dbl_park_Opt_inst_phi2_df.iloc[i][c]
            obj_reverse = PAP_obj * scale_s_i
            #identify the correct FCFS dbl parking value
            FCFS_dbl_park = dbl_park_FCFS_instance_df.iloc[i][c]
            #update the diff matrix
            dbl_park_Diff_inst_phi2_df.loc[i][c] = FCFS_dbl_park - obj_reverse
            #update the Opt matrix as well
            dbl_park_Opt_inst_phi2_df.loc[i][c] = obj_reverse

for c in range(1, 8):
    for i in range(0, 100):
        #first, focus in on only the optimizations conducted by the PAP
        if PAPvAP_inst_phi5_df.iloc[i][c] == 'PAP':
            #pull the correct Q set of vehicle requests and grab the scaling factor
            Q = arrival_dfs_df.iloc[i][c]
            scale_s_i = np.mean(Q['s_i'])
            #identify the correct original objective value and reverse the scaling
            PAP_obj = dbl_park_Opt_inst_phi5_df.iloc[i][c]
            obj_reverse = PAP_obj * scale_s_i
            #identify the correct FCFS dbl parking value
            FCFS_dbl_park = dbl_park_FCFS_instance_df.iloc[i][c]
            #update the diff matrix
            dbl_park_Diff_inst_phi5_df.loc[i][c] = FCFS_dbl_park - obj_reverse
            #update the Opt matrix as well
            dbl_park_Opt_inst_phi5_df.loc[i][c] = obj_reverse

for c in range(1, 8):
    for i in range(0, 100):
        #first, focus in on only the optimizations conducted by the PAP
        if PAPvAP_inst_phi10_df.iloc[i][c] == 'PAP':
            #pull the correct Q set of vehicle requests and grab the scaling factor
            Q = arrival_dfs_df.iloc[i][c]
            scale_s_i = np.mean(Q['s_i'])
            #identify the correct original objective value and reverse the scaling
            PAP_obj = dbl_park_Opt_inst_phi10_df.iloc[i][c]
            obj_reverse = PAP_obj * scale_s_i
            #identify the correct FCFS dbl parking value
            FCFS_dbl_park = dbl_park_FCFS_instance_df.iloc[i][c]
            #update the diff matrix
            dbl_park_Diff_inst_phi10_df.loc[i][c] = FCFS_dbl_park - obj_reverse
            #update the Opt matrix as well
            dbl_park_Opt_inst_phi10_df.loc[i][c] = obj_reverse

for c in range(1, 8):
    for i in range(0, 100):
        #first, focus in on only the optimizations conducted by the PAP
        if PAPvAP_inst_phi15_df.iloc[i][c] == 'PAP':
            #pull the correct Q set of vehicle requests and grab the scaling factor
            Q = arrival_dfs_df.iloc[i][c]
            scale_s_i = np.mean(Q['s_i'])
            #identify the correct original objective value and reverse the scaling
            PAP_obj = dbl_park_Opt_inst_phi15_df.iloc[i][c]
            obj_reverse = PAP_obj * scale_s_i
            #identify the correct FCFS dbl parking value
            FCFS_dbl_park = dbl_park_FCFS_instance_df.iloc[i][c]
            #update the diff matrix
            dbl_park_Diff_inst_phi15_df.loc[i][c] = FCFS_dbl_park - obj_reverse
            #update the Opt matrix as well
            dbl_park_Opt_inst_phi15_df.loc[i][c] = obj_reverse

for c in range(1, 8):
    for i in range(0, 100):
        #first, focus in on only the optimizations conducted by the PAP
        if PAPvAP_inst_phi30_df.iloc[i][c] == 'PAP':
            #pull the correct Q set of vehicle requests and grab the scaling factor
            Q = arrival_dfs_df.iloc[i][c]
            scale_s_i = np.mean(Q['s_i'])
            #identify the correct original objective value and reverse the scaling
            PAP_obj = dbl_park_Opt_inst_phi30_df.iloc[i][c]
            obj_reverse = PAP_obj * scale_s_i
            #identify the correct FCFS dbl parking value
            FCFS_dbl_park = dbl_park_FCFS_instance_df.iloc[i][c]
            #update the diff matrix
            dbl_park_Diff_inst_phi30_df.loc[i][c] = FCFS_dbl_park - obj_reverse
            #update the Opt matrix as well
            dbl_park_Opt_inst_phi30_df.loc[i][c] = obj_reverse


#****phi5 only, used for the buffer scenarios**********************************
for c in range(1, 8):
    for i in range(0, 100):
        #first, focus in on only the optimizations conducted by the PAP
        if PAPvAP_inst_phi5_df.iloc[i][c] == 'PAP':
            #pull the correct Q set of vehicle requests and grab the scaling factor
            Q = arrival_dfs_df.iloc[i][c]
            scale_s_i = np.mean(Q['s_i'])
            #identify the correct original objective value and reverse the scaling
            PAP_obj = dbl_park_Opt_inst_phi5_df.iloc[i][c]
            obj_reverse = PAP_obj * scale_s_i
            #identify the correct FCFS dbl parking value
            FCFS_dbl_park = dbl_park_FCFS_instance_df.iloc[i][c]
            #update the diff matrix
            dbl_park_Diff_inst_phi5_df.loc[i][c] = FCFS_dbl_park - obj_reverse
            #update the Opt matrix as well
            dbl_park_Opt_inst_phi5_df.loc[i][c] = obj_reverse





#save data from the run
# import pickle
# with open('pub_Pitt_run_for_record_16_Nov_2022_reversed_scaling.pkl', 'wb') as file:
#     pickle.dump([n_index_lst_df,
#                   n_index_norm_lst_df,
#                   arrival_dfs_df,
#                   sum_service_df,
#                   dbl_park_FCFS_instance_df,
#                   dbl_park_FCFS_cancelled_inst_df,
#                   dbl_park_events_df_inst_FCFS_df,
#                   legal_park_events_df_inst_FCFS_df,
#                   park_events_df_inst_FCFS_df,
#                   dbl_park_Opt_status_inst_phi0_df,
#                   dbl_park_Opt_status_inst_phi1_df,
#                   dbl_park_Opt_status_inst_phi2_df,
#                   dbl_park_Opt_status_inst_phi5_df,
#                   dbl_park_Opt_status_inst_phi10_df,
#                   dbl_park_Opt_status_inst_phi15_df,
#                   dbl_park_Opt_status_inst_phi30_df,
#                   PAPvAP_inst_phi0_df,
#                   PAPvAP_inst_phi1_df,
#                   PAPvAP_inst_phi2_df,
#                   PAPvAP_inst_phi5_df,
#                   PAPvAP_inst_phi10_df,
#                   PAPvAP_inst_phi15_df,
#                   PAPvAP_inst_phi30_df,
#                   dbl_park_Opt_inst_phi0_df,
#                   dbl_park_Opt_inst_phi1_df,
#                   dbl_park_Opt_inst_phi2_df,
#                   dbl_park_Opt_inst_phi5_df,
#                   dbl_park_Opt_inst_phi10_df,
#                   dbl_park_Opt_inst_phi15_df,
#                   dbl_park_Opt_inst_phi30_df,
#                   dbl_park_Diff_inst_phi0_df,
#                   dbl_park_Diff_inst_phi1_df,
#                   dbl_park_Diff_inst_phi2_df,
#                   dbl_park_Diff_inst_phi5_df,
#                   dbl_park_Diff_inst_phi10_df,
#                   dbl_park_Diff_inst_phi15_df,
#                   dbl_park_Diff_inst_phi30_df,
#                   park_demand_Opt_inst_phi0_df,
#                   park_demand_Opt_inst_phi1_df,
#                   park_demand_Opt_inst_phi2_df,
#                   park_demand_Opt_inst_phi5_df,
#                   park_demand_Opt_inst_phi10_df,
#                   park_demand_Opt_inst_phi15_df,
#                   park_demand_Opt_inst_phi30_df,
#                   dbl_park_events_df_inst_phi0_df,
#                   dbl_park_events_df_inst_phi1_df,
#                   dbl_park_events_df_inst_phi2_df,
#                   dbl_park_events_df_inst_phi5_df,
#                   dbl_park_events_df_inst_phi10_df,
#                   dbl_park_events_df_inst_phi15_df,
#                   dbl_park_events_df_inst_phi30_df,
#                   park_events_df_inst_phi0_df,
#                   park_events_df_inst_phi1_df,
#                   park_events_df_inst_phi2_df,
#                   park_events_df_inst_phi5_df,
#                   park_events_df_inst_phi10_df,
#                   park_events_df_inst_phi15_df,
#                   park_events_df_inst_phi30_df,
#                   runtime,
#                   buffer,
#                   end,
#                   iterations,
#                   max_parking_spaces,
#                   phi],
#                 file)



#****phi5 only, used for the buffer scenarios**********************************
#save data from the run
# import pickle
# with open('pub_Pitt_run_for_record_12_Nov_2022_buffer_5_reversed_scaling.pkl', 'wb') as file:
#     pickle.dump([n_index_lst_df,
#                   n_index_norm_lst_df,
#                   arrival_dfs_df,
#                   sum_service_df,
#                   dbl_park_FCFS_instance_df,
#                   dbl_park_FCFS_cancelled_inst_df,
#                   dbl_park_events_df_inst_FCFS_df,
#                   legal_park_events_df_inst_FCFS_df,
#                   park_events_df_inst_FCFS_df,
#                   dbl_park_Opt_status_inst_phi5_df,
#                   PAPvAP_inst_phi5_df,
#                   dbl_park_Opt_inst_phi5_df,
#                   dbl_park_Diff_inst_phi5_df,
#                   park_demand_Opt_inst_phi5_df,
#                   dbl_park_events_df_inst_phi5_df,
#                   park_events_df_inst_phi5_df,
#                   runtime,
#                   buffer,
#                   end,
#                   iterations,
#                   max_parking_spaces,
#                   phi],
#                 file)


