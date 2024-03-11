# -*- coding: utf-8 -*-
"""
Created on Wed Dec  1 20:17:09 2021

@author: Burns
"""


import numpy as np
import pandas as pd
import pickle
import time
import matplotlib.pyplot as plt
import seaborn as sns
plt.rcParams['figure.dpi'] = 500
#from scipy.optimize import fsolve
#import scipy.integrate as integrate

tic = time.time()


#add in the boxplot FCFS comparison data


#new, random uniform number of DVs, 100 iteration, run for record
with open('pub_Aspen_run_for_record_16_Nov_2022_reversed_scaling.pkl', 'rb') as file:
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
        
with open('pub_Aspen_boxplot_data_gen_16_Nov_2022.pkl', 'rb') as file:
    dbl_park_FCFS_instance_df_1_2, \
    dbl_park_FCFS_instance_df_2_3, \
    dbl_park_FCFS_instance_df_3_4, \
    dbl_park_FCFS_instance_df_4_5, \
    dbl_park_FCFS_instance_df_5_6, \
    dbl_park_FCFS_instance_df_6_7, \
    dbl_park_FCFS_instance_df_7_8 \
        = pickle.load(file)
        
#publication baseline run for record, no buffer, queuing data, labeled
with open('pub_Aspen_queuing_data_post_process_phi5_med_limit30_7_Nov_2022.pkl', 'rb') as file:
    net_dbl_park_minutes_df_inst_FCFS, \
    total_veh_delay_inst_FCFS, \
    total_veh_delay_error_inst_FCFS, \
    queue_duration_inst_FCFS, \
    t_queue_remove_inst_FCFS, \
    veh_in_queue_inst_FCFS, \
    avg_veh_in_queue_inst_FCFS, \
    max_veh_in_queue_inst_FCFS, \
    avg_veh_delay_inst_FCFS, \
    avg_len_queue_inst_FCFS, \
    net_dbl_park_minutes_df_inst_phi5, \
    total_veh_delay_inst_phi5, \
    total_veh_delay_error_inst_phi5, \
    queue_duration_inst_phi5, \
    t_queue_remove_inst_phi5, \
    veh_in_queue_inst_phi5, \
    avg_veh_in_queue_inst_FCFS, \
    max_veh_in_queue_inst_phi5, \
    avg_veh_delay_inst_phi5, \
    avg_len_queue_inst_phi5, \
    net_dbl_park_minutes_Diff_df_inst_phi5, \
    total_veh_delay_Diff_inst_phi5, \
    total_veh_delay_error_Diff_inst_phi5, \
    queue_duration_Diff_inst_phi5, \
    t_queue_remove_Diff_inst_phi5, \
    avg_veh_in_queue_Diff_inst_phi5, \
    max_veh_in_queue_Diff_inst_phi5, \
    avg_veh_delay_Diff_inst_phi5, \
    avg_len_queue_Diff_inst_phi5 \
        = pickle.load(file)
 
#***********Aspen w/ buffer 5**************************************************
#new, random uniform number of DVs, 100 iteration, run for record, buffer 5
with open('pub_Aspen_run_for_record_17_Jan_2024_buffer_15.pkl', 'rb') as file:
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
        
        
#data to help graph the redux in dbl parking with buffer 5, but after the schedule
#has been shifted and reassessed 
with open('pub_Aspen_reassessed_combined_18_Jan_2024_buffer_15_redux_graphic_prep.pkl', 'rb') as file: 
          n_index_lst_df, \
          n_index_norm_lst_df, \
          arrival_dfs_df, \
          sum_service_df, \
          dbl_park_Opt_status_inst_phi5_df, \
          PAPvAP_inst_phi5_df, \
          park_demand_Opt_inst_phi5_df, \
          park_events_df_inst_phi5_shifted, \
          park_events_df_inst_phi5_shifted, \
          runtime, \
          buffer, \
          end, \
          iterations, \
          max_parking_spaces, \
          phi, \
          park_events_df_inst_phi5_df, \
          dbl_park_events_df_inst_phi5_df, \
          dbl_park_events_df_inst_FCFS_df, \
          dbl_park_Diff_inst_phi5_df \
              = pickle.load(file)  
 
    
 
#publication run for record, buffer 5, queuing data, labeled
#pub_Aspen_queuing_data_post_process_phi5_limit30_18_Mar_2023_buffer_5_pessimistic.pkl
#pub_Aspen_queuing_data_post_process_phi5_limit30_18_Mar_2023_buffer_5_optimistic.pkl
#pub_Aspen_queuing_data_post_process_phi5_limit30_19_Mar_2023_buffer_5_basecase.pkl
# with open('pub_Aspen_queuing_data_post_process_phi5_limit30_18_Mar_2023_buffer_5_pessimistic.pkl', 'rb') as file:
#     net_dbl_park_minutes_df_inst_FCFS, \
#     total_veh_delay_inst_FCFS, \
#     total_veh_delay_error_inst_FCFS, \
#     queue_duration_inst_FCFS, \
#     t_queue_remove_inst_FCFS, \
#     veh_in_queue_inst_FCFS, \
#     avg_veh_in_queue_inst_FCFS, \
#     max_veh_in_queue_inst_FCFS, \
#     avg_veh_delay_inst_FCFS, \
#     avg_len_queue_inst_FCFS, \
#     net_dbl_park_minutes_df_inst_phi5, \
#     total_veh_delay_inst_phi5, \
#     total_veh_delay_error_inst_phi5, \
#     queue_duration_inst_phi5, \
#     t_queue_remove_inst_phi5, \
#     veh_in_queue_inst_phi5, \
#     avg_veh_in_queue_inst_FCFS, \
#     max_veh_in_queue_inst_phi5, \
#     avg_veh_delay_inst_phi5, \
#     avg_len_queue_inst_phi5, \
#     net_dbl_park_minutes_Diff_df_inst_phi5, \
#     total_veh_delay_Diff_inst_phi5, \
#     total_veh_delay_error_Diff_inst_phi5, \
#     queue_duration_Diff_inst_phi5, \
#     t_queue_remove_Diff_inst_phi5, \
#     avg_veh_in_queue_Diff_inst_phi5, \
#     max_veh_in_queue_Diff_inst_phi5, \
#     avg_veh_delay_Diff_inst_phi5, \
#     avg_len_queue_Diff_inst_phi5 \
#         = pickle.load(file)
        

#pub_Aspen_queuing_data_post_process_phi5_limit30_midpt_24_Mar_2023_buffer_5_basecase.pkl
#pub_Aspen_queuing_data_post_process_phi5_limit30_midpt_24_Mar_2023_buffer_5_pessimistic.pkl
#pub_Aspen_queuing_data_post_process_phi5_limit30_midpt_24_Mar_2023_buffer_5_optimistic.pkl

with open('pub_Aspen_queuing_data_post_process_phi5_limit30_midpt_24_Mar_2023_buffer_5_basecase.pkl', 'rb') as file:
    net_dbl_park_minutes_df_inst_FCFS, \
    total_veh_delay_inst_FCFS, \
    queue_duration_inst_FCFS, \
    t_queue_remove_inst_FCFS, \
    avg_len_queue_inst_FCFS, \
    net_dbl_park_minutes_df_inst_phi5, \
    total_veh_delay_inst_phi5, \
    queue_duration_inst_phi5, \
    t_queue_remove_inst_phi5, \
    avg_len_queue_inst_phi5, \
    net_dbl_park_minutes_Diff_df_inst_phi5, \
    total_veh_delay_Diff_inst_phi5, \
    queue_duration_Diff_inst_phi5, \
    t_queue_remove_Diff_inst_phi5, \
    avg_len_queue_Diff_inst_phi5 \
        = pickle.load(file)


        
#***************Pitt, baseline no buffer***************************************         
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
 
    
with open('pub_Pitt_boxplot_data_gen_25_Nov_2022.pkl', 'rb') as file:
     dbl_park_FCFS_instance_df_1_2, \
     dbl_park_FCFS_instance_df_2_3, \
     dbl_park_FCFS_instance_df_3_4, \
     dbl_park_FCFS_instance_df_4_5, \
     dbl_park_FCFS_instance_df_5_6, \
     dbl_park_FCFS_instance_df_6_7, \
     dbl_park_FCFS_instance_df_7_8 \
         = pickle.load(file)
    

#publication baseline run for record, no buffer, queuing data, labeled
with open('pub_Pitt_queuing_data_post_process_phi5_med_limit30_25_Nov_2022.pkl', 'rb') as file:
    net_dbl_park_minutes_df_inst_FCFS, \
    total_veh_delay_inst_FCFS, \
    total_veh_delay_error_inst_FCFS, \
    queue_duration_inst_FCFS, \
    t_queue_remove_inst_FCFS, \
    veh_in_queue_inst_FCFS, \
    avg_veh_in_queue_inst_FCFS, \
    max_veh_in_queue_inst_FCFS, \
    avg_veh_delay_inst_FCFS, \
    avg_len_queue_inst_FCFS, \
    net_dbl_park_minutes_df_inst_phi5, \
    total_veh_delay_inst_phi5, \
    total_veh_delay_error_inst_phi5, \
    queue_duration_inst_phi5, \
    t_queue_remove_inst_phi5, \
    veh_in_queue_inst_phi5, \
    avg_veh_in_queue_inst_FCFS, \
    max_veh_in_queue_inst_phi5, \
    avg_veh_delay_inst_phi5, \
    avg_len_queue_inst_phi5, \
    net_dbl_park_minutes_Diff_df_inst_phi5, \
    total_veh_delay_Diff_inst_phi5, \
    total_veh_delay_error_Diff_inst_phi5, \
    queue_duration_Diff_inst_phi5, \
    t_queue_remove_Diff_inst_phi5, \
    avg_veh_in_queue_Diff_inst_phi5, \
    max_veh_in_queue_Diff_inst_phi5, \
    avg_veh_delay_Diff_inst_phi5, \
    avg_len_queue_Diff_inst_phi5 \
        = pickle.load(file)
      
 
    
#***********Pittsburgh w/ buffer 5**************************************************
#new, random uniform number of DVs, 100 iteration, run for record, buffer 5
with open('pub_Pitt_run_for_record_27_Nov_2022_buffer_5.pkl', 'rb') as file:
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
    
    
#data to help graph the redux in dbl parking with buffer 5, but after the schedule
#has been shifted and reassessed 
with open('pub_Pitt_reassessed_combined_3_Dec_2022_buffer_5_redux_graphic_prep.pkl', 'rb') as file: 
          n_index_lst_df, \
          n_index_norm_lst_df, \
          arrival_dfs_df, \
          sum_service_df, \
          dbl_park_Opt_status_inst_phi5_df, \
          PAPvAP_inst_phi5_df, \
          park_demand_Opt_inst_phi5_df, \
          park_events_df_inst_phi5_shifted, \
          park_events_df_inst_phi5_shifted, \
          runtime, \
          buffer, \
          end, \
          iterations, \
          max_parking_spaces, \
          phi, \
          park_events_df_inst_phi5_df, \
          dbl_park_events_df_inst_phi5_df, \
          dbl_park_events_df_inst_FCFS_df, \
          dbl_park_Diff_inst_phi5_df \
              = pickle.load(file)     
              

#publication run for record, buffer 5, queuing data, labeled
#pub_Pitt_queuing_data_post_process_phi5_limit30_22_Mar_2023_buffer_5_pessimistic.pkl
#pub_Pitt_queuing_data_post_process_phi5_limit30_23_Mar_2023_buffer_5_basecase.pkl
#pub_Pitt_queuing_data_post_process_phi5_limit30_21_Mar_2023_buffer_5_optimistic.pkl

# with open('pub_Pitt_queuing_data_post_process_phi5_limit30_23_Mar_2023_buffer_5_pessimistic.pkl', 'rb') as file:
#     net_dbl_park_minutes_df_inst_FCFS, \
#     total_veh_delay_inst_FCFS, \
#     total_veh_delay_error_inst_FCFS, \
#     queue_duration_inst_FCFS, \
#     t_queue_remove_inst_FCFS, \
#     veh_in_queue_inst_FCFS, \
#     avg_veh_in_queue_inst_FCFS, \
#     max_veh_in_queue_inst_FCFS, \
#     avg_veh_delay_inst_FCFS, \
#     avg_len_queue_inst_FCFS, \
#     net_dbl_park_minutes_df_inst_phi5, \
#     total_veh_delay_inst_phi5, \
#     total_veh_delay_error_inst_phi5, \
#     queue_duration_inst_phi5, \
#     t_queue_remove_inst_phi5, \
#     veh_in_queue_inst_phi5, \
#     avg_veh_in_queue_inst_FCFS, \
#     max_veh_in_queue_inst_phi5, \
#     avg_veh_delay_inst_phi5, \
#     avg_len_queue_inst_phi5, \
#     net_dbl_park_minutes_Diff_df_inst_phi5, \
#     total_veh_delay_Diff_inst_phi5, \
#     total_veh_delay_error_Diff_inst_phi5, \
#     queue_duration_Diff_inst_phi5, \
#     t_queue_remove_Diff_inst_phi5, \
#     avg_veh_in_queue_Diff_inst_phi5, \
#     max_veh_in_queue_Diff_inst_phi5, \
#     avg_veh_delay_Diff_inst_phi5, \
#     avg_len_queue_Diff_inst_phi5 \
#         = pickle.load(file)


#pub_Pitt_queuing_data_post_process_phi5_limit30_midpt_24_Mar_2023_buffer_5_basecase.pkl
#pub_Pitt_queuing_data_post_process_phi5_limit30_midpt_24_Mar_2023_buffer_5_pessimistic.pkl
#pub_Pitt_queuing_data_post_process_phi5_limit30_midpt_24_Mar_2023_buffer_5_optimistic.pkl

with open('pub_Pitt_queuing_data_post_process_phi5_limit30_midpt_24_Mar_2023_buffer_5_basecase.pkl', 'rb') as file:
    net_dbl_park_minutes_df_inst_FCFS, \
    total_veh_delay_inst_FCFS, \
    queue_duration_inst_FCFS, \
    t_queue_remove_inst_FCFS, \
    avg_len_queue_inst_FCFS, \
    net_dbl_park_minutes_df_inst_phi5, \
    total_veh_delay_inst_phi5, \
    queue_duration_inst_phi5, \
    t_queue_remove_inst_phi5, \
    avg_len_queue_inst_phi5, \
    net_dbl_park_minutes_Diff_df_inst_phi5, \
    total_veh_delay_Diff_inst_phi5, \
    queue_duration_Diff_inst_phi5, \
    t_queue_remove_Diff_inst_phi5, \
    avg_len_queue_Diff_inst_phi5 \
        = pickle.load(file)


    

#*****************************Correcting for the scaling issue*****************
#************************Issue found on 12 Nov 2022****************************

#****phi5 only, used for the buffer scenarios
# for c in range(1, 8):
#     for i in range(0, 100):
#         if PAPvAP_inst_phi5_df.iloc[i][c] == 'PAP':
#             Q = arrival_dfs_df.iloc[i][c]
#             scale_s_i = np.mean(Q['s_i'])
#             dbl_park_Diff_inst_phi5_df.at[i][c] = dbl_park_Diff_inst_phi5_df.iloc[i][c]*scale_s_i
        
#****all phi, needed for buffer = 0 and generating reduction graphics for the appendix  
 

#this is so I can test the reversed scaling of the PAP objective function
with open('pub_Aspen_run_for_record_12_Nov_2022_test_c_1.pkl', 'rb') as file:
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



#**********************Relevant Graphics for Run for Record********************


##############################################################################
#Average reduction in unschedule service duration, phi = 5, random uniform DV scenarios

#4th attempt at the rolling average, and trying to overlay the scatter plot of the data


data_df = pd.DataFrame()

c_list = [1,2,3,4,5,6,7]
c_list = [1,2,4,7]
#c_list = [1]
for c in c_list:
    #create a series to represent the specific number of parking spaces we are looking at
    parking_space = pd.Series([c]*50, name = 'Parking Spaces')
    #pull the normalized parking demand for a specific number of parking spaces
    parking_space_demand = pd.Series(n_index_norm_lst_df[c], name = 'norm parking demand')
    #pull the associated reduction in double parking
    redux = pd.Series(dbl_park_Diff_inst_phi5_df[c]/11/c, name = 'redux') #11 for Aspen, 20 for Pitt
    #combine this two in column form
    df = pd.concat([parking_space, parking_space_demand, redux], axis = 1)
    #sort the data based on the norm parking demand
    df = df.sort_values(by = ['norm parking demand'], ascending = [True], ignore_index = True)
    #now, calculate the rolling average
    rolling_avg = df['redux'].rolling(11).mean().shift(-5)
    #append the rolling average data to the dataframe
    df['rolling avg'] = rolling_avg
    
    data_df = pd.concat([data_df, df], ignore_index = True)

    
plt.figure()

#sns.scatterplot(x = 'Vehicle Demand Norm', y = 'Redux Dbl Park phi5', data = data_df, hue = 'Parking Spaces', palette = "tab10")
sns.lineplot(x = 'norm parking demand', y = 'rolling avg', data = data_df, hue = 'Parking Spaces', palette = "tab10", ci = None)
sns.scatterplot(x = 'norm parking demand', y = 'redux', data = data_df, hue = 'Parking Spaces', palette = "tab10", marker = 'X', legend = False) #alpha = 0.4, 
plt.axhline(y = 0, xmin = 0, xmax = 6, linewidth=2, color='k', linestyle = '--')
#plt.suptitle('Reduction in Double Parking (\u03A6 = 5, \u03A8 = 0)')
#plt.title('(Aspen, 11-sample rolling average)')
plt.xlabel('Number of Deliveries \n (per hour per parking space)')
plt.ylabel('Reduction in Double Parking \n (minutes per hour per parking space)')
plt.ylim([-10, 11.5])
plt.legend(title = 'Parking Spaces', loc = 'upper left', prop={'size': 8})

plt.savefig("output.jpg", bbox_inches = 'tight')

##############################################################################


##############################################################################
#Average reduction in fuel consumption, phi = 5, random uniform DV scenarios

import numpy as np
import pandas as pd
import pickle
import time
import matplotlib.pyplot as plt
import seaborn as sns
plt.rcParams['figure.dpi'] = 500


#***********Aspen w/ buffer 5**************************************************
#new, random uniform number of DVs, 100 iteration, run for record, buffer 5
with open('pub_Aspen_run_for_record_17_Jan_2024_buffer_15.pkl', 'rb') as file:
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


#pub_Aspen_queuing_data_post_process_phi5_limit30_midpt_24_Mar_2023_buffer_5_basecase.pkl
#pub_Aspen_queuing_data_post_process_phi5_limit30_midpt_24_Mar_2023_buffer_5_pessimistic.pkl
#pub_Aspen_queuing_data_post_process_phi5_limit30_midpt_24_Mar_2023_buffer_5_optimistic.pkl

with open('pub_Aspen_queuing_data_post_process_phi5_limit30_midpt_17_Feb_2024_buffer_15_basecase.pkl', 'rb') as file:
    net_dbl_park_minutes_df_inst_FCFS, \
    total_veh_delay_inst_FCFS, \
    queue_duration_inst_FCFS, \
    t_queue_remove_inst_FCFS, \
    avg_len_queue_inst_FCFS, \
    net_dbl_park_minutes_df_inst_phi5, \
    total_veh_delay_inst_phi5, \
    queue_duration_inst_phi5, \
    t_queue_remove_inst_phi5, \
    avg_len_queue_inst_phi5, \
    net_dbl_park_minutes_Diff_df_inst_phi5, \
    total_veh_delay_Diff_inst_phi5, \
    queue_duration_Diff_inst_phi5, \
    t_queue_remove_Diff_inst_phi5, \
    avg_len_queue_Diff_inst_phi5 \
        = pickle.load(file)


#***********Pittsburgh w/ buffer 5**************************************************
#new, random uniform number of DVs, 100 iteration, run for record, buffer 5
with open('pub_Pitt_run_for_record_18_Jan_2024_buffer_15.pkl', 'rb') as file:
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

#pub_Pitt_queuing_data_post_process_phi5_limit30_midpt_24_Mar_2023_buffer_5_basecase.pkl
#pub_Pitt_queuing_data_post_process_phi5_limit30_midpt_24_Mar_2023_buffer_5_pessimistic.pkl
#pub_Pitt_queuing_data_post_process_phi5_limit30_midpt_24_Mar_2023_buffer_5_optimistic.pkl

with open('pub_Pitt_queuing_data_post_process_phi5_limit30_midpt_24_Mar_2023_buffer_5_basecase.pkl', 'rb') as file:
    net_dbl_park_minutes_df_inst_FCFS, \
    total_veh_delay_inst_FCFS, \
    queue_duration_inst_FCFS, \
    t_queue_remove_inst_FCFS, \
    avg_len_queue_inst_FCFS, \
    net_dbl_park_minutes_df_inst_phi5, \
    total_veh_delay_inst_phi5, \
    queue_duration_inst_phi5, \
    t_queue_remove_inst_phi5, \
    avg_len_queue_inst_phi5, \
    net_dbl_park_minutes_Diff_df_inst_phi5, \
    total_veh_delay_Diff_inst_phi5, \
    queue_duration_Diff_inst_phi5, \
    t_queue_remove_Diff_inst_phi5, \
    avg_len_queue_Diff_inst_phi5 \
        = pickle.load(file)


#The total_veh_delay_Diff_inst_phi5 df has all of the data, but stored in lists, need to get this data
#out of the list format so that we can do math on the elements


total_veh_delay_Diff = total_veh_delay_Diff_inst_phi5.applymap(lambda x: np.mean(x))


data_df = pd.DataFrame()

c_list = [1, 2, 3, 4, 5, 6, 7]
c_list = [1,2,4,7]
#c_list = [1,4,7]
c_list = [1]
for c in c_list:
    #create a series to represent the specific number of parking spaces we are looking at
    parking_space = pd.Series([c]*100, name = 'Parking Spaces') #*100 for the original data set, *50 for the R2R
    #pull the normalized parking demand for a specific number of parking spaces
    parking_space_demand = pd.Series(n_index_norm_lst_df[c], name = 'norm parking demand')
    #pull the associated reduction in total vehicle delay
    redux_time = pd.Series(total_veh_delay_Diff[c]/60*365, name = 'redux_time') #/11/c  #or convert to hours per year /60*365, have min per day, convert to hours per day * 365 days in a year
    #pull the associated reduction in total vehicle delay / by 240 for fuel consumption
    redux_fuel = pd.Series(total_veh_delay_Diff[c]/240*365, name = 'redux_fuel') #/11/c/240 #or convert to gallons per year /240*365, have min per day, convert to gallons per day * 365 days
    
    #combine this in column form
    df = pd.concat([parking_space, parking_space_demand, redux_time, redux_fuel], axis = 1)
    #sort the data based on the norm parking demand
    df = df.sort_values(by = ['norm parking demand'], ascending = [True], ignore_index = True)
    
    #now, calculate the rolling average
    rolling_avg = df['redux_fuel'].rolling(21).mean().shift(-10)  #rolling(11).shift(-5)
    #append the rolling average data to the dataframe
    df['rolling avg fuel'] = rolling_avg
    
    
    data_df = pd.concat([data_df, df], ignore_index = True)


plt.figure()
fig, ax1 = plt.subplots(1,1)

sns.scatterplot(x = 'norm parking demand', y = 'redux_time', data = data_df, hue = 'Parking Spaces', palette = 'tab10', marker = 'X', legend = None, ax = ax1)

ax2 = ax1.twinx()
sns.scatterplot(x = 'norm parking demand', y = 'redux_fuel', data = data_df, hue = 'Parking Spaces', palette = 'tab10', marker = 'X', legend = None, ax = ax2)
sns.lineplot(x = 'norm parking demand', y = 'rolling avg fuel', data = data_df, hue = 'Parking Spaces', palette = 'tab10', ci = None, linewidth = 3)

#plt.suptitle("Reduction in Vehicle Delay and Fuel Consumption (\u03A6 = 5, \u03A8 = 5)")
#plt.title("(Aspen, base case traffic, 21-sample rolling average)")

ax1.set_ylabel('Reduction in Total Vehicle Delay\n(minutes per hour per parking space)')
ax2.set_ylabel('Reduction in Fuel Lost\n(gallons per hour per parking space)')
ax1.set_xlabel("Number of Deliveries\n(per parking space per hour)")

#plt.legend(title = 'Parking Spaces', loc = 'lower right', prop={'size': 8})
plt.legend(title = 'Parking Spaces', prop={'size': 8}) #loc = 'upper left',
ax1.axhline(y = 0, xmin = 0, xmax = 6, linewidth=2, color='k', linestyle = '--')
#ax1.set_ylim(-15500, 18000)
#ax2.set_ylim(-15500/4, 18000/4)

plt.savefig("output.jpg", bbox_inches = 'tight')

##############################################################################




###############################################################################
#Lane Obstruction Overtime Comparison

import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['figure.dpi'] = 500


# optimal w/ buffer, randomly shifted arrivals, reassassed parking schedule, run
# the below load instead
with open('pub_Aspen_reassessed_combined_18_Jan_2024_buffer_15.pkl', 'rb') as file:
        n_index_lst_df, \
        n_index_norm_lst_df, \
        arrival_dfs_df, \
        sum_service_df, \
        dbl_park_Opt_status_inst_phi5_df, \
        PAPvAP_inst_phi5_df, \
        park_demand_Opt_inst_phi5_df, \
        park_events_df_inst_phi5_shifted, \
        park_events_df_inst_phi5_shifted, \
        runtime, \
        buffer, \
        end, \
        iterations, \
        max_parking_spaces, \
        phi, \
        park_events_df_inst_phi5_df, \
        dbl_park_events_df_inst_phi5_df, \
        dbl_park_events_df_inst_FCFS_df, \
        Events, \
        late_no_starts_1, \
        late_no_starts_more_1, \
        early_no_starts_1, \
        early_no_starts_more_1, \
        change_sum_dbl_parking, \
        change_legal_and_dbl \
            = pickle.load(file)

with open('pub_Aspen_net_dbl_parking_14_Feb_2024_buffer_15.pkl', 'rb') as file:
    net_dbl_park_events_df_inst_FCFS, \
    net_dbl_park_events_df_inst_phi5, \
    max_parking_spaces, \
    iterations\
        = pickle.load(file)
        
file.close()



# with open('pub_Pitt_reassessed_combined_2_Dec_2022_buffer_5.pkl', 'rb') as file:
#         n_index_lst_df, \
#         n_index_norm_lst_df, \
#         arrival_dfs_df, \
#         sum_service_df, \
#         dbl_park_Opt_status_inst_phi5_df, \
#         PAPvAP_inst_phi5_df, \
#         park_demand_Opt_inst_phi5_df, \
#         park_events_df_inst_phi5_shifted, \
#         park_events_df_inst_phi5_shifted, \
#         runtime, \
#         buffer, \
#         end, \
#         iterations, \
#         max_parking_spaces, \
#         phi, \
#         park_events_df_inst_phi5_df, \
#         dbl_park_events_df_inst_phi5_df, \
#         dbl_park_events_df_inst_FCFS_df, \
#         Events, \
#         late_no_starts_1, \
#         late_no_starts_more_1, \
#         early_no_starts_1, \
#         early_no_starts_more_1, \
#         change_sum_dbl_parking, \
#         change_legal_and_dbl \
#             = pickle.load(file)

# with open('pub_Pitt_net_dbl_parking_2_Dec_2022_buffer_5.pkl', 'rb') as file:
#     net_dbl_park_events_df_inst_FCFS, \
#     net_dbl_park_events_df_inst_phi5, \
#     max_parking_spaces, \
#     iterations\
#         = pickle.load(file)
        
# file.close()


#circling back to look at the worst case redux in dbl parking for 7 parking spaces
# requires pub\_Aspen\_reassessed\_combined\_1\_Dec\_2022\_buffer\_5.pkl
total_dbl_park_Diff_df = pd.DataFrame()

#for c in range(1,8):
for c in [1,2,4,7]:
    
    dbl_park = []
    
    for i in range(0,50): #100 for OG work, 50 for R2R
        FCFS = dbl_park_events_df_inst_FCFS_df.iloc[i][c]
        phi5 = dbl_park_events_df_inst_phi5_df.iloc[i][c]
        total_dbl_park_FCFS = FCFS['s_i'].sum()
        total_dbl_park_phi5 = phi5['s_i'].sum()
        total_dbl_park_Diff = total_dbl_park_FCFS - total_dbl_park_phi5
        dbl_park.append(total_dbl_park_Diff)

    total_dbl_park_Diff_df[c] = dbl_park



#Updated method of graphing that shows the number of dbl parked vehicles over time
import matplotlib.pyplot as plt

i = 25  #25 for Aspen buffer 15, 
c = 1   #1 for Aspen buffer 15, 

#start with FCFS
FCFS = dbl_park_events_df_inst_FCFS_df.iloc[i][c]

arrivals = pd.DataFrame({'Truck': FCFS['Truck'], 'Time': FCFS['a_i']})
arrivals['Event'] = 'arrival'
departures = pd.DataFrame({'Truck': FCFS['Truck'],'Time': FCFS['d_i']})
departures['Event'] = 'departure'
FCFS_sched = pd.concat([arrivals, departures], axis = 0)
FCFS_sched.sort_values(by = 'Time', inplace = True)

counter_ls = []
counter = 0

for row in range(0, len(FCFS_sched)):
    if FCFS_sched.iloc[row]['Event'] == 'arrival':
        counter += 1
        counter_ls.append(counter)
    elif FCFS_sched.iloc[row]['Event'] == 'departure':
        counter -= 1
        counter_ls.append(counter)
    
FCFS_sched['Counter'] = counter_ls

#organize and counter the phi5 data as well
phi5 = dbl_park_events_df_inst_phi5_df.iloc[i][c]

arrivals = pd.DataFrame({'Truck': phi5['Truck'], 'Time': phi5['a_i']})
arrivals['Event'] = 'arrival'
departures = pd.DataFrame({'Truck': phi5['Truck'],'Time': phi5['d_i']})
departures['Event'] = 'departure'
phi5_sched = pd.concat([arrivals, departures], axis = 0)
phi5_sched.sort_values(by = 'Time', inplace = True)

counter_ls = []
counter = 0

for row in range(0, len(phi5_sched)):
    if phi5_sched.iloc[row]['Event'] == 'arrival':
        counter += 1
        counter_ls.append(counter)
    elif phi5_sched.iloc[row]['Event'] == 'departure':
        counter -= 1
        counter_ls.append(counter)
    
phi5_sched['Counter'] = counter_ls


#Graph it!
plt.figure
plt.step(x = FCFS_sched['Time'], y = FCFS_sched['Counter'], label = 'FCFS', where = 'post')
plt.step(x = phi5_sched['Time'], y = phi5_sched['Counter'], label = 'Optimal (phi5)', where = 'post')
plt.legend()
plt.xlabel('Time (minutes)')
plt.ylabel('Number of Double Parked Vehicles')
#plt.title('Number of Double Parked Vehicles Over Time\n(Instance = ' + str(i) + ', Num Parking Spaces = ' + str(c) + ')')
#plt.xlim([635, 680])

plt.savefig("output.jpg", bbox_inches = 'tight')
plt.show()


#still interesting to see the total lane obstruction number as well
FCFS_lane_ob = net_dbl_park_events_df_inst_FCFS.iloc[i][c][0]
phi5_lane_ob = net_dbl_park_events_df_inst_phi5.iloc[i][c][0]

print('Total min of lane obstruction for FCFS = ' + str(FCFS_lane_ob['Total'].sum()) + ' , phi5 = ' + str(phi5_lane_ob['Total'].sum()))






##############################################################################

#Boxplot comparison between an extra parking space and smart curbs


data_df = pd.DataFrame(np.empty((2800, 4), dtype = float), columns = ["Parking Spaces","Phi", "Inst", "Redux Ratio"])
row = 0



Opt_phi_dfs = [dbl_park_Opt_inst_phi0_df,
               dbl_park_Opt_inst_phi1_df,
               dbl_park_Opt_inst_phi2_df,
               dbl_park_Opt_inst_phi5_df,
               dbl_park_Opt_inst_phi10_df,
               dbl_park_Opt_inst_phi15_df,
               dbl_park_Opt_inst_phi30_df,
               ]

c_list = [1,2,3,4,5,6,7] #change dataframe size to (4900, 4) as well
c_list = [1,2,4,7]
for c_index in c_list:
    
    phi_index = -1
    
    
    for item in Opt_phi_dfs:
        
        phi_index += 1
        
        for i_index in range(0, iterations):
            
            if c_index == 1:
                data_df.iloc[row, 0] = str(c_index)
                data_df.iloc[row, 1] = str(phi[phi_index])
                data_df.iloc[row, 2] = i_index
                ratio_smart = 1 - (item.iloc[i_index, c_index -1] / dbl_park_FCFS_instance_df.iloc[i_index, c_index -1])
                ratio_extra = 1 - (dbl_park_FCFS_instance_df_1_2.iloc[i_index, 0] / dbl_park_FCFS_instance_df.iloc[i_index, c_index -1])
                redux_ratio = ratio_smart / ratio_extra
                #ratio_smart = dbl_park_FCFS_instance_df.iloc[i_index, c_index -1] / dbl_park_Opt_inst_phi0_df.iloc[i_index, c_index -1]
                #ratio_extra = dbl_park_FCFS_instance_df.iloc[i_index, c_index -1] / dbl_park_FCFS_instance_df_1_2.iloc[i_index, 0]
                #redux_ratio = ratio_smart / ratio_extra #equivalent to FCFS_1_2 / Opt
                data_df.iloc[row, 3] = redux_ratio
                
                row += 1
                
            elif c_index == 2:
                data_df.iloc[row, 0] = str(c_index)
                data_df.iloc[row, 1] = str(phi[phi_index])
                data_df.iloc[row, 2] = i_index
                ratio_smart = 1 - (item.iloc[i_index, c_index -1] / dbl_park_FCFS_instance_df.iloc[i_index, c_index -1])
                ratio_extra = 1 - (dbl_park_FCFS_instance_df_2_3.iloc[i_index, 0] / dbl_park_FCFS_instance_df.iloc[i_index, c_index -1])
                redux_ratio = ratio_smart / ratio_extra
                data_df.iloc[row, 3] = redux_ratio
                
                row += 1
                
            elif c_index == 3:
                data_df.iloc[row, 0] = str(c_index)
                data_df.iloc[row, 1] = str(phi[phi_index])
                data_df.iloc[row, 2] = i_index
                ratio_smart = 1 - (item.iloc[i_index, c_index -1] / dbl_park_FCFS_instance_df.iloc[i_index, c_index -1])
                ratio_extra = 1 - (dbl_park_FCFS_instance_df_3_4.iloc[i_index, 0] / dbl_park_FCFS_instance_df.iloc[i_index, c_index -1])
                redux_ratio = ratio_smart / ratio_extra
                data_df.iloc[row, 3] = redux_ratio
                
                row += 1
                
            elif c_index == 4:
                data_df.iloc[row, 0] = str(c_index)
                data_df.iloc[row, 1] = str(phi[phi_index])
                data_df.iloc[row, 2] = i_index
                ratio_smart = 1 - (item.iloc[i_index, c_index -1] / dbl_park_FCFS_instance_df.iloc[i_index, c_index -1])
                ratio_extra = 1 - (dbl_park_FCFS_instance_df_4_5.iloc[i_index, 0] / dbl_park_FCFS_instance_df.iloc[i_index, c_index -1])
                redux_ratio = ratio_smart / ratio_extra
                data_df.iloc[row, 3] = redux_ratio
                
                row += 1
                
            elif c_index == 5:
                data_df.iloc[row, 0] = str(c_index)
                data_df.iloc[row, 1] = str(phi[phi_index])
                data_df.iloc[row, 2] = i_index
                ratio_smart = 1 - (item.iloc[i_index, c_index -1] / dbl_park_FCFS_instance_df.iloc[i_index, c_index -1])
                ratio_extra = 1 - (dbl_park_FCFS_instance_df_5_6.iloc[i_index, 0] / dbl_park_FCFS_instance_df.iloc[i_index, c_index -1])
                redux_ratio = ratio_smart / ratio_extra
                data_df.iloc[row, 3] = redux_ratio
                
                row += 1
                
            elif c_index == 6:
                data_df.iloc[row, 0] = str(c_index)
                data_df.iloc[row, 1] = str(phi[phi_index])
                data_df.iloc[row, 2] = i_index
                ratio_smart = 1 - (item.iloc[i_index, c_index -1] / dbl_park_FCFS_instance_df.iloc[i_index, c_index -1])
                ratio_extra = 1 - (dbl_park_FCFS_instance_df_6_7.iloc[i_index, 0] / dbl_park_FCFS_instance_df.iloc[i_index, c_index -1])
                redux_ratio = ratio_smart / ratio_extra
                data_df.iloc[row, 3] = redux_ratio
                
                row += 1
                
            elif c_index == 7:
                data_df.iloc[row, 0] = str(c_index)
                data_df.iloc[row, 1] = str(phi[phi_index])
                data_df.iloc[row, 2] = i_index
                ratio_smart = 1 - (item.iloc[i_index, c_index -1] / dbl_park_FCFS_instance_df.iloc[i_index, c_index -1])
                ratio_extra = 1 - (dbl_park_FCFS_instance_df_7_8.iloc[i_index, 0] / dbl_park_FCFS_instance_df.iloc[i_index, c_index -1])
                redux_ratio = ratio_smart / ratio_extra
                data_df.iloc[row, 3] = redux_ratio
                
                row += 1


plt.figure()
sns.boxplot(x = 'Phi', y = 'Redux Ratio', hue = 'Parking Spaces', data = data_df)
plt.axhline(y = 1, xmin = 0, xmax = 6, linewidth=2, color='r', linestyle = '--')
#plt.title('Parking Capacity Expansion Equivalence \n of Smart Curb Management \n(Pittsburgh Dataset)')
plt.xlabel('Minutes of Delivery Vehicle Arrival Flexibility, \u03A6')
plt.ylabel('Ratio of Reduction in Double Parking \n (Convert to Smart Curb / add 1 Parking Space)')
#plt.ylim([-0.5, 5.75])

plt.savefig("output.jpg", bbox_inches = 'tight')


###############################################################################
#Normalize reduction in double parking by total service requested per hour per parking space















data_df = pd.DataFrame()

c_list = [1,2,3,4,5,6,7]
c_list = [1,2,4,7]
#c_list = [1]
for c in c_list:
    #create a series to represent the specific number of parking spaces we are looking at
    parking_space = pd.Series([c]*100, name = 'Parking Spaces')
    #pull the normalized parking demand for a specific number of parking spaces
    parking_space_demand = pd.Series(n_index_norm_lst_df[c], name = 'norm parking demand')
    #pull the associated reduction in double parking
    redux = pd.Series(dbl_park_Diff_inst_phi5_df[c]/20/c, name = 'redux')
    #combine this two in column form
    df = pd.concat([parking_space, parking_space_demand, redux], axis = 1)
    #sort the data based on the norm parking demand
    df = df.sort_values(by = ['norm parking demand'], ascending = [True], ignore_index = True)
    #now, calculate the rolling average
    rolling_avg = df['redux'].rolling(11).mean().shift(-5)
    #append the rolling average data to the dataframe
    df['rolling avg'] = rolling_avg
    
    data_df = pd.concat([data_df, df], ignore_index = True)

    
plt.figure()

#sns.scatterplot(x = 'Vehicle Demand Norm', y = 'Redux Dbl Park phi5', data = data_df, hue = 'Parking Spaces', palette = "tab10")
sns.lineplot(x = 'norm parking demand', y = 'rolling avg', data = data_df, hue = 'Parking Spaces', palette = "tab10", ci = None)
sns.scatterplot(x = 'norm parking demand', y = 'redux', data = data_df, hue = 'Parking Spaces', palette = "tab10", marker = 'X', legend = False) #alpha = 0.4, 
plt.axhline(y = 0, xmin = 0, xmax = 6, linewidth=2, color='k', linestyle = '--')
plt.suptitle('Reduction in Double Parking (\u03A6 = 5, \u03A8 = 0)')
plt.title('(Pittsburgh, 11-sample rolling average)')
plt.xlabel('Number of Deliveries \n (per Parking Space per Hour)')
plt.ylabel('Reduction in Double Parking \n (minutes per hour per parking space)')
plt.ylim([-0.75, 9.75])
plt.legend(title = 'Parking Spaces', loc = 'upper left', prop={'size': 8})



















###############################################################################














##############################################################################
#investigating the Pittsburgh data drop around normalized demand of 4 vehicle per hour per parking space


data_df = pd.DataFrame()

c_list = [1,2,3,4,5,6,7]
c_list = [1,2,4,7]
c_list = [1]
for c in c_list:
    #create a series to represent the specific number of parking spaces we are looking at
    parking_space = pd.Series([c]*100, name = 'Parking Spaces')
    #pull the normalized parking demand for a specific number of parking spaces
    parking_space_demand = pd.Series(n_index_norm_lst_df[c], name = 'norm parking demand')
    #pull the associated reduction in double parking
    obj = pd.Series(dbl_park_Opt_inst_phi5_df[c]/20/c, name = 'obj')
    #combine this two in column form
    df = pd.concat([parking_space, parking_space_demand, obj], axis = 1)
    #sort the data based on the norm parking demand
    df = df.sort_values(by = ['norm parking demand'], ascending = [True], ignore_index = True)
    #now, calculate the rolling average
    rolling_avg = df['obj'].rolling(11).mean().shift(-5)
    #append the rolling average data to the dataframe
    df['rolling avg'] = rolling_avg
    
    data_df = pd.concat([data_df, df], ignore_index = True)

    
plt.figure()

#sns.scatterplot(x = 'Vehicle Demand Norm', y = 'Redux Dbl Park phi5', data = data_df, hue = 'Parking Spaces', palette = "tab10")
sns.lineplot(x = 'norm parking demand', y = 'rolling avg', data = data_df, hue = 'Parking Spaces', palette = "tab10", ci = None)
sns.scatterplot(x = 'norm parking demand', y = 'obj', data = data_df, hue = 'Parking Spaces', palette = "tab10", marker = 'X', legend = False) #alpha = 0.4, 
plt.axhline(y = 0, xmin = 0, xmax = 6, linewidth=2, color='k', linestyle = '--')
plt.suptitle('Double Parking Minutes Optimal (\u03A6 = 5, \u03A8 = 0)')
plt.title('(Pittsburgh, 11-sample rolling average)')
plt.xlabel('Number of Deliveries \n (per Parking Space per Hour)')
plt.ylabel('Double Parking in the Optimal Solultion\n (minutes per hour per parking space)')
#plt.ylim([-3, 14])
plt.legend(title = 'Parking Spaces', loc = 'upper left', prop={'size': 8})


#################################Look at FCFS as well


data_df = pd.DataFrame()

c_list = [1,2,3,4,5,6,7]
c_list = [1,2,4,7]
c_list = [1]
for c in c_list:
    #create a series to represent the specific number of parking spaces we are looking at
    parking_space = pd.Series([c]*100, name = 'Parking Spaces')
    #pull the normalized parking demand for a specific number of parking spaces
    parking_space_demand = pd.Series(n_index_norm_lst_df[c], name = 'norm parking demand')
    #pull the associated reduction in double parking
    obj = pd.Series(dbl_park_FCFS_instance_df[c]/20/c, name = 'FCFS')
    #combine this two in column form
    df = pd.concat([parking_space, parking_space_demand, obj], axis = 1)
    #sort the data based on the norm parking demand
    df = df.sort_values(by = ['norm parking demand'], ascending = [True], ignore_index = True)
    #now, calculate the rolling average
    rolling_avg = df['FCFS'].rolling(11).mean().shift(-5)
    #append the rolling average data to the dataframe
    df['rolling avg'] = rolling_avg
    
    data_df = pd.concat([data_df, df], ignore_index = True)

    
plt.figure()

#sns.scatterplot(x = 'Vehicle Demand Norm', y = 'Redux Dbl Park phi5', data = data_df, hue = 'Parking Spaces', palette = "tab10")
sns.lineplot(x = 'norm parking demand', y = 'rolling avg', data = data_df, hue = 'Parking Spaces', palette = "tab10", ci = None)
sns.scatterplot(x = 'norm parking demand', y = 'FCFS', data = data_df, hue = 'Parking Spaces', palette = "tab10", marker = 'X', legend = False) #alpha = 0.4, 
plt.axhline(y = 0, xmin = 0, xmax = 6, linewidth=2, color='k', linestyle = '--')
plt.suptitle('Double Parking Minutes FCFS')
plt.title('(Pittsburgh, 11-sample rolling average)')
plt.xlabel('Number of Deliveries \n (per Parking Space per Hour)')
plt.ylabel('Double Parking with FCFS\n (minutes per hour per parking space)')
#plt.ylim([-3, 14])
plt.legend(title = 'Parking Spaces', loc = 'upper left', prop={'size': 8})



##############################################################################
#investigating the Aspen data spike around normalized demand of 4 vehicle per hour per parking space


data_df = pd.DataFrame()

c_list = [1,2,3,4,5,6,7]
c_list = [1,2,4,7]
c_list = [1]
for c in c_list:
    #create a series to represent the specific number of parking spaces we are looking at
    parking_space = pd.Series([c]*100, name = 'Parking Spaces')
    #pull the normalized parking demand for a specific number of parking spaces
    parking_space_demand = pd.Series(n_index_norm_lst_df[c], name = 'norm parking demand')
    #pull the associated reduction in double parking
    obj = pd.Series(dbl_park_Opt_inst_phi5_df[c]/11/c, name = 'obj')
    #combine this two in column form
    df = pd.concat([parking_space, parking_space_demand, obj], axis = 1)
    #sort the data based on the norm parking demand
    df = df.sort_values(by = ['norm parking demand'], ascending = [True], ignore_index = True)
    #now, calculate the rolling average
    rolling_avg = df['obj'].rolling(11).mean().shift(-5)
    #append the rolling average data to the dataframe
    df['rolling avg'] = rolling_avg
    
    data_df = pd.concat([data_df, df], ignore_index = True)

    
plt.figure()

#sns.scatterplot(x = 'Vehicle Demand Norm', y = 'Redux Dbl Park phi5', data = data_df, hue = 'Parking Spaces', palette = "tab10")
sns.lineplot(x = 'norm parking demand', y = 'rolling avg', data = data_df, hue = 'Parking Spaces', palette = "tab10", ci = None)
sns.scatterplot(x = 'norm parking demand', y = 'obj', data = data_df, hue = 'Parking Spaces', palette = "tab10", marker = 'X', legend = False) #alpha = 0.4, 
plt.axhline(y = 0, xmin = 0, xmax = 6, linewidth=2, color='k', linestyle = '--')
plt.suptitle('Double Parking Minutes Optimal (\u03A6 = 5, \u03A8 = 0)')
plt.title('(Aspen, 11-sample rolling average)')
plt.xlabel('Number of Deliveries \n (per Parking Space per Hour)')
plt.ylabel('Double Parking in the Optimal Solultion\n (minutes per hour per parking space)')
#plt.ylim([-3, 14])
plt.legend(title = 'Parking Spaces', loc = 'upper left', prop={'size': 8})


#################################Look at FCFS as well


data_df = pd.DataFrame()

c_list = [1,2,3,4,5,6,7]
c_list = [1,2,4,7]
c_list = [1]
for c in c_list:
    #create a series to represent the specific number of parking spaces we are looking at
    parking_space = pd.Series([c]*100, name = 'Parking Spaces')
    #pull the normalized parking demand for a specific number of parking spaces
    parking_space_demand = pd.Series(n_index_norm_lst_df[c], name = 'norm parking demand')
    #pull the associated reduction in double parking
    obj = pd.Series(dbl_park_FCFS_instance_df[c]/11/c, name = 'FCFS')
    #combine this two in column form
    df = pd.concat([parking_space, parking_space_demand, obj], axis = 1)
    #sort the data based on the norm parking demand
    df = df.sort_values(by = ['norm parking demand'], ascending = [True], ignore_index = True)
    #now, calculate the rolling average
    rolling_avg = df['FCFS'].rolling(11).mean().shift(-5)
    #append the rolling average data to the dataframe
    df['rolling avg'] = rolling_avg
    
    data_df = pd.concat([data_df, df], ignore_index = True)

    
plt.figure()

#sns.scatterplot(x = 'Vehicle Demand Norm', y = 'Redux Dbl Park phi5', data = data_df, hue = 'Parking Spaces', palette = "tab10")
sns.lineplot(x = 'norm parking demand', y = 'rolling avg', data = data_df, hue = 'Parking Spaces', palette = "tab10", ci = None)
sns.scatterplot(x = 'norm parking demand', y = 'FCFS', data = data_df, hue = 'Parking Spaces', palette = "tab10", marker = 'X', legend = False) #alpha = 0.4, 
plt.axhline(y = 0, xmin = 0, xmax = 6, linewidth=2, color='k', linestyle = '--')
plt.suptitle('Double Parking Minutes FCFS')
plt.title('(Aspen, 11-sample rolling average)')
plt.xlabel('Number of Deliveries \n (per Parking Space per Hour)')
plt.ylabel('Double Parking with FCFS\n (minutes per hour per parking space)')
#plt.ylim([-3, 14])
plt.legend(title = 'Parking Spaces', loc = 'upper left', prop={'size': 8})




#******************************************************************************
# Investigating why with the Aspen dataset we have negative reductions in dbl parking
# minutes, e.g. more minutes of double parking for optimal versus FCFS, but we
# don't see this negative impact on fuel consumption and delay, e.g. data after 
# the queuing model

with open('pub_Aspen_net_dbl_parking_1_Dec_2022_buffer_5.pkl', 'rb') as file:
    net_dbl_park_events_df_inst_FCFS, \
    net_dbl_park_events_df_inst_phi5, \
    max_parking_spaces, \
    iterations\
        = pickle.load(file)
        
file.close()


FCFS_total_lane_obstruct = []
Opt_total_lane_obstruct = []

for i in range(0,100):
    df_FCFS = net_dbl_park_events_df_inst_FCFS.iloc[i, 0][0]
    if df_FCFS.empty == False:
        FCFS_total_lane_obstruct_inst = df_FCFS['Total'].sum()
        FCFS_total_lane_obstruct.append(FCFS_total_lane_obstruct_inst)
    else:
        FCFS_total_lane_obstruct.append(0)
    
    df_Opt = net_dbl_park_events_df_inst_phi5.iloc[i, 0][0]
    if df_Opt.empty == False:
        Opt_total_lane_obstruct_inst = df_Opt['Total'].sum()
        Opt_total_lane_obstruct.append(Opt_total_lane_obstruct_inst)
    else:
        Opt_total_lane_obstruct.append(0)

array1 = np.array(FCFS_total_lane_obstruct)
array2 = np.array(Opt_total_lane_obstruct)
array3 = array1 - array2

plt.figure()
plt.scatter(range(0,100),array1)
plt.scatter(range(0,100),array2)
plt.scatter(range(0,100),array3, marker = 'x')
plt.legend(['FCFS Lane Obstruct', 'Opt Lane Obstruct', 'Diff Lane Obstruct'])
plt.axhline(y = 0, xmin = 0, xmax = 100, linewidth=2, color='k', linestyle = '--')
plt.axhline(y = 660, xmin = 0, xmax = 100, linewidth=2, color='k', linestyle = '--')
plt.ylim(ymax = 750, ymin = -250)
plt.ylabel('Minutes of Lane Obstruction')
plt.xlabel('Iteration')




    
#*****************************Old Stuff****************************************
    
 
#run for record, but focused on 1 parking space and extending n to look for an approach to
#zero for the redux in double parking
with open('run_for_record_31_July_2022_extended_n.pkl', 'rb') as file:
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
        
#run for record, but focused on 7 parking spaces and extending n to look for an approach to
#zero for the redux in double parking
with open('run_for_record_2_August_2022_extended_n_7_spaces.pkl', 'rb') as file:
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


     



#short test to see if changes to Q generation had any impact on the results. Needed
#to change Q to that there would not be an delivery vehicles that would have
#their arrival + service exceed the end of the scenario
with open('run_for_record_16_August_2022_test.pkl', 'rb') as file:
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




with open('net_dbl_parking.pkl', 'rb') as file:
    net_dbl_park_events_df_inst_FCFS, \
    net_dbl_park_events_df_inst_phi0, \
    net_dbl_park_events_df_inst_phi1, \
    net_dbl_park_events_df_inst_phi2, \
    net_dbl_park_events_df_inst_phi5, \
    net_dbl_park_events_df_inst_phi10, \
    net_dbl_park_events_df_inst_phi15, \
    net_dbl_park_events_df_inst_phi30, \
    truck_scenarios, \
    max_parking_spaces, \
    iterations,\
    max_trucks\
        = pickle.load(file)
        
file.close()

with open('queuing_data_post_process_phi0_low.pkl', 'rb') as file:
    net_dbl_park_minutes_df_inst_FCFS, \
    total_veh_delay_inst_FCFS, \
    total_veh_delay_error_inst_FCFS, \
    queue_duration_inst_FCFS, \
    t_queue_remove_inst_FCFS, \
    veh_in_queue_inst_FCFS, \
    avg_veh_delay_inst_FCFS, \
    avg_len_queue_inst_FCFS, \
    net_dbl_park_minutes_df_inst_phi0, \
    total_veh_delay_inst_phi0, \
    total_veh_delay_error_inst_phi0, \
    queue_duration_inst_phi0, \
    t_queue_remove_inst_phi0, \
    veh_in_queue_inst_phi0, \
    avg_veh_delay_inst_phi0, \
    avg_len_queue_inst_phi0, \
    net_dbl_park_minutes_Diff_df_inst_phi0, \
    total_veh_delay_Diff_inst_phi0, \
    total_veh_delay_error_Diff_inst_phi0, \
    queue_duration_Diff_inst_phi0, \
    t_queue_remove_Diff_inst_phi0, \
    veh_in_queue_Diff_inst_phi0, \
    avg_veh_delay_Diff_inst_phi0, \
    avg_len_queue_Diff_inst_phi0, \
    AVG_net_dbl_park_minutes_Diff_df_inst_phi0, \
    AVG_total_veh_delay_Diff_inst_phi0, \
    AVG_total_veh_delay_error_Diff_inst_phi0, \
    AVG_queue_duration_Diff_inst_phi0, \
    AVG_t_queue_remove_Diff_inst_phi0, \
    AVG_veh_in_queue_Diff_inst_phi0, \
    AVG_avg_veh_delay_Diff_inst_phi0, \
    AVG_avg_len_queue_Diff_inst_phi0 \
        = pickle.load(file)
        
file.close()

with open('queuing_data_post_process_phi0_med.pkl', 'rb') as file:
    net_dbl_park_minutes_df_inst_FCFS, \
    total_veh_delay_inst_FCFS, \
    total_veh_delay_error_inst_FCFS, \
    queue_duration_inst_FCFS, \
    t_queue_remove_inst_FCFS, \
    veh_in_queue_inst_FCFS, \
    avg_veh_delay_inst_FCFS, \
    avg_len_queue_inst_FCFS, \
    net_dbl_park_minutes_df_inst_phi0, \
    total_veh_delay_inst_phi0, \
    total_veh_delay_error_inst_phi0, \
    queue_duration_inst_phi0, \
    t_queue_remove_inst_phi0, \
    veh_in_queue_inst_phi0, \
    avg_veh_delay_inst_phi0, \
    avg_len_queue_inst_phi0, \
    net_dbl_park_minutes_Diff_df_inst_phi0, \
    total_veh_delay_Diff_inst_phi0, \
    total_veh_delay_error_Diff_inst_phi0, \
    queue_duration_Diff_inst_phi0, \
    t_queue_remove_Diff_inst_phi0, \
    veh_in_queue_Diff_inst_phi0, \
    avg_veh_delay_Diff_inst_phi0, \
    avg_len_queue_Diff_inst_phi0, \
    AVG_net_dbl_park_minutes_Diff_df_inst_phi0, \
    AVG_total_veh_delay_Diff_inst_phi0, \
    AVG_total_veh_delay_error_Diff_inst_phi0, \
    AVG_queue_duration_Diff_inst_phi0, \
    AVG_t_queue_remove_Diff_inst_phi0, \
    AVG_veh_in_queue_Diff_inst_phi0, \
    AVG_avg_veh_delay_Diff_inst_phi0, \
    AVG_avg_len_queue_Diff_inst_phi0 \
        = pickle.load(file)
        
file.close()

#phi5 data from low scenario, no queue limit
with open('queuing_data_post_process_phi5_low.pkl', 'rb') as file:
    net_dbl_park_minutes_df_inst_FCFS, \
    total_veh_delay_inst_FCFS, \
    total_veh_delay_error_inst_FCFS, \
    queue_duration_inst_FCFS, \
    t_queue_remove_inst_FCFS, \
    veh_in_queue_inst_FCFS, \
    avg_veh_delay_inst_FCFS, \
    avg_len_queue_inst_FCFS, \
    net_dbl_park_minutes_df_inst_phi5, \
    total_veh_delay_inst_phi5, \
    total_veh_delay_error_inst_phi5, \
    queue_duration_inst_phi5, \
    t_queue_remove_inst_phi5, \
    veh_in_queue_inst_phi5, \
    avg_veh_delay_inst_phi5, \
    avg_len_queue_inst_phi5, \
    net_dbl_park_minutes_Diff_df_inst_phi5, \
    total_veh_delay_Diff_inst_phi5, \
    total_veh_delay_error_Diff_inst_phi5, \
    queue_duration_Diff_inst_phi5, \
    t_queue_remove_Diff_inst_phi5, \
    veh_in_queue_Diff_inst_phi5, \
    avg_veh_delay_Diff_inst_phi5, \
    avg_len_queue_Diff_inst_phi5, \
    AVG_net_dbl_park_minutes_Diff_df_inst_phi5, \
    AVG_total_veh_delay_Diff_inst_phi5, \
    AVG_total_veh_delay_error_Diff_inst_phi5, \
    AVG_queue_duration_Diff_inst_phi5, \
    AVG_t_queue_remove_Diff_inst_phi5, \
    AVG_veh_in_queue_Diff_inst_phi5, \
    AVG_avg_veh_delay_Diff_inst_phi5, \
    AVG_avg_len_queue_Diff_inst_phi5 \
        = pickle.load(file)
        
file.close()

#has limit but only for 5 iterations
with open('queuing_data_post_process_phi5_low_limit.pkl', 'rb') as file:
    net_dbl_park_minutes_df_inst_FCFS, \
    total_veh_delay_inst_FCFS, \
    total_veh_delay_error_inst_FCFS, \
    queue_duration_inst_FCFS, \
    t_queue_remove_inst_FCFS, \
    veh_in_queue_inst_FCFS, \
    max_veh_in_queue_inst_FCFS, \
    avg_veh_delay_inst_FCFS, \
    avg_len_queue_inst_FCFS, \
    net_dbl_park_minutes_df_inst_phi5, \
    total_veh_delay_inst_phi5, \
    total_veh_delay_error_inst_phi5, \
    queue_duration_inst_phi5, \
    t_queue_remove_inst_phi5, \
    veh_in_queue_inst_phi5, \
    max_veh_in_queue_inst_phi5, \
    avg_veh_delay_inst_phi5, \
    avg_len_queue_inst_phi5, \
    net_dbl_park_minutes_Diff_df_inst_phi5, \
    total_veh_delay_Diff_inst_phi5, \
    total_veh_delay_error_Diff_inst_phi5, \
    queue_duration_Diff_inst_phi5, \
    t_queue_remove_Diff_inst_phi5, \
    avg_veh_in_queue_Diff_inst_phi5, \
    max_veh_in_queue_Diff_inst_phi5, \
    avg_veh_delay_Diff_inst_phi5, \
    avg_len_queue_Diff_inst_phi5, \
    AVG_net_dbl_park_minutes_Diff_df_inst_phi5, \
    AVG_total_veh_delay_Diff_inst_phi5, \
    AVG_total_veh_delay_error_Diff_inst_phi5, \
    AVG_queue_duration_Diff_inst_phi5, \
    AVG_t_queue_remove_Diff_inst_phi5, \
    AVG_avg_veh_in_queue_Diff_inst_phi5, \
    AVG_max_veh_in_queue_Diff_inst_phi5, \
    AVG_avg_veh_delay_Diff_inst_phi5, \
    AVG_avg_len_queue_Diff_inst_phi5 \
        = pickle.load(file)

file.close()

import pickle
with open('queuing_data_post_process_phi5_low_limit30_partA.pkl', 'rb') as file:
    net_dbl_park_minutes_df_inst_FCFS, \
    total_veh_delay_inst_FCFS, \
    total_veh_delay_error_inst_FCFS, \
    queue_duration_inst_FCFS, \
    t_queue_remove_inst_FCFS, \
    veh_in_queue_inst_FCFS, \
    avg_veh_in_queue_inst_FCFS, \
    max_veh_in_queue_inst_FCFS, \
    avg_veh_delay_inst_FCFS, \
    avg_len_queue_inst_FCFS, \
    net_dbl_park_minutes_df_inst_phi5, \
    total_veh_delay_inst_phi5, \
    total_veh_delay_error_inst_phi5, \
    queue_duration_inst_phi5, \
    t_queue_remove_inst_phi5, \
    veh_in_queue_inst_phi5, \
    avg_veh_in_queue_inst_FCFS, \
    max_veh_in_queue_inst_phi5, \
    avg_veh_delay_inst_phi5, \
    avg_len_queue_inst_phi5, \
    net_dbl_park_minutes_Diff_df_inst_phi5, \
    total_veh_delay_Diff_inst_phi5, \
    total_veh_delay_error_Diff_inst_phi5, \
    queue_duration_Diff_inst_phi5, \
    t_queue_remove_Diff_inst_phi5, \
    avg_veh_in_queue_Diff_inst_phi5, \
    max_veh_in_queue_Diff_inst_phi5, \
    avg_veh_delay_Diff_inst_phi5, \
    avg_len_queue_Diff_inst_phi5, \
    AVG_net_dbl_park_minutes_Diff_df_inst_phi5, \
    AVG_total_veh_delay_Diff_inst_phi5, \
    AVG_total_veh_delay_error_Diff_inst_phi5, \
    AVG_queue_duration_Diff_inst_phi5, \
    AVG_t_queue_remove_Diff_inst_phi5, \
    AVG_avg_veh_in_queue_Diff_inst_phi5, \
    AVG_max_veh_in_queue_Diff_inst_phi5, \
    AVG_avg_veh_delay_Diff_inst_phi5, \
    AVG_avg_len_queue_Diff_inst_phi5, \
        = pickle.load(file)

file.close()


import pickle
with open('queuing_data_post_process_phi5_low_limit30.pkl', 'rb') as file:
    net_dbl_park_minutes_df_inst_FCFS, \
    total_veh_delay_inst_FCFS, \
    total_veh_delay_error_inst_FCFS, \
    queue_duration_inst_FCFS, \
    t_queue_remove_inst_FCFS, \
    veh_in_queue_inst_FCFS, \
    avg_veh_in_queue_inst_FCFS, \
    max_veh_in_queue_inst_FCFS, \
    avg_veh_delay_inst_FCFS, \
    avg_len_queue_inst_FCFS, \
    net_dbl_park_minutes_df_inst_phi5, \
    total_veh_delay_inst_phi5, \
    total_veh_delay_error_inst_phi5, \
    queue_duration_inst_phi5, \
    t_queue_remove_inst_phi5, \
    veh_in_queue_inst_phi5, \
    avg_veh_in_queue_inst_FCFS, \
    max_veh_in_queue_inst_phi5, \
    avg_veh_delay_inst_phi5, \
    avg_len_queue_inst_phi5, \
    net_dbl_park_minutes_Diff_df_inst_phi5, \
    total_veh_delay_Diff_inst_phi5, \
    total_veh_delay_error_Diff_inst_phi5, \
    queue_duration_Diff_inst_phi5, \
    t_queue_remove_Diff_inst_phi5, \
    avg_veh_in_queue_Diff_inst_phi5, \
    max_veh_in_queue_Diff_inst_phi5, \
    avg_veh_delay_Diff_inst_phi5, \
    avg_len_queue_Diff_inst_phi5, \
    AVG_net_dbl_park_minutes_Diff_df_inst_phi5, \
    AVG_total_veh_delay_Diff_inst_phi5, \
    AVG_total_veh_delay_error_Diff_inst_phi5, \
    AVG_queue_duration_Diff_inst_phi5, \
    AVG_t_queue_remove_Diff_inst_phi5, \
    AVG_avg_veh_in_queue_Diff_inst_phi5, \
    AVG_max_veh_in_queue_Diff_inst_phi5, \
    AVG_avg_veh_delay_Diff_inst_phi5, \
    AVG_avg_len_queue_Diff_inst_phi5, \
        = pickle.load(file)

file.close()

import pickle
with open('queuing_data_post_process_phi5_med_limit30.pkl', 'rb') as file:
    net_dbl_park_minutes_df_inst_FCFS, \
    total_veh_delay_inst_FCFS, \
    total_veh_delay_error_inst_FCFS, \
    queue_duration_inst_FCFS, \
    t_queue_remove_inst_FCFS, \
    veh_in_queue_inst_FCFS, \
    avg_veh_in_queue_inst_FCFS, \
    max_veh_in_queue_inst_FCFS, \
    avg_veh_delay_inst_FCFS, \
    avg_len_queue_inst_FCFS, \
    net_dbl_park_minutes_df_inst_phi5, \
    total_veh_delay_inst_phi5, \
    total_veh_delay_error_inst_phi5, \
    queue_duration_inst_phi5, \
    t_queue_remove_inst_phi5, \
    veh_in_queue_inst_phi5, \
    avg_veh_in_queue_inst_FCFS, \
    max_veh_in_queue_inst_phi5, \
    avg_veh_delay_inst_phi5, \
    avg_len_queue_inst_phi5, \
    net_dbl_park_minutes_Diff_df_inst_phi5, \
    total_veh_delay_Diff_inst_phi5, \
    total_veh_delay_error_Diff_inst_phi5, \
    queue_duration_Diff_inst_phi5, \
    t_queue_remove_Diff_inst_phi5, \
    avg_veh_in_queue_Diff_inst_phi5, \
    max_veh_in_queue_Diff_inst_phi5, \
    avg_veh_delay_Diff_inst_phi5, \
    avg_len_queue_Diff_inst_phi5, \
    AVG_net_dbl_park_minutes_Diff_df_inst_phi5, \
    AVG_total_veh_delay_Diff_inst_phi5, \
    AVG_total_veh_delay_error_Diff_inst_phi5, \
    AVG_queue_duration_Diff_inst_phi5, \
    AVG_t_queue_remove_Diff_inst_phi5, \
    AVG_avg_veh_in_queue_Diff_inst_phi5, \
    AVG_max_veh_in_queue_Diff_inst_phi5, \
    AVG_avg_veh_delay_Diff_inst_phi5, \
    AVG_avg_len_queue_Diff_inst_phi5, \
        = pickle.load(file)

file.close()


import pickle
with open('queuing_data_post_process_phi5_high_limit30.pkl', 'rb') as file:
    net_dbl_park_minutes_df_inst_FCFS, \
    total_veh_delay_inst_FCFS, \
    total_veh_delay_error_inst_FCFS, \
    queue_duration_inst_FCFS, \
    t_queue_remove_inst_FCFS, \
    veh_in_queue_inst_FCFS, \
    avg_veh_in_queue_inst_FCFS, \
    max_veh_in_queue_inst_FCFS, \
    avg_veh_delay_inst_FCFS, \
    avg_len_queue_inst_FCFS, \
    net_dbl_park_minutes_df_inst_phi5, \
    total_veh_delay_inst_phi5, \
    total_veh_delay_error_inst_phi5, \
    queue_duration_inst_phi5, \
    t_queue_remove_inst_phi5, \
    veh_in_queue_inst_phi5, \
    avg_veh_in_queue_inst_FCFS, \
    max_veh_in_queue_inst_phi5, \
    avg_veh_delay_inst_phi5, \
    avg_len_queue_inst_phi5, \
    net_dbl_park_minutes_Diff_df_inst_phi5, \
    total_veh_delay_Diff_inst_phi5, \
    total_veh_delay_error_Diff_inst_phi5, \
    queue_duration_Diff_inst_phi5, \
    t_queue_remove_Diff_inst_phi5, \
    avg_veh_in_queue_Diff_inst_phi5, \
    max_veh_in_queue_Diff_inst_phi5, \
    avg_veh_delay_Diff_inst_phi5, \
    avg_len_queue_Diff_inst_phi5, \
    AVG_net_dbl_park_minutes_Diff_df_inst_phi5, \
    AVG_total_veh_delay_Diff_inst_phi5, \
    AVG_total_veh_delay_error_Diff_inst_phi5, \
    AVG_queue_duration_Diff_inst_phi5, \
    AVG_t_queue_remove_Diff_inst_phi5, \
    AVG_avg_veh_in_queue_Diff_inst_phi5, \
    AVG_max_veh_in_queue_Diff_inst_phi5, \
    AVG_avg_veh_delay_Diff_inst_phi5, \
    AVG_avg_len_queue_Diff_inst_phi5, \
        = pickle.load(file)

file.close()


#phi5 data from medium scenario
with open('queuing_data_post_process_phi5_med.pkl', 'rb') as file:
    net_dbl_park_minutes_df_inst_FCFS, \
    total_veh_delay_inst_FCFS, \
    total_veh_delay_error_inst_FCFS, \
    queue_duration_inst_FCFS, \
    t_queue_remove_inst_FCFS, \
    veh_in_queue_inst_FCFS, \
    avg_veh_delay_inst_FCFS, \
    avg_len_queue_inst_FCFS, \
    net_dbl_park_minutes_df_inst_phi5, \
    total_veh_delay_inst_phi5, \
    total_veh_delay_error_inst_phi5, \
    queue_duration_inst_phi5, \
    t_queue_remove_inst_phi5, \
    veh_in_queue_inst_phi5, \
    avg_veh_delay_inst_phi5, \
    avg_len_queue_inst_phi5, \
    net_dbl_park_minutes_Diff_df_inst_phi5, \
    total_veh_delay_Diff_inst_phi5, \
    total_veh_delay_error_Diff_inst_phi5, \
    queue_duration_Diff_inst_phi5, \
    t_queue_remove_Diff_inst_phi5, \
    veh_in_queue_Diff_inst_phi5, \
    avg_veh_delay_Diff_inst_phi5, \
    avg_len_queue_Diff_inst_phi5, \
    AVG_net_dbl_park_minutes_Diff_df_inst_phi5, \
    AVG_total_veh_delay_Diff_inst_phi5, \
    AVG_total_veh_delay_error_Diff_inst_phi5, \
    AVG_queue_duration_Diff_inst_phi5, \
    AVG_t_queue_remove_Diff_inst_phi5, \
    AVG_veh_in_queue_Diff_inst_phi5, \
    AVG_avg_veh_delay_Diff_inst_phi5, \
    AVG_avg_len_queue_Diff_inst_phi5 \
        = pickle.load(file)
        
file.close()

#phi5 data from high scenario
with open('queuing_data_post_process_phi5_high.pkl', 'rb') as file:
    net_dbl_park_minutes_df_inst_FCFS, \
    total_veh_delay_inst_FCFS, \
    total_veh_delay_error_inst_FCFS, \
    queue_duration_inst_FCFS, \
    t_queue_remove_inst_FCFS, \
    veh_in_queue_inst_FCFS, \
    avg_veh_delay_inst_FCFS, \
    avg_len_queue_inst_FCFS, \
    net_dbl_park_minutes_df_inst_phi5, \
    total_veh_delay_inst_phi5, \
    total_veh_delay_error_inst_phi5, \
    queue_duration_inst_phi5, \
    t_queue_remove_inst_phi5, \
    veh_in_queue_inst_phi5, \
    avg_veh_delay_inst_phi5, \
    avg_len_queue_inst_phi5, \
    net_dbl_park_minutes_Diff_df_inst_phi5, \
    total_veh_delay_Diff_inst_phi5, \
    total_veh_delay_error_Diff_inst_phi5, \
    queue_duration_Diff_inst_phi5, \
    t_queue_remove_Diff_inst_phi5, \
    veh_in_queue_Diff_inst_phi5, \
    avg_veh_delay_Diff_inst_phi5, \
    avg_len_queue_Diff_inst_phi5, \
    AVG_net_dbl_park_minutes_Diff_df_inst_phi5, \
    AVG_total_veh_delay_Diff_inst_phi5, \
    AVG_total_veh_delay_error_Diff_inst_phi5, \
    AVG_queue_duration_Diff_inst_phi5, \
    AVG_t_queue_remove_Diff_inst_phi5, \
    AVG_veh_in_queue_Diff_inst_phi5, \
    AVG_avg_veh_delay_Diff_inst_phi5, \
    AVG_avg_len_queue_Diff_inst_phi5 \
        = pickle.load(file)
        
file.close()


#this is actually phi5_low_limit_30, until we rerun it, has been rerun on 23 Dec 2021
import pickle
with open('queuing_data_post_process_phi15_low_limit30.pkl', 'rb') as file:
    net_dbl_park_minutes_df_inst_FCFS, \
    total_veh_delay_inst_FCFS, \
    total_veh_delay_error_inst_FCFS, \
    queue_duration_inst_FCFS, \
    t_queue_remove_inst_FCFS, \
    veh_in_queue_inst_FCFS, \
    avg_veh_in_queue_inst_FCFS, \
    max_veh_in_queue_inst_FCFS, \
    avg_veh_delay_inst_FCFS, \
    avg_len_queue_inst_FCFS, \
    net_dbl_park_minutes_df_inst_phi15, \
    total_veh_delay_inst_phi15, \
    total_veh_delay_error_inst_phi15, \
    queue_duration_inst_phi15, \
    t_queue_remove_inst_phi15, \
    veh_in_queue_inst_phi15, \
    avg_veh_in_queue_inst_FCFS, \
    max_veh_in_queue_inst_phi15, \
    avg_veh_delay_inst_phi15, \
    avg_len_queue_inst_phi15, \
    net_dbl_park_minutes_Diff_df_inst_phi15, \
    total_veh_delay_Diff_inst_phi15, \
    total_veh_delay_error_Diff_inst_phi15, \
    queue_duration_Diff_inst_phi15, \
    t_queue_remove_Diff_inst_phi15, \
    avg_veh_in_queue_Diff_inst_phi15, \
    max_veh_in_queue_Diff_inst_phi15, \
    avg_veh_delay_Diff_inst_phi15, \
    avg_len_queue_Diff_inst_phi15, \
    AVG_net_dbl_park_minutes_Diff_df_inst_phi15, \
    AVG_total_veh_delay_Diff_inst_phi15, \
    AVG_total_veh_delay_error_Diff_inst_phi15, \
    AVG_queue_duration_Diff_inst_phi15, \
    AVG_t_queue_remove_Diff_inst_phi15, \
    AVG_avg_veh_in_queue_Diff_inst_phi15, \
    AVG_max_veh_in_queue_Diff_inst_phi15, \
    AVG_avg_veh_delay_Diff_inst_phi15, \
    AVG_avg_len_queue_Diff_inst_phi15, \
        = pickle.load(file)

file.close()


import pickle
with open('queuing_data_post_process_phi15_med_limit30.pkl', 'rb') as file:
    net_dbl_park_minutes_df_inst_FCFS, \
    total_veh_delay_inst_FCFS, \
    total_veh_delay_error_inst_FCFS, \
    queue_duration_inst_FCFS, \
    t_queue_remove_inst_FCFS, \
    veh_in_queue_inst_FCFS, \
    avg_veh_in_queue_inst_FCFS, \
    max_veh_in_queue_inst_FCFS, \
    avg_veh_delay_inst_FCFS, \
    avg_len_queue_inst_FCFS, \
    net_dbl_park_minutes_df_inst_phi15, \
    total_veh_delay_inst_phi15, \
    total_veh_delay_error_inst_phi15, \
    queue_duration_inst_phi15, \
    t_queue_remove_inst_phi15, \
    veh_in_queue_inst_phi15, \
    avg_veh_in_queue_inst_FCFS, \
    max_veh_in_queue_inst_phi15, \
    avg_veh_delay_inst_phi15, \
    avg_len_queue_inst_phi15, \
    net_dbl_park_minutes_Diff_df_inst_phi15, \
    total_veh_delay_Diff_inst_phi15, \
    total_veh_delay_error_Diff_inst_phi15, \
    queue_duration_Diff_inst_phi15, \
    t_queue_remove_Diff_inst_phi15, \
    avg_veh_in_queue_Diff_inst_phi15, \
    max_veh_in_queue_Diff_inst_phi15, \
    avg_veh_delay_Diff_inst_phi15, \
    avg_len_queue_Diff_inst_phi15, \
    AVG_net_dbl_park_minutes_Diff_df_inst_phi15, \
    AVG_total_veh_delay_Diff_inst_phi15, \
    AVG_total_veh_delay_error_Diff_inst_phi15, \
    AVG_queue_duration_Diff_inst_phi15, \
    AVG_t_queue_remove_Diff_inst_phi15, \
    AVG_avg_veh_in_queue_Diff_inst_phi15, \
    AVG_max_veh_in_queue_Diff_inst_phi15, \
    AVG_avg_veh_delay_Diff_inst_phi15, \
    AVG_avg_len_queue_Diff_inst_phi15, \
        = pickle.load(file)

file.close()


import pickle
with open('queuing_data_post_process_phi15_high_limit30.pkl', 'rb') as file:
    net_dbl_park_minutes_df_inst_FCFS, \
    total_veh_delay_inst_FCFS, \
    total_veh_delay_error_inst_FCFS, \
    queue_duration_inst_FCFS, \
    t_queue_remove_inst_FCFS, \
    veh_in_queue_inst_FCFS, \
    avg_veh_in_queue_inst_FCFS, \
    max_veh_in_queue_inst_FCFS, \
    avg_veh_delay_inst_FCFS, \
    avg_len_queue_inst_FCFS, \
    net_dbl_park_minutes_df_inst_phi15, \
    total_veh_delay_inst_phi15, \
    total_veh_delay_error_inst_phi15, \
    queue_duration_inst_phi15, \
    t_queue_remove_inst_phi15, \
    veh_in_queue_inst_phi15, \
    avg_veh_in_queue_inst_FCFS, \
    max_veh_in_queue_inst_phi15, \
    avg_veh_delay_inst_phi15, \
    avg_len_queue_inst_phi15, \
    net_dbl_park_minutes_Diff_df_inst_phi15, \
    total_veh_delay_Diff_inst_phi15, \
    total_veh_delay_error_Diff_inst_phi15, \
    queue_duration_Diff_inst_phi15, \
    t_queue_remove_Diff_inst_phi15, \
    avg_veh_in_queue_Diff_inst_phi15, \
    max_veh_in_queue_Diff_inst_phi15, \
    avg_veh_delay_Diff_inst_phi15, \
    avg_len_queue_Diff_inst_phi15, \
    AVG_net_dbl_park_minutes_Diff_df_inst_phi15, \
    AVG_total_veh_delay_Diff_inst_phi15, \
    AVG_total_veh_delay_error_Diff_inst_phi15, \
    AVG_queue_duration_Diff_inst_phi15, \
    AVG_t_queue_remove_Diff_inst_phi15, \
    AVG_avg_veh_in_queue_Diff_inst_phi15, \
    AVG_max_veh_in_queue_Diff_inst_phi15, \
    AVG_avg_veh_delay_Diff_inst_phi15, \
    AVG_avg_len_queue_Diff_inst_phi15, \
        = pickle.load(file)

file.close()


#phi30 data from medium scenario
with open('queuing_data_post_process_phi30_med.pkl', 'rb') as file:
    net_dbl_park_minutes_df_inst_FCFS, \
    total_veh_delay_inst_FCFS, \
    total_veh_delay_error_inst_FCFS, \
    queue_duration_inst_FCFS, \
    t_queue_remove_inst_FCFS, \
    veh_in_queue_inst_FCFS, \
    avg_veh_delay_inst_FCFS, \
    avg_len_queue_inst_FCFS, \
    net_dbl_park_minutes_df_inst_phi30, \
    total_veh_delay_inst_phi30, \
    total_veh_delay_error_inst_phi30, \
    queue_duration_inst_phi30, \
    t_queue_remove_inst_phi30, \
    veh_in_queue_inst_phi30, \
    avg_veh_delay_inst_phi30, \
    avg_len_queue_inst_phi30, \
    net_dbl_park_minutes_Diff_df_inst_phi30, \
    total_veh_delay_Diff_inst_phi30, \
    total_veh_delay_error_Diff_inst_phi30, \
    queue_duration_Diff_inst_phi30, \
    t_queue_remove_Diff_inst_phi30, \
    veh_in_queue_Diff_inst_phi30, \
    avg_veh_delay_Diff_inst_phi30, \
    avg_len_queue_Diff_inst_phi30, \
    AVG_net_dbl_park_minutes_Diff_df_inst_phi30, \
    AVG_total_veh_delay_Diff_inst_phi30, \
    AVG_total_veh_delay_error_Diff_inst_phi30, \
    AVG_queue_duration_Diff_inst_phi30, \
    AVG_t_queue_remove_Diff_inst_phi30, \
    AVG_veh_in_queue_Diff_inst_phi30, \
    AVG_avg_veh_delay_Diff_inst_phi30, \
    AVG_avg_len_queue_Diff_inst_phi30 \
        = pickle.load(file)
        
file.close()

#Number of unscheduled vehicles in FCFS and the total dbl parking minutes, across parking spaces and number of trucks (not the net dbl parking)​
#Show a comparison with phi5, probably focused on the number of unscheduled vehicles (not the net dbl parking)




#Total minutes of double parking from FCFS
dbl_park_FCFS_instance_AVG = dbl_park_FCFS_instance.applymap(lambda x: np.mean(x))
low_res_1 = []
low_res_2 = []
low_res_3 = []
low_res_4 = []
low_res_5 = []
low_res_6 = []
low_res_7 = []
for j in range(0,len(DV_scenarios)):
    low_res_1.append(dbl_park_FCFS_instance_AVG[1][DV_scenarios.loc[j][0]])
    low_res_2.append(dbl_park_FCFS_instance_AVG[2][DV_scenarios.loc[j][1]])
    low_res_3.append(dbl_park_FCFS_instance_AVG[3][DV_scenarios.loc[j][2]])
    low_res_4.append(dbl_park_FCFS_instance_AVG[4][DV_scenarios.loc[j][3]])
    low_res_5.append(dbl_park_FCFS_instance_AVG[5][DV_scenarios.loc[j][4]])
    low_res_6.append(dbl_park_FCFS_instance_AVG[6][DV_scenarios.loc[j][5]])
    low_res_7.append(dbl_park_FCFS_instance_AVG[7][DV_scenarios.loc[j][6]])

dbl_park_FCFS_instance_AVG_low_res = pd.DataFrame({ "1": low_res_1,
                                                    "2": low_res_2,
                                                    "3": low_res_3,
                                                    "4": low_res_4,
                                                    "5": low_res_5,
                                                    "6": low_res_6,
                                                    "7": low_res_7})



plt.figure()
for i in range(0,7):
    plt.plot(DV_scenarios.loc[i], dbl_park_FCFS_instance_AVG_low_res.loc[i])
plt.legend()



dbl_park_FCFS_instance_AVG_low_res = pd.DataFrame({"Trucks": truck_scenarios,
                                                    "1": low_res_1,
                                                    "2": low_res_2,
                                                    "3": low_res_3,
                                                    "4": low_res_4})

df = dbl_park_FCFS_instance_AVG_low_res
df['Trucks'] = truck_scenarios
df = df.set_index('Trucks')

plt.figure()
df.plot()
plt.title("Average Total Minutes of Unschedule Service (FCFS)")
plt.xlabel("Quantity of Delivery Vehicles")
plt.ylabel('Average Total Unscheduled Service (min)')
plt.legend(title = 'Parking Spaces', loc = 'upper left')
plt.show()


#Total number of unscheduled vehicles from FCFS
dbl_park_FCFS_cancelled_inst_AVG = dbl_park_FCFS_cancelled_inst.applymap(lambda x: np.mean(x))
low_res_1 = []
low_res_2 = []
low_res_3 = []
low_res_4 = []
for j in truck_scenarios:
    low_res_1.append(dbl_park_FCFS_cancelled_inst_AVG[1][j])
    low_res_2.append(dbl_park_FCFS_cancelled_inst_AVG[2][j])
    low_res_3.append(dbl_park_FCFS_cancelled_inst_AVG[3][j])
    low_res_4.append(dbl_park_FCFS_cancelled_inst_AVG[4][j])

dbl_park_FCFS_cancelled_inst_AVG_low_res = pd.DataFrame({"Trucks": truck_scenarios,
                                                    "1": low_res_1,
                                                    "2": low_res_2,
                                                    "3": low_res_3,
                                                    "4": low_res_4})

df = dbl_park_FCFS_cancelled_inst_AVG_low_res
df['Trucks'] = truck_scenarios
df = df.set_index('Trucks')

plt.figure()
df.plot()
plt.title("Average Unscheduled Delivery Vehicles (FCFS)")
plt.xlabel("Quantity of Delivery Vehicles")
plt.ylabel('Average Unscheduled Delivery Vehicles')
plt.legend(title = 'Parking Spaces', loc = 'upper left')
plt.show()



##############################################################################
#Average reduction in unschedule service duration, phi = 0
dbl_park_Diff_inst_phi0_AVG = dbl_park_Diff_inst_phi0.applymap(lambda x: np.mean(x))
low_res_1 = []
low_res_2 = []
low_res_3 = []
low_res_4 = []
for j in truck_scenarios:
    low_res_1.append(dbl_park_Diff_inst_phi0_AVG[1][j])
    low_res_2.append(dbl_park_Diff_inst_phi0_AVG[2][j])
    low_res_3.append(dbl_park_Diff_inst_phi0_AVG[3][j])
    low_res_4.append(dbl_park_Diff_inst_phi0_AVG[4][j])

dbl_park_Diff_inst_phi0_AVG_low_res = pd.DataFrame({"Trucks": truck_scenarios,
                                                    "1": low_res_1,
                                                    "2": low_res_2,
                                                    "3": low_res_3,
                                                    "4": low_res_4})

df = dbl_park_Diff_inst_phi0_AVG_low_res
df['Trucks'] = truck_scenarios
df = df.set_index('Trucks')

plt.figure()
df.plot()
plt.title("Avg Reduction in Double Parking Minutes (phi = 0)")
plt.xlabel("Quantity of Delivery Vehicles")
plt.ylabel('Avg Reduction in Double Parking (min)')
plt.legend(title = 'Parking Spaces', loc = 'upper left')
plt.ylim([0, 455])
plt.show()
##############################################################################

##############################################################################
#Average reduction in unschedule service duration, phi = 0 w/ CI

low_res_1 = []
low_res_2 = []
low_res_3 = []
low_res_4 = []
for j in truck_scenarios:
    low_res_1.append(dbl_park_Diff_inst_phi0[1][j])
    low_res_2.append(dbl_park_Diff_inst_phi0[2][j])
    low_res_3.append(dbl_park_Diff_inst_phi0[3][j])
    low_res_4.append(dbl_park_Diff_inst_phi0[4][j])

dbl_park_Diff_inst_phi0_low_res = pd.DataFrame({"Trucks": truck_scenarios,
                                                    "1": low_res_1,
                                                    "2": low_res_2,
                                                    "3": low_res_3,
                                                    "4": low_res_4})


#Confidence interval graphic generation
data_df = pd.DataFrame(np.empty((3280, 4), dtype = float), columns = ["Parking Spaces","Vehicles", "Inst", "Redux Dbl Park phi0"])
row = 0
for c in range(1, 5):
    if c == 1:
        for n in range(0, 41):
            for i in range(0, 20):
                data_df.iloc[row, 0] = str(c)
                data_df.iloc[row, 1] = int(truck_scenarios[n])
                data_df.iloc[row, 2] = i+1
                data_df.iloc[row, 3] = float(dbl_park_Diff_inst_phi0_low_res.iloc[n][c][i])/60
                
                #data_df.iloc[row, 4] = float(sum_service[i])
                row += 1
                #print(row)
    elif c == 2:
        for n in range(0, 41):
            for i in range(0, 20):
                data_df.iloc[row, 0] = str(c)
                data_df.iloc[row, 1] = int(truck_scenarios[n])
                data_df.iloc[row, 2] = i+1
                data_df.iloc[row, 3] = float(dbl_park_Diff_inst_phi0_low_res.iloc[n][c][i])/60
                
                #data_df.iloc[row, 4] = float(sum_service[i])
                row += 1
                #print(row)
    elif c == 3:
        for n in range(0, 41):
            for i in range(0, 20):
                data_df.iloc[row, 0] = str(c)
                data_df.iloc[row, 1] = int(truck_scenarios[n])
                data_df.iloc[row, 2] = i+1
                data_df.iloc[row, 3] = float(dbl_park_Diff_inst_phi0_low_res.iloc[n][c][i])/60
                
                #data_df.iloc[row, 4] = float(sum_service[i])
                row += 1
                #print(row)
    elif c == 4:
        for n in range(0, 41):
            for i in range(0, 20):
                data_df.iloc[row, 0] = str(c)
                data_df.iloc[row, 1] = int(truck_scenarios[n])
                data_df.iloc[row, 2] = i+1
                data_df.iloc[row, 3] = float(dbl_park_Diff_inst_phi0_low_res.iloc[n][c][i])/60
                
                
                #data_df.iloc[row, 4] = float(sum_service[i])
                row += 1
                #print(row)
   

#plot minutes of lane obstruction between uncoord and coord
plt.figure()
import seaborn as sns
import matplotlib.pyplot as plt
#fig, ax1 = plt.subplots(1,1)

sns.lineplot(data = data_df, x = "Vehicles", y = "Redux Dbl Park phi0", hue = "Parking Spaces",
              palette = "tab10", ci = 95, linestyle = 'solid', legend = 'full')

plt.suptitle("Avg Reduction in Double Parking Minutes (phi = 0)")
plt.title('95% Confidence Interval')
plt.xlabel("Quantity of Delivery Vehicles")
plt.ylabel('Avg Reduction in Double Parking (hours)')
plt.legend(title = 'Parking Spaces', loc = 'upper left', prop={'size': 8})
#plt.ylim([0, 480])
plt.ylim([0, 8.5]) #for visualising the graph in hours
plt.show()
##############################################################################


##############################################################################
#Average reduction in unschedule service duration, phi = 5
dbl_park_Diff_inst_phi5_AVG = dbl_park_Diff_inst_phi5.applymap(lambda x: np.mean(x))
low_res_1 = []
low_res_2 = []
low_res_3 = []
low_res_4 = []
for j in truck_scenarios:
    low_res_1.append(dbl_park_Diff_inst_phi5_AVG[1][j])
    low_res_2.append(dbl_park_Diff_inst_phi5_AVG[2][j])
    low_res_3.append(dbl_park_Diff_inst_phi5_AVG[3][j])
    low_res_4.append(dbl_park_Diff_inst_phi5_AVG[4][j])

dbl_park_Diff_inst_phi5_AVG_low_res = pd.DataFrame({"Trucks": truck_scenarios,
                                                    "1": low_res_1,
                                                    "2": low_res_2,
                                                    "3": low_res_3,
                                                    "4": low_res_4})

df = dbl_park_Diff_inst_phi5_AVG_low_res
df['Trucks'] = truck_scenarios
df = df.set_index('Trucks')

plt.figure()
df.plot()
plt.title("Avg Reduction in Double Parking Minutes (phi = 5)")
plt.xlabel("Quantity of Delivery Vehicles")
plt.ylabel('Avg Reduction in Double Parking (min)')
plt.legend(title = 'Parking Spaces', loc = 'upper left')
plt.ylim([0, 455])
plt.show()
##############################################################################


##############################################################################
#Average reduction in unschedule service duration, phi = 5 w/ CI

low_res_1 = []
low_res_2 = []
low_res_3 = []
low_res_4 = []
low_res_5 = []
low_res_6 = []
low_res_7 = []
for j in range(0, len(DV_scenarios)):
    low_res_1.append(dbl_park_Diff_inst_phi5[1][DV_scenarios.loc[j][0]])
    low_res_2.append(dbl_park_Diff_inst_phi5[2][DV_scenarios.loc[j][1]])
    low_res_3.append(dbl_park_Diff_inst_phi5[3][DV_scenarios.loc[j][2]])
    low_res_4.append(dbl_park_Diff_inst_phi5[4][DV_scenarios.loc[j][3]])
    low_res_5.append(dbl_park_Diff_inst_phi5[5][DV_scenarios.loc[j][4]])
    low_res_6.append(dbl_park_Diff_inst_phi5[6][DV_scenarios.loc[j][5]])
    low_res_7.append(dbl_park_Diff_inst_phi5[7][DV_scenarios.loc[j][6]])

dbl_park_Diff_inst_phi5_low_res = pd.DataFrame({
                                                    "1": low_res_1,
                                                    "2": low_res_2,
                                                    "3": low_res_3,
                                                    "4": low_res_4,
                                                    "5": low_res_5,
                                                    "6": low_res_6,
                                                    "7": low_res_7})

#convert DV_scenarios to the correct parking demand per parking space per hour
DV_scenarios_norm = DV_scenarios / 11
DV_scenarios_norm['2'] = (DV_scenarios_norm['2'] / 2)
DV_scenarios_norm['3'] = (DV_scenarios_norm['3'] / 3)
DV_scenarios_norm['4'] = (DV_scenarios_norm['4'] / 4)
DV_scenarios_norm['5'] = (DV_scenarios_norm['5'] / 5)
DV_scenarios_norm['6'] = (DV_scenarios_norm['6'] / 6)
DV_scenarios_norm['7'] = (DV_scenarios_norm['7'] / 7)

# parking_demand_scenarios = np.array([0.25, 0.5, 0.75, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6])
# DV_scenarios = pd.DataFrame({'1': (parking_demand_scenarios * 11),
#                                 '2': (parking_demand_scenarios * 11 * 2),
#                                 '3': (parking_demand_scenarios * 11 * 3),
#                                 '4': (parking_demand_scenarios * 11 * 4),
#                                 '5': (parking_demand_scenarios * 11 * 5),
#                                 '6': (parking_demand_scenarios * 11 * 6),
#                                 '7': (parking_demand_scenarios * 11 * 7),
#                                 })


#Confidence interval graphic generation #1862
data_df = pd.DataFrame(np.empty((1862, 4), dtype = float), columns = ["Parking Spaces","Vehicle Demand", "Inst", "Redux Dbl Park phi5"])
row = 0
for c in range(1, 8):
    if c == 1:
        for n in range(0, 14):
            for i in range(0, 19):
                data_df.iloc[row, 0] = str(c)
                data_df.iloc[row, 1] = np.log(DV_scenarios_norm.iloc[n][c-1])
                data_df.iloc[row, 2] = i+1
                data_df.iloc[row, 3] = float(dbl_park_Diff_inst_phi5_low_res.iloc[n][c-1][i])/11/1
                
                row += 1
                
    if c == 2:
        for n in range(0, 14):
            for i in range(0, 19):
                data_df.iloc[row, 0] = str(c)
                data_df.iloc[row, 1] = np.log(DV_scenarios_norm.iloc[n][c-1])
                data_df.iloc[row, 2] = i+1
                data_df.iloc[row, 3] = float(dbl_park_Diff_inst_phi5_low_res.iloc[n][c-1][i])/11/2
                
                row += 1
    
    if c == 3:
        for n in range(0, 14):
            for i in range(0, 19):
                data_df.iloc[row, 0] = str(c)
                data_df.iloc[row, 1] = np.log(DV_scenarios_norm.iloc[n][c-1])
                data_df.iloc[row, 2] = i+1
                data_df.iloc[row, 3] = float(dbl_park_Diff_inst_phi5_low_res.iloc[n][c-1][i])/11/3
                
                row += 1
                
    if c == 4:
        for n in range(0, 14):
            for i in range(0, 19):
                data_df.iloc[row, 0] = str(c)
                data_df.iloc[row, 1] = np.log(DV_scenarios_norm.iloc[n][c-1])
                data_df.iloc[row, 2] = i+1
                data_df.iloc[row, 3] = float(dbl_park_Diff_inst_phi5_low_res.iloc[n][c-1][i])/11/4
                
                row += 1
                
    if c == 5:
        for n in range(0, 14):
            for i in range(0, 19):
                data_df.iloc[row, 0] = str(c)
                data_df.iloc[row, 1] = np.log(DV_scenarios_norm.iloc[n][c-1])
                data_df.iloc[row, 2] = i+1
                data_df.iloc[row, 3] = float(dbl_park_Diff_inst_phi5_low_res.iloc[n][c-1][i])/11/5
                
                row += 1
                
    if c == 6:
        for n in range(0, 14):
            for i in range(0, 19):
                data_df.iloc[row, 0] = str(c)
                data_df.iloc[row, 1] = np.log(DV_scenarios_norm.iloc[n][c-1])
                data_df.iloc[row, 2] = i+1
                data_df.iloc[row, 3] = float(dbl_park_Diff_inst_phi5_low_res.iloc[n][c-1][i])/11/6
                
                row += 1
                
    if c == 7:
        for n in range(0, 14):
            for i in range(0, 19):
                data_df.iloc[row, 0] = str(c)
                data_df.iloc[row, 1] = np.log(DV_scenarios_norm.iloc[n][c-1])
                data_df.iloc[row, 2] = i+1
                data_df.iloc[row, 3] = float(dbl_park_Diff_inst_phi5_low_res.iloc[n][c-1][i])/11/7
                
                row += 1

   

#plot minutes of lane obstruction between uncoord and coord
plt.figure()
#import seaborn as sns
import matplotlib.pyplot as plt
#fig, ax1 = plt.subplots(1,1)

sns.lineplot(data = data_df, x = "Vehicle Demand", y = "Redux Dbl Park phi5", hue = "Parking Spaces",
              palette = "tab10", ci = 95, linestyle = 'solid', legend = 'full')

plt.suptitle("Avg Reduction in Double Parking (phi = 5)")
plt.title('95% Confidence Interval')
plt.xlabel("Number of Deliveries per Parking Space per Hour")
#plt.ylabel('Avg Reduction in Double Parking \n (hours per parking space per day)')
plt.ylabel('Avg Reduction in Double Parking \n (minutes per hour per parking space)')
plt.legend(title = 'Parking Spaces', loc = 'lower right', prop={'size': 8})
#plt.ylim([0, 350])
plt.show()
##############################################################################



##############################################################################
#Average reduction in unschedule service duration, phi = 5, random uniform DV scenarios

# #one option, but the legend doesn't come out correctly
# plt.figure()
# for i in range(1, max_parking_spaces +1):
#     sns.scatterplot(x = n_index_norm_lst_df[i], y = dbl_park_Diff_inst_phi5_df[i]/11/i)

# plt.suptitle('Reduction in Double Parking (phi = 5)')
# plt.xlabel('Number of Deliveries per Parking Space per Hours')
# plt.ylabel('Reduction in Double Parking \n (minutes per hour per parking space)')
# plt.legend(title = 'Parking Spaces', loc = 'lower right', prop={'size': 8})

# plt.show()





# #need to create a single dataframe for sns to work its best and have the right legend

# #organize the n_index into a column vector
# data_df = pd.DataFrame(np.empty((70, 3), dtype = float), columns = ["Parking Spaces", "Vehicle Demand Norm", "Redux Dbl Park phi5"])

# row = 0
# for c in range(1, max_parking_spaces +1):
#     for i in range(0, iterations):
#         data_df.iloc[row, 0] = str(c)
#         data_df.iloc[row, 1] = n_index_norm_lst_df.iloc[i, c-1]
#         data_df.iloc[row, 2] = dbl_park_Diff_inst_phi5_df.iloc[i, c-1]/11/c
        
#         row += 1

# plt.figure()

# sns.scatterplot(x = 'Vehicle Demand Norm', y = 'Redux Dbl Park phi5', data = data_df, hue = 'Parking Spaces', palette = "tab10")
# #sns.lineplot(x = 'Vehicle Demand Norm', y = 'Redux Dbl Park phi5', data = data_df, hue = 'Parking Spaces', palette = "tab10")
# plt.suptitle('Reduction in Double Parking (phi = 5)')
# plt.xlabel('Number of Deliveries per Parking Space per Hour')
# plt.ylabel('Reduction in Double Parking \n (minutes per hour per parking space)')
# plt.legend(title = 'Parking Spaces', loc = 'lower right', prop={'size': 8})

# #log version of the above
# data_df = pd.DataFrame(np.empty((70, 3), dtype = float), columns = ["Parking Spaces", "Vehicle Demand Norm", "Redux Dbl Park phi5"])

# row = 0
# for c in range(1, max_parking_spaces +1):
#     for i in range(0, iterations):
#         data_df.iloc[row, 0] = str(c)
#         data_df.iloc[row, 1] = n_index_norm_lst_df.iloc[i, c-1]
#         # if dbl_park_Diff_inst_phi5_df.iloc[i, c-1]/11/c < 0.0001:
#         #     data_df.iloc[row, 2] = 
#         data_df.iloc[row, 2] = np.log(dbl_park_Diff_inst_phi5_df.iloc[i, c-1]/11/c)
        
#         row += 1

# plt.figure()

# sns.scatterplot(x = 'Vehicle Demand Norm', y = 'Redux Dbl Park phi5', data = data_df, hue = 'Parking Spaces', palette = "tab10")
# plt.suptitle('Reduction in Double Parking (phi = 5)')
# plt.xlabel('Number of Deliveries per Parking Space per Hours')
# plt.ylabel('Log Reduction in Double Parking \n (minutes per hour per parking space)')
# plt.legend(title = 'Parking Spaces', loc = 'lower right', prop={'size': 8})


# #rolling average plot
# #organize the n_index into a column vector
# data_df = pd.DataFrame(np.empty((70, 3), dtype = float), columns = ["Parking Spaces", "Vehicle Demand Norm", "Redux Dbl Park phi5"])

# row = 0
# for c in range(1, max_parking_spaces +1):
#     for i in range(0, iterations):
#         data_df.iloc[row, 0] = str(c)
#         data_df.iloc[row, 1] = n_index_norm_lst_df.iloc[i, c-1]
#         data_df.iloc[row, 2] = dbl_park_Diff_inst_phi5_df.iloc[i, c-1]/11/c
        
#         row += 1

# data_df['rolling_avg'] = data_df['Redux Dbl Park phi5'].rolling(5).mean().shift(-4)

# plt.figure()

# #sns.scatterplot(x = 'Vehicle Demand Norm', y = 'Redux Dbl Park phi5', data = data_df, hue = 'Parking Spaces', palette = "tab10")
# sns.lineplot(x = 'Vehicle Demand Norm', y = 'rolling_avg', data = data_df, hue = 'Parking Spaces', palette = "tab10")
# plt.suptitle('Reduction in Double Parking (phi = 5)')
# plt.xlabel('Number of Deliveries per Parking Space per Hour')
# plt.ylabel('Reduction in Double Parking \n (minutes per hour per parking space)')
# plt.legend(title = 'Parking Spaces', loc = 'lower right', prop={'size': 8})




# #2nd attempt at the rolling average, this should be the correct method
# dbl_park_Diff_inst_phi5_df_rolling_avg = pd.DataFrame()
# rolling_avg = []
# for c in range(1, 8):
#     rolling_avg = dbl_park_Diff_inst_phi5_df[c].rolling(5).mean()
#     dbl_park_Diff_inst_phi5_df_rolling_avg[c] = rolling_avg


# data_df = pd.DataFrame(np.empty((70, 3), dtype = float), columns = ["Parking Spaces", "Vehicle Demand Norm", "Redux Dbl Park phi5 Rolling Avg"])

# row = 0
# for c in range(1, max_parking_spaces +1):
#     for i in range(0, iterations):
#         data_df.iloc[row, 0] = str(c)
#         data_df.iloc[row, 1] = n_index_norm_lst_df.iloc[i, c-1]
#         data_df.iloc[row, 2] = dbl_park_Diff_inst_phi5_df_rolling_avg.iloc[i, c-1]/11/c
        
#         row += 1


# plt.figure()

# #sns.scatterplot(x = 'Vehicle Demand Norm', y = 'Redux Dbl Park phi5', data = data_df, hue = 'Parking Spaces', palette = "tab10")
# sns.lineplot(x = 'Vehicle Demand Norm', y = 'Redux Dbl Park phi5 Rolling Avg', data = data_df, hue = 'Parking Spaces', palette = "tab10")
# plt.suptitle('Reduction in Double Parking (phi = 5)')
# plt.title('Rolling Average (5 samples)')
# plt.xlabel('Number of Deliveries per Parking Space per Hour')
# plt.ylabel('Reduction in Double Parking \n (minutes per hour per parking space)')
# plt.legend(title = 'Parking Spaces', loc = 'lower right', prop={'size': 8})



# #3rd attempt at the rolling average, trying to capture the points around the data
# #point of interest, not just the 5 pervious
# dbl_park_Diff_inst_phi5_df_rolling_avg = pd.DataFrame()
# rolling_avg = []
# for c in range(1, 8):
#     rolling_avg = dbl_park_Diff_inst_phi5_df[c].rolling(61).mean().shift(-30)
#     dbl_park_Diff_inst_phi5_df_rolling_avg[c] = rolling_avg


# data_df = pd.DataFrame(np.empty((700, 3), dtype = float), columns = ["Parking Spaces", "Vehicle Demand Norm", "Redux Dbl Park phi5 Rolling Avg"])

# row = 0
# #for c in range(1, max_parking_spaces +1):
# c_list = [1, 2, 3, 4, 5, 6, 7]
# #c_list = [1, 4, 7]
# for c in c_list:
#     for i in range(0, iterations):
#         data_df.iloc[row, 0] = str(c)
#         data_df.iloc[row, 1] = n_index_norm_lst_df.iloc[i, c-1]
#         data_df.iloc[row, 2] = dbl_park_Diff_inst_phi5_df_rolling_avg.iloc[i, c-1]/11/c
        
#         row += 1


# plt.figure()

# #sns.scatterplot(x = 'Vehicle Demand Norm', y = 'Redux Dbl Park phi5', data = data_df, hue = 'Parking Spaces', palette = "tab10")
# sns.lineplot(x = 'Vehicle Demand Norm', y = 'Redux Dbl Park phi5 Rolling Avg', data = data_df, hue = 'Parking Spaces', palette = "tab10", ci = None)
# plt.suptitle('Reduction in Double Parking (phi = 5)')
# plt.title('Rolling Average (61 samples)')
# plt.xlabel('Number of Deliveries per Parking Space per Hour')
# plt.ylabel('Reduction in Double Parking \n (minutes per hour per parking space)')
# plt.ylim([0, 9])
# plt.legend(title = 'Parking Spaces', loc = 'lower right', prop={'size': 8})








##############################################################################
#Average reduction in unschedule service duration, phi = 15
dbl_park_Diff_inst_phi15_AVG = dbl_park_Diff_inst_phi15.applymap(lambda x: np.mean(x))
low_res_1 = []
low_res_2 = []
low_res_3 = []
low_res_4 = []
for j in truck_scenarios:
    low_res_1.append(dbl_park_Diff_inst_phi15_AVG[1][j])
    low_res_2.append(dbl_park_Diff_inst_phi15_AVG[2][j])
    low_res_3.append(dbl_park_Diff_inst_phi15_AVG[3][j])
    low_res_4.append(dbl_park_Diff_inst_phi15_AVG[4][j])

dbl_park_Diff_inst_phi15_AVG_low_res = pd.DataFrame({"Trucks": truck_scenarios,
                                                    "1": low_res_1,
                                                    "2": low_res_2,
                                                    "3": low_res_3,
                                                    "4": low_res_4})

df = dbl_park_Diff_inst_phi15_AVG_low_res
df['Trucks'] = truck_scenarios
df = df.set_index('Trucks')

plt.figure()
df.plot()
plt.title("Avg Reduction in Double Parking Minutes (phi = 15)")
plt.xlabel("Quantity of Delivery Vehicles")
plt.ylabel('Avg Reduction in Double Parking (min)')
plt.legend(title = 'Parking Spaces', loc = 'lower right')
plt.ylim([0, 455])
plt.show()
##############################################################################


##############################################################################
#Average reduction in unschedule service duration, phi = 15 w/ CI

low_res_1 = []
low_res_2 = []
low_res_3 = []
low_res_4 = []
for j in truck_scenarios:
    low_res_1.append(dbl_park_Diff_inst_phi15[1][j])
    low_res_2.append(dbl_park_Diff_inst_phi15[2][j])
    low_res_3.append(dbl_park_Diff_inst_phi15[3][j])
    low_res_4.append(dbl_park_Diff_inst_phi15[4][j])

dbl_park_Diff_inst_phi15_low_res = pd.DataFrame({"Trucks": truck_scenarios,
                                                    "1": low_res_1,
                                                    "2": low_res_2,
                                                    "3": low_res_3,
                                                    "4": low_res_4})


#Confidence interval graphic generation
data_df = pd.DataFrame(np.empty((3280, 4), dtype = float), columns = ["Parking Spaces","Vehicles", "Inst", "Redux Dbl Park phi15"])
row = 0
for c in range(1, 5):
    if c == 1:
        for n in range(0, 41):
            for i in range(0, 20):
                data_df.iloc[row, 0] = str(c)
                data_df.iloc[row, 1] = int(truck_scenarios[n])
                data_df.iloc[row, 2] = i+1
                data_df.iloc[row, 3] = float(dbl_park_Diff_inst_phi15_low_res.iloc[n][c][i])/60
                
                #data_df.iloc[row, 4] = float(sum_service[i])
                row += 1
                #print(row)
    elif c == 2:
        for n in range(0, 41):
            for i in range(0, 20):
                data_df.iloc[row, 0] = str(c)
                data_df.iloc[row, 1] = int(truck_scenarios[n])
                data_df.iloc[row, 2] = i+1
                data_df.iloc[row, 3] = float(dbl_park_Diff_inst_phi15_low_res.iloc[n][c][i])/60
                
                #data_df.iloc[row, 4] = float(sum_service[i])
                row += 1
                #print(row)
    elif c == 3:
        for n in range(0, 41):
            for i in range(0, 20):
                data_df.iloc[row, 0] = str(c)
                data_df.iloc[row, 1] = int(truck_scenarios[n])
                data_df.iloc[row, 2] = i+1
                data_df.iloc[row, 3] = float(dbl_park_Diff_inst_phi15_low_res.iloc[n][c][i])/60
                
                #data_df.iloc[row, 4] = float(sum_service[i])
                row += 1
                #print(row)
    elif c == 4:
        for n in range(0, 41):
            for i in range(0, 20):
                data_df.iloc[row, 0] = str(c)
                data_df.iloc[row, 1] = int(truck_scenarios[n])
                data_df.iloc[row, 2] = i+1
                data_df.iloc[row, 3] = float(dbl_park_Diff_inst_phi15_low_res.iloc[n][c][i])/60
                
                
                #data_df.iloc[row, 4] = float(sum_service[i])
                row += 1
                #print(row)
   

#plot minutes of lane obstruction between uncoord and coord
plt.figure()
import seaborn as sns
import matplotlib.pyplot as plt
#fig, ax1 = plt.subplots(1,1)

sns.lineplot(data = data_df, x = "Vehicles", y = "Redux Dbl Park phi15", hue = "Parking Spaces",
              palette = "tab10", ci = 95, linestyle = 'solid', legend = 'full')

plt.suptitle("Avg Reduction in Double Parking Minutes (phi = 15)")
plt.title('95% Confidence Interval')
plt.xlabel("Quantity of Delivery Vehicles")
plt.ylabel('Avg Reduction in Double Parking (hours)')
plt.legend(title = 'Parking Spaces', loc = 'lower right', prop={'size': 8})
#plt.ylim([0, 480])
plt.ylim([0, 8.5])
plt.show()
##############################################################################







#plot the avg reduction phi0 normalized by the number of trucks
dbl_park_Diff_inst_phi0_AVG_low_res_norm_trucks = pd.DataFrame(index = range(0, 41), columns = range(max_parking_spaces +1), dtype = object).applymap(lambda x: [])

for c in range(1, max_parking_spaces +1):
    for n in range(0, len(truck_scenarios)):
        dbl_park_Diff_inst_phi0_AVG_low_res_norm_trucks.iloc[n][c] = \
            dbl_park_Diff_inst_phi0_AVG_low_res.iloc[n][c] / dbl_park_Diff_inst_phi0_AVG_low_res['Trucks'][n]

df = dbl_park_Diff_inst_phi0_AVG_low_res_norm_trucks
df['Trucks'] = truck_scenarios
df = df.set_index('Trucks')

plt.figure()
df.plot()
plt.suptitle("Avg Reduction in Unscheduled Service (phi = 0)")
plt.title("Normalized by Trucks")
plt.xlabel("Quantity of Delivery Vehicles")
plt.ylabel('Avg Reduction in Unscheduled Service / Truck')
plt.legend(title = 'Parking Spaces', loc = 'upper left')
plt.ylim([0, 4])
plt.show()





##############################################################################
#plot the avg reduction phi5 normalized by the number of trucks
dbl_park_Diff_inst_phi5_AVG_low_res_norm_trucks = pd.DataFrame(index = range(0, 41), columns = range(max_parking_spaces +1), dtype = object).applymap(lambda x: [])

for c in range(1, max_parking_spaces +1):
    for n in range(0, len(truck_scenarios)):
        dbl_park_Diff_inst_phi5_AVG_low_res_norm_trucks.iloc[n][c] = \
            dbl_park_Diff_inst_phi5_AVG_low_res.iloc[n][c] / dbl_park_Diff_inst_phi5_AVG_low_res['Trucks'][n]

df = dbl_park_Diff_inst_phi5_AVG_low_res_norm_trucks
df['Trucks'] = truck_scenarios
df = df.set_index('Trucks')

plt.figure()
df.plot()
plt.suptitle("Avg Reduction in Unscheduled Service (phi = 5)")
plt.title("Normalized by Trucks")
plt.xlabel("Quantity of Delivery Vehicles")
plt.ylabel('Avg Reduction in Unscheduled Service / Truck')
plt.legend(title = 'Parking Spaces', loc = 'upper right')
plt.ylim([0, 4.2])
plt.show()
##############################################################################


##############################################################################
#plot the avg reduction phi15 normalized by the number of trucks
dbl_park_Diff_inst_phi15_AVG_low_res_norm_trucks = pd.DataFrame(index = range(0, 41), columns = range(max_parking_spaces +1), dtype = object).applymap(lambda x: [])

for c in range(1, max_parking_spaces +1):
    for n in range(0, len(truck_scenarios)):
        dbl_park_Diff_inst_phi15_AVG_low_res_norm_trucks.iloc[n][c] = \
            dbl_park_Diff_inst_phi15_AVG_low_res.iloc[n][c] / dbl_park_Diff_inst_phi15_AVG_low_res['Trucks'][n]

df = dbl_park_Diff_inst_phi15_AVG_low_res_norm_trucks
df['Trucks'] = truck_scenarios
df = df.set_index('Trucks')

plt.figure()
df.plot()
plt.suptitle("Avg Reduction in Double Parking Minutes (phi = 15)")
plt.title("Normalized by Delivery Vehicles")
plt.xlabel("Quantity of Delivery Vehicles")
plt.ylabel('Avg Reduction in Dbl Parking (min) / vehicle')
plt.legend(title = 'Parking Spaces', loc = 'upper right')
#plt.ylim([0, 4.2])
plt.show()
##############################################################################


##############################################################################
#plot the avg reduction phi15 normalized by the number of trucks w/ CI

low_res_1 = []
low_res_2 = []
low_res_3 = []
low_res_4 = []
for j in truck_scenarios:
    low_res_1.append(dbl_park_Diff_inst_phi15[1][j])
    low_res_2.append(dbl_park_Diff_inst_phi15[2][j])
    low_res_3.append(dbl_park_Diff_inst_phi15[3][j])
    low_res_4.append(dbl_park_Diff_inst_phi15[4][j])

dbl_park_Diff_inst_phi15_low_res = pd.DataFrame({"Trucks": truck_scenarios,
                                                    "1": low_res_1,
                                                    "2": low_res_2,
                                                    "3": low_res_3,
                                                    "4": low_res_4})


#Confidence interval graphic generation
data_df = pd.DataFrame(np.empty((3280, 4), dtype = float), columns = ["Parking Spaces","Vehicles", "Inst", "Redux Dbl Park phi15 norm trucks"])
row = 0
for c in range(1, 5):
    if c == 1:
        for n in range(0, 41):
            for i in range(0, 20):
                data_df.iloc[row, 0] = str(c)
                data_df.iloc[row, 1] = int(truck_scenarios[n])
                data_df.iloc[row, 2] = i+1
                data_df.iloc[row, 3] = float(dbl_park_Diff_inst_phi15_low_res.iloc[n][c][i] / dbl_park_Diff_inst_phi15_low_res['Trucks'][n])
                
                #data_df.iloc[row, 4] = float(sum_service[i])
                row += 1
                #print(row)
    elif c == 2:
        for n in range(0, 41):
            for i in range(0, 20):
                data_df.iloc[row, 0] = str(c)
                data_df.iloc[row, 1] = int(truck_scenarios[n])
                data_df.iloc[row, 2] = i+1
                data_df.iloc[row, 3] = float(dbl_park_Diff_inst_phi15_low_res.iloc[n][c][i] / dbl_park_Diff_inst_phi15_low_res['Trucks'][n])
                
                #data_df.iloc[row, 4] = float(sum_service[i])
                row += 1
                #print(row)
    elif c == 3:
        for n in range(0, 41):
            for i in range(0, 20):
                data_df.iloc[row, 0] = str(c)
                data_df.iloc[row, 1] = int(truck_scenarios[n])
                data_df.iloc[row, 2] = i+1
                data_df.iloc[row, 3] = float(dbl_park_Diff_inst_phi15_low_res.iloc[n][c][i] / dbl_park_Diff_inst_phi15_low_res['Trucks'][n])
                
                #data_df.iloc[row, 4] = float(sum_service[i])
                row += 1
                #print(row)
    elif c == 4:
        for n in range(0, 41):
            for i in range(0, 20):
                data_df.iloc[row, 0] = str(c)
                data_df.iloc[row, 1] = int(truck_scenarios[n])
                data_df.iloc[row, 2] = i+1
                data_df.iloc[row, 3] = float(dbl_park_Diff_inst_phi15_low_res.iloc[n][c][i] / dbl_park_Diff_inst_phi15_low_res['Trucks'][n])
                
                
                #data_df.iloc[row, 4] = float(sum_service[i])
                row += 1
                #print(row)
   

#plot minutes of lane obstruction between uncoord and coord
plt.figure()
import seaborn as sns
import matplotlib.pyplot as plt
#fig, ax1 = plt.subplots(1,1)

sns.lineplot(data = data_df, x = "Vehicles", y = "Redux Dbl Park phi15 norm trucks", hue = "Parking Spaces",
              palette = "tab10", ci = 95, linestyle = 'solid', legend = 'full')

plt.suptitle("Avg and 95% CI Reduction in Dbl Parking Minutes (phi = 15)")
plt.title('Normalized by Delivery Vehicles')
plt.xlabel("Quantity of Delivery Vehicles")
plt.ylabel('Avg Reduction in Double Parking / vehicle (min)')
plt.legend(title = 'Parking Spaces', loc = 'upper right')

plt.show()
##############################################################################








##############################################################################
#plot the avg reduction phi5 normalized by the minutes of FCFS double parking
dbl_park_Diff_inst_phi5_AVG_low_res_norm_FCFS = pd.DataFrame(index = range(0, 41), columns = ['Trucks', 1, 2, 3, 4], dtype = object).applymap(lambda x: [])

for c in range(1, max_parking_spaces +1):
    
    n = 0
    
    for N in truck_scenarios:
        
        for i in range(0, iterations):
            
            if dbl_park_FCFS_instance[c][N][i] == 0:
                dbl_park_Diff_inst_phi5_AVG_low_res_norm_FCFS.iloc[n][c].append(0)
            
            else:
                dbl_park_Diff_inst_phi5_AVG_low_res_norm_FCFS.iloc[n][c].append( \
                    (dbl_park_Diff_inst_phi5[c][N][i] / dbl_park_FCFS_instance[c][N][i])*100)

        n += 1

df = dbl_park_Diff_inst_phi5_AVG_low_res_norm_FCFS
df = df.applymap(lambda x: np.mean(x))
df['Trucks'] = truck_scenarios
df = df.set_index('Trucks')
plt.figure()
df.plot()
plt.title("Avg % of Reduction in Dbl Parking Min to Uncoordinated Min Dbl Parking (phi = 5)")
plt.ylabel("% Reduction in Dbl Parking (minutes)")
plt.xlabel('Avg Vehicles in Queue')
plt.ylim(0,75)
plt.legend(title = 'Parking Spaces', loc = 'upper right')
plt.show()
##############################################################################


##############################################################################
#plot the avg reduction phi15 normalized by the minutes of FCFS double parking
dbl_park_Diff_inst_phi15_AVG_low_res_norm_FCFS = pd.DataFrame(index = range(0, 41), columns = ['Trucks', 1, 2, 3, 4], dtype = object).applymap(lambda x: [])

for c in range(1, max_parking_spaces +1):
    
    n = 0
    
    for N in truck_scenarios:
        
        for i in range(0, iterations):
            
            if dbl_park_FCFS_instance[c][N][i] == 0:
                dbl_park_Diff_inst_phi15_AVG_low_res_norm_FCFS.iloc[n][c].append(0)
            
            else:
                dbl_park_Diff_inst_phi15_AVG_low_res_norm_FCFS.iloc[n][c].append( \
                    (dbl_park_Diff_inst_phi15[c][N][i] / dbl_park_FCFS_instance[c][N][i])*100)

        n += 1

df = dbl_park_Diff_inst_phi15_AVG_low_res_norm_FCFS
df = df.applymap(lambda x: np.mean(x))
df['Trucks'] = truck_scenarios
df = df.set_index('Trucks')
plt.figure()
df.plot()
plt.title("Avg % of Reduction in Dbl Parking Min to Uncoordinated Min Dbl Parking (phi = 15)")
plt.ylabel("% Reduction in Dbl Parking (minutes)")
plt.xlabel('Avg Vehicles in Queue')
#plt.ylim(0,75)
plt.legend(title = 'Parking Spaces', loc = 'upper right')
plt.show()
##############################################################################



##############################################################################
#plot the avg reduction phi15 normalized by the minutes of FCFS double parking

low_res_1 = []
low_res_2 = []
low_res_3 = []
low_res_4 = []
for j in truck_scenarios:
    low_res_1.append(dbl_park_FCFS_instance[1][j])
    low_res_2.append(dbl_park_FCFS_instance[2][j])
    low_res_3.append(dbl_park_FCFS_instance[3][j])
    low_res_4.append(dbl_park_FCFS_instance[4][j])

dbl_park_FCFS_instance_low_res = pd.DataFrame({"Trucks": truck_scenarios,
                                                    "1": low_res_1,
                                                    "2": low_res_2,
                                                    "3": low_res_3,
                                                    "4": low_res_4})

low_res_1 = []
low_res_2 = []
low_res_3 = []
low_res_4 = []
for j in truck_scenarios:
    low_res_1.append(dbl_park_Diff_inst_phi15[1][j])
    low_res_2.append(dbl_park_Diff_inst_phi15[2][j])
    low_res_3.append(dbl_park_Diff_inst_phi15[3][j])
    low_res_4.append(dbl_park_Diff_inst_phi15[4][j])

dbl_park_Diff_inst_phi15_low_res = pd.DataFrame({"Trucks": truck_scenarios,
                                                    "1": low_res_1,
                                                    "2": low_res_2,
                                                    "3": low_res_3,
                                                    "4": low_res_4})


#Confidence interval graphic generation
data_df = pd.DataFrame(np.empty((3280, 4), dtype = float), columns = ["Parking Spaces","Vehicles", "Inst", "Redux Dbl Park phi15 norm FCFS"])
row = 0
for c in range(1, 5):
    if c == 1:
        for n in range(0, 41):
            for i in range(0, 20):
                data_df.iloc[row, 0] = str(c)
                data_df.iloc[row, 1] = int(truck_scenarios[n])
                data_df.iloc[row, 2] = i+1
                
                if dbl_park_FCFS_instance_low_res.iloc[n][c][i] == 0:
                    data_df.iloc[row, 3] = 0
                else:
                    data_df.iloc[row, 3] = float(dbl_park_Diff_inst_phi15_low_res.iloc[n][c][i] / dbl_park_FCFS_instance_low_res.iloc[n][c][i])*100
                
                #data_df.iloc[row, 4] = float(sum_service[i])
                row += 1
                #print(row)
    elif c == 2:
        for n in range(0, 41):
            for i in range(0, 20):
                data_df.iloc[row, 0] = str(c)
                data_df.iloc[row, 1] = int(truck_scenarios[n])
                data_df.iloc[row, 2] = i+1
                
                if dbl_park_FCFS_instance_low_res.iloc[n][c][i] == 0:
                    data_df.iloc[row, 3] = 0
                else:
                    data_df.iloc[row, 3] = float(dbl_park_Diff_inst_phi15_low_res.iloc[n][c][i] / dbl_park_FCFS_instance_low_res.iloc[n][c][i])*100
                
                #data_df.iloc[row, 4] = float(sum_service[i])
                row += 1
                #print(row)
    elif c == 3:
        for n in range(0, 41):
            for i in range(0, 20):
                data_df.iloc[row, 0] = str(c)
                data_df.iloc[row, 1] = int(truck_scenarios[n])
                data_df.iloc[row, 2] = i+1
                
                if dbl_park_FCFS_instance_low_res.iloc[n][c][i] == 0:
                    data_df.iloc[row, 3] = 0
                else:
                    data_df.iloc[row, 3] = float(dbl_park_Diff_inst_phi15_low_res.iloc[n][c][i] / dbl_park_FCFS_instance_low_res.iloc[n][c][i])*100
                
                
                #data_df.iloc[row, 4] = float(sum_service[i])
                row += 1
                #print(row)
    elif c == 4:
        for n in range(0, 41):
            for i in range(0, 20):
                data_df.iloc[row, 0] = str(c)
                data_df.iloc[row, 1] = int(truck_scenarios[n])
                data_df.iloc[row, 2] = i+1
                
                if dbl_park_FCFS_instance_low_res.iloc[n][c][i] == 0:
                    data_df.iloc[row, 3] = 0
                else:
                    data_df.iloc[row, 3] = float(dbl_park_Diff_inst_phi15_low_res.iloc[n][c][i] / dbl_park_FCFS_instance_low_res.iloc[n][c][i])*100
                
                
                
                #data_df.iloc[row, 4] = float(sum_service[i])
                row += 1
                #print(row)
   

#plot minutes of lane obstruction between uncoord and coord
plt.figure()
import seaborn as sns
import matplotlib.pyplot as plt
#fig, ax1 = plt.subplots(1,1)

sns.lineplot(data = data_df, x = "Vehicles", y = "Redux Dbl Park phi15 norm FCFS", hue = "Parking Spaces",
              palette = "tab10", ci = 95, linestyle = 'solid', legend = 'full')


plt.suptitle('% of Reduction in Dbl Parking to Uncoord Dbl Parking (phi = 15)')
plt.title('Avg and 95% CI')

plt.ylabel("% Reduction in Dbl Parking (minutes)")
plt.xlabel("Quantity of Delivery Vehicles")

plt.legend(title = 'Parking Spaces', loc = 'upper right')

plt.show()
##############################################################################






















#Average number of unscheduled vehicles with phi = 5
count_dbl_park_events_df_inst_phi5 = pd.DataFrame(index = range(len(truck_scenarios)), columns = ['Trucks', 1, 2, 3, 4], dtype = object).applymap(lambda x: [])
count_dbl_park_events_df_inst_phi5['Trucks'] = truck_scenarios
count_sched_Diff_df_inst_phi5 = pd.DataFrame(index = range(len(truck_scenarios)), columns = ['Trucks', 1, 2, 3, 4], dtype = object).applymap(lambda x: [])
count_dbl_park_events_df_inst_phi5['Trucks'] = truck_scenarios
max_parking_spaces = 4
for c in range(1, max_parking_spaces +1):
#for c in range(1, 2):
    
    n = 0
    
    for N in truck_scenarios:
    #for n in range(2, 4):
        
                
        for i in range(0, iterations):
        #for i in range(0, 4):
            
            #Record the number of raw double parking events as unscheduled delivery vehicles
            count_dbl_park_events_df_inst_phi5.iloc[n][c].append(len(dbl_park_events_df_inst_phi5[c][N][i]))
            
            #record the difference in number of unscheduled vehicles between FCFS and phi5
            count_sched_Diff_df_inst_phi5.iloc[n][c].append(dbl_park_FCFS_cancelled_inst[c][N][i] - len(dbl_park_events_df_inst_phi5[c][N][i]))
            

            
        n += 1

count_dbl_park_events_df_inst_AVG_phi5 = count_dbl_park_events_df_inst_phi5.applymap(lambda x: np.mean(x))

df = count_dbl_park_events_df_inst_AVG_phi5
df['Trucks'] = truck_scenarios
df = df.set_index('Trucks')

plt.figure()
df.plot()
plt.title("Average Unscheduled Delivery Vehicles (phi = 5)")
plt.xlabel("Quantity of Delivery Vehicles")
plt.ylabel('Average Unscheduled Delivery Vehicles')
plt.legend(title = 'Parking Spaces', loc = 'upper left')
plt.show()

#difference in the number of unscheduled vehicles for phi = 5 and FCFS
count_sched_Diff_df_inst_AVG_phi5 = count_sched_Diff_df_inst_phi5.applymap(lambda x: np.mean(x))

df = count_sched_Diff_df_inst_AVG_phi5
df['Trucks'] = truck_scenarios
df = df.set_index('Trucks')

plt.figure()
df.plot()
plt.title("Average Difference in Unscheduled Delivery Vehicles (phi = 5)")
plt.xlabel("Quantity of Delivery Vehicles")
plt.ylabel('Average Difference in Unscheduled Delivery Vehicles')
plt.legend(title = 'Parking Spaces', loc = 'upper left')
plt.show()



#3D graphic of Average reduction in total vehicle delay

#code from https://linuxtut.com/en/121e21df5904af4d281e/ on 29 Nov 2021
#https://likegeeks.com/3d-plotting-in-python/ modify axis and customize
import pandas as pd

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import pandas as pd
import seaborn as sns


df = AVG_total_veh_delay_Diff_inst_phi5
df['Trucks'] = truck_scenarios
df = df.set_index('Trucks')
#df = AVG_avg_veh_delay_Diff_inst_phi5[[1, 2, 3, 4]]

X = np.array([])
Y = np.array([])
Z = np.array([])

for i in range(df.index.size):
    X = np.concatenate([X, np.full(df.columns.size, df.index[i])], 0)

for i in range(df.index.size):
    Y = np.concatenate([Y, np.array(df.columns)], 0)

for i in range(df.index.size):
    Z = np.concatenate([Z, np.array(df[i:i+1])[0]], 0)
    
W = Z *(1/240)
    
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(X, Y, Z)
ax.set_xlabel('Trucks')
ax.set_ylabel('Parking Spaces')
ax.set_yticks([1, 2, 3, 4])
ax.set_zlabel('AVG Total Vehicle Delay')
ax.set_title('Average Reduction in Total Vehicle Delay (phi = 5)')
plt.show()


##############################################################################
#Confidence interval graphic generation - difference in fuel consumption uncoord to coord
data_df = pd.DataFrame(np.empty((3280, 5), dtype = float), columns = ["Parking Spaces","Vehicles", "Inst", "Redux Veh-Min", "Redux Fuel"])
row = 0
for c in range(1, 5):
    if c == 1:
        for n in range(0, 41):
            for i in range(0, 20):
                data_df.iloc[row, 0] = str(c)
                data_df.iloc[row, 1] = int(truck_scenarios[n])
                data_df.iloc[row, 2] = i+1
                data_df.iloc[row, 3] = float(total_veh_delay_Diff_inst_phi15[c][n][i])
                data_df.iloc[row, 4] = float(total_veh_delay_Diff_inst_phi15[c][n][i]/240)
                #data_df.iloc[row, 4] = float(sum_service[i])
                row += 1
                #print(row)
    elif c == 2:
        for n in range(0, 41):
            for i in range(0, 20):
                data_df.iloc[row, 0] = str(c)
                data_df.iloc[row, 1] = int(truck_scenarios[n])
                data_df.iloc[row, 2] = i+1
                data_df.iloc[row, 3] = float(total_veh_delay_Diff_inst_phi15[c][n][i])
                data_df.iloc[row, 4] = float(total_veh_delay_Diff_inst_phi15[c][n][i]/240)
                #data_df.iloc[row, 4] = float(sum_service[i])
                row += 1
                #print(row)
    elif c == 3:
        for n in range(0, 41):
            for i in range(0, 20):
                data_df.iloc[row, 0] = str(c)
                data_df.iloc[row, 1] = int(truck_scenarios[n])
                data_df.iloc[row, 2] = i+1
                data_df.iloc[row, 3] = float(total_veh_delay_Diff_inst_phi15[c][n][i])
                data_df.iloc[row, 4] = float(total_veh_delay_Diff_inst_phi15[c][n][i]/240)
                #data_df.iloc[row, 4] = float(sum_service[i])
                row += 1
                #print(row)
    elif c == 4:
        for n in range(0, 41):
            for i in range(0, 20):
                data_df.iloc[row, 0] = str(c)
                data_df.iloc[row, 1] = int(truck_scenarios[n])
                data_df.iloc[row, 2] = i+1
                data_df.iloc[row, 3] = float(total_veh_delay_Diff_inst_phi15[c][n][i])
                data_df.iloc[row, 4] = float(total_veh_delay_Diff_inst_phi15[c][n][i]/240)
                
                #data_df.iloc[row, 4] = float(sum_service[i])
                row += 1
                #print(row)
   


#plot total vehicle delay and fuel lost on the same graph
plt.figure()
import seaborn as sns
import matplotlib.pyplot as plt
fig, ax1 = plt.subplots(1,1)

sns.lineplot(data = data_df, x = "Vehicles", y = "Redux Veh-Min", hue = "Parking Spaces",
              palette = "tab10", ci = 95, ax = ax1, err_style = 'band')

ax2 = ax1.twinx()
sns.lineplot(data = data_df, x = "Vehicles", y = "Redux Fuel", hue = "Parking Spaces",
              palette = "tab10", ci = 95, ax = ax2, err_style = 'band')

#df_fuel.plot(ax = ax2, legend = None)
#ax1.set_ylim(0, 5520)
#ax2.set_ylim(0, 23)
ax1.legend(title = 'Parking Spaces', loc = 'upper right')
ax1.set_ylabel('Avg Reduction in Total Vehicle Delay (min)')
ax2.set_ylabel('Avg Reduction in Fuel Lost per day (gallons)')
ax1.set_xlabel("Quantity of Delivery Vehicles")
plt.suptitle("Avg Reduction in Vehicle Delay and Fuel (phi = 15, medium traffic)")
plt.title('95% Confidence Interval')
plt.show()


#extra plot
sns.lineplot(data = data_df, x = "Vehicles", y = "Redux Fuel", hue = "Parking Spaces",
              palette = "tab10", ci = 95)
plt.suptitle("Avg Reduction in Vehicle Fuel (phi = 15, low traffic)")
plt.title('95% Confidence Interval')
plt.legend(title = 'Parking Spaces', loc = 'upper right')
#plt.xticks(np.arange(0, 220, step = 20))
plt.xlabel("Quantity of Delivery Vehicles")
plt.ylabel('Avg Reduction in Fuel Lost (gallons)')

##############################################################################




##############################################################################
#Confidence interval graphic generation - fuel from FCFS only
data_df = pd.DataFrame(np.empty((3280, 5), dtype = float), columns = ["Parking Spaces","Vehicles", "Inst", "Redux Veh-Min", "Redux Fuel"])
row = 0
for c in range(1, 5):
    if c == 1:
        for n in range(0, 41):
            for i in range(0, 20):
                data_df.iloc[row, 0] = str(c)
                data_df.iloc[row, 1] = int(truck_scenarios[n])
                data_df.iloc[row, 2] = i+1
                data_df.iloc[row, 3] = float(total_veh_delay_inst_FCFS[c][n][i])
                data_df.iloc[row, 4] = float(total_veh_delay_inst_FCFS[c][n][i]/240)
                #data_df.iloc[row, 4] = float(sum_service[i])
                row += 1
                #print(row)
    elif c == 2:
        for n in range(0, 41):
            for i in range(0, 20):
                data_df.iloc[row, 0] = str(c)
                data_df.iloc[row, 1] = int(truck_scenarios[n])
                data_df.iloc[row, 2] = i+1
                data_df.iloc[row, 3] = float(total_veh_delay_inst_FCFS[c][n][i])
                data_df.iloc[row, 4] = float(total_veh_delay_inst_FCFS[c][n][i]/240)
                #data_df.iloc[row, 4] = float(sum_service[i])
                row += 1
                #print(row)
    elif c == 3:
        for n in range(0, 41):
            for i in range(0, 20):
                data_df.iloc[row, 0] = str(c)
                data_df.iloc[row, 1] = int(truck_scenarios[n])
                data_df.iloc[row, 2] = i+1
                data_df.iloc[row, 3] = float(total_veh_delay_inst_FCFS[c][n][i])
                data_df.iloc[row, 4] = float(total_veh_delay_inst_FCFS[c][n][i]/240)
                #data_df.iloc[row, 4] = float(sum_service[i])
                row += 1
                #print(row)
    elif c == 4:
        for n in range(0, 41):
            for i in range(0, 20):
                data_df.iloc[row, 0] = str(c)
                data_df.iloc[row, 1] = int(truck_scenarios[n])
                data_df.iloc[row, 2] = i+1
                data_df.iloc[row, 3] = float(total_veh_delay_inst_FCFS[c][n][i])
                data_df.iloc[row, 4] = float(total_veh_delay_inst_FCFS[c][n][i]/240)
                
                #data_df.iloc[row, 4] = float(sum_service[i])
                row += 1
                #print(row)
   


#plot total vehicle delay and fuel lost on the same graph
plt.figure()
import seaborn as sns
import matplotlib.pyplot as plt
fig, ax1 = plt.subplots(1,1)

sns.lineplot(data = data_df, x = "Vehicles", y = "Redux Veh-Min", hue = "Parking Spaces",
              palette = "tab10", ci = 95, ax = ax1, err_style = 'band')

ax2 = ax1.twinx()
sns.lineplot(data = data_df, x = "Vehicles", y = "Redux Fuel", hue = "Parking Spaces",
              palette = "tab10", ci = 95, ax = ax2, err_style = 'band')

#df_fuel.plot(ax = ax2, legend = None)
#ax1.set_ylim(0, 5520)
#ax2.set_ylim(0, 23)
#ax1.legend(title = 'Parking Spaces', loc = 'upper right')
ax1.set_ylabel('Avg Total Vehicle Delay (min)')
ax2.set_ylabel('Avg Fuel Lost per day (gallons)')
ax1.set_xlabel("Quantity of Delivery Vehicles")
plt.suptitle("Avg Vehicle Delay and Fuel (FCFS, medium traffic)")
plt.title('95% Confidence Interval')
plt.show()


#extra plot
sns.lineplot(data = data_df, x = "Vehicles", y = "Redux Fuel", hue = "Parking Spaces",
              palette = "tab10", ci = 95)
plt.suptitle("Avg Reduction in Vehicle Fuel (phi = 15, low traffic)")
plt.title('95% Confidence Interval')
plt.legend(title = 'Parking Spaces', loc = 'upper right')
#plt.xticks(np.arange(0, 220, step = 20))
plt.xlabel("Quantity of Delivery Vehicles")
plt.ylabel('Avg Reduction in Fuel Lost (gallons)')

##############################################################################


##############################################################################
#Confidence interval graphic generation - fuel from opt phi15 only
data_df = pd.DataFrame(np.empty((3280, 5), dtype = float), columns = ["Parking Spaces","Vehicles", "Inst", "Redux Veh-Min", "Redux Fuel"])
row = 0
for c in range(1, 5):
    if c == 1:
        for n in range(0, 41):
            for i in range(0, 20):
                data_df.iloc[row, 0] = str(c)
                data_df.iloc[row, 1] = int(truck_scenarios[n])
                data_df.iloc[row, 2] = i+1
                data_df.iloc[row, 3] = float(total_veh_delay_inst_phi15[c][n][i])
                data_df.iloc[row, 4] = float(total_veh_delay_inst_phi15[c][n][i]/240)
                #data_df.iloc[row, 4] = float(sum_service[i])
                row += 1
                #print(row)
    elif c == 2:
        for n in range(0, 41):
            for i in range(0, 20):
                data_df.iloc[row, 0] = str(c)
                data_df.iloc[row, 1] = int(truck_scenarios[n])
                data_df.iloc[row, 2] = i+1
                data_df.iloc[row, 3] = float(total_veh_delay_inst_phi15[c][n][i])
                data_df.iloc[row, 4] = float(total_veh_delay_inst_phi15[c][n][i]/240)
                #data_df.iloc[row, 4] = float(sum_service[i])
                row += 1
                #print(row)
    elif c == 3:
        for n in range(0, 41):
            for i in range(0, 20):
                data_df.iloc[row, 0] = str(c)
                data_df.iloc[row, 1] = int(truck_scenarios[n])
                data_df.iloc[row, 2] = i+1
                data_df.iloc[row, 3] = float(total_veh_delay_inst_phi15[c][n][i])
                data_df.iloc[row, 4] = float(total_veh_delay_inst_phi15[c][n][i]/240)
                #data_df.iloc[row, 4] = float(sum_service[i])
                row += 1
                #print(row)
    elif c == 4:
        for n in range(0, 41):
            for i in range(0, 20):
                data_df.iloc[row, 0] = str(c)
                data_df.iloc[row, 1] = int(truck_scenarios[n])
                data_df.iloc[row, 2] = i+1
                data_df.iloc[row, 3] = float(total_veh_delay_inst_phi15[c][n][i])
                data_df.iloc[row, 4] = float(total_veh_delay_inst_phi15[c][n][i]/240)
                
                #data_df.iloc[row, 4] = float(sum_service[i])
                row += 1
                #print(row)
   


#plot total vehicle delay and fuel lost on the same graph
plt.figure()
import seaborn as sns
import matplotlib.pyplot as plt
fig, ax1 = plt.subplots(1,1)

sns.lineplot(data = data_df, x = "Vehicles", y = "Redux Veh-Min", hue = "Parking Spaces",
              palette = "tab10", ci = 95, ax = ax1, err_style = 'band')

ax2 = ax1.twinx()
sns.lineplot(data = data_df, x = "Vehicles", y = "Redux Fuel", hue = "Parking Spaces",
              palette = "tab10", ci = 95, ax = ax2, err_style = 'band')

#df_fuel.plot(ax = ax2, legend = None)
#ax1.set_ylim(0, 5520)
#ax2.set_ylim(0, 23)
#ax1.legend(title = 'Parking Spaces', loc = 'upper right')
ax1.set_ylabel('Avg Total Vehicle Delay (min)')
ax2.set_ylabel('Avg Fuel Lost per day (gallons)')
ax1.set_xlabel("Quantity of Delivery Vehicles")
plt.suptitle("Avg Vehicle Delay and Fuel (phi15, medium traffic)")
plt.title('95% Confidence Interval')
plt.show()


#extra plot
sns.lineplot(data = data_df, x = "Vehicles", y = "Redux Fuel", hue = "Parking Spaces",
              palette = "tab10", ci = 95)
plt.suptitle("Avg Reduction in Vehicle Fuel (phi = 15, low traffic)")
plt.title('95% Confidence Interval')
plt.legend(title = 'Parking Spaces', loc = 'upper right')
#plt.xticks(np.arange(0, 220, step = 20))
plt.xlabel("Quantity of Delivery Vehicles")
plt.ylabel('Avg Reduction in Fuel Lost (gallons)')

##############################################################################













#possibly the meshgrid, surf plot version of the above scatter plot
#https://www.mathworks.com/matlabcentral/answers/387362-how-do-i-create-a-3-dimensional-surface-from-x-y-z-points

#2D plot of average reduction in total vehicle delay
plt.figure()
df.plot()
plt.title("Average Reduction in Total Vehicle Delay (phi = 5)")
plt.xlabel("Quantity of Delivery Vehicles")
plt.ylabel('Average Reduction in Total Vehicle Delay (min)')
plt.legend(title = 'Parking Spaces', loc = 'upper right')
plt.show()


#scaled for idling gallons lost
df_fuel = df.applymap(lambda x: (1/240)*x)

plt.figure()
df_fuel.plot()
plt.title("Average Reduction in Gallons of Fuel Lost (phi = 5)")
plt.xlabel("Quantity of Delivery Vehicles")
plt.ylabel('Average Reduction in Fuel Lost (gallons)')
plt.legend(title = 'Parking Spaces', loc = 'upper right')
plt.show()

#plot total vehicle delay and fuel lost on the same graph
plt.figure()
fig, ax1 = plt.subplots(1,1)
#ax1.set_xlim(0, 20)
#ax1.set_ylim(0, 65000)
#ax1.set_xticks([0,5,10,15,20])
df.plot(ax = ax1)
ax2 = ax1.twinx()
#ax2.set_ylim(0, 65000/240)
df_fuel.plot(ax = ax2, legend = None)
ax1.legend(title = 'Parking Spaces', loc = 'upper right')
ax1.set_ylabel('Avg Reduction in Total Vehicle Delay (min)')
ax2.set_ylabel('Avg Reduction in Fuel Lost (gallons)')
ax1.set_xlabel("Quantity of Delivery Vehicles")
plt.title('Avg Reduction in Vehicle Delay and Fuel (phi = 5)')
plt.show()







#graphics for the story of the disconnect between objective functions and net double parking

#do I need to run my models out to larger than 200 DVs to see the asymptote?
#maybe FCFS is so damn inefficient that it cannot fill all of the gaps perfectly like smart curbspace can, 
#and this is why smart curbspace can reduce metrics, but only by a small consistent amount

#but why the peak early on?  Smart curbspace wants to schedule large service duration vehicles, or
#atleast shuffle arrivals such that there are fewer double parked vehicles, FCFS doesn't do this
#THAT's the different, smart curbspace has just fewer double parking events overall and as a result likely
#to have less net double parking as well



##############################################################################
# Average of Total Double Parking phi = 15
dbl_park_Opt_inst_phi15_AVG = dbl_park_Opt_inst_phi15.applymap(lambda x: np.mean(x))
low_res_1 = []
low_res_2 = []
low_res_3 = []
low_res_4 = []
for j in truck_scenarios:
    low_res_1.append(dbl_park_Opt_inst_phi15_AVG[1][j])
    low_res_2.append(dbl_park_Opt_inst_phi15_AVG[2][j])
    low_res_3.append(dbl_park_Opt_inst_phi15_AVG[3][j])
    low_res_4.append(dbl_park_Opt_inst_phi15_AVG[4][j])

dbl_park_Opt_inst_phi15_AVG_low_res = pd.DataFrame({"Trucks": truck_scenarios,
                                                    "1": low_res_1,
                                                    "2": low_res_2,
                                                    "3": low_res_3,
                                                    "4": low_res_4})

df = dbl_park_Opt_inst_phi15_AVG_low_res
df = df.set_index('Trucks')
plt.figure()
df.plot()
plt.title("Average of Total Dbl Parking Minutes (phi = 15)")
plt.xlabel("Quantity of Delivery Vehicles")
plt.ylabel('Avg Double Parking (min)')
plt.legend(title = 'Parking Spaces', loc = 'lower right')
plt.show()




#Confidence interval graphic generation
low_res_1 = []
low_res_2 = []
low_res_3 = []
low_res_4 = []
for j in truck_scenarios:
    low_res_1.append(dbl_park_Opt_inst_phi15[1][j])
    low_res_2.append(dbl_park_Opt_inst_phi15[2][j])
    low_res_3.append(dbl_park_Opt_inst_phi15[3][j])
    low_res_4.append(dbl_park_Opt_inst_phi15[4][j])

dbl_park_Opt_inst_phi15_low_res = pd.DataFrame({"Trucks": truck_scenarios,
                                                    "1": low_res_1,
                                                    "2": low_res_2,
                                                    "3": low_res_3,
                                                    "4": low_res_4})



data_df = pd.DataFrame(np.empty((3280, 4), dtype = float), columns = ["Parking Spaces","Vehicles", "Inst", "Total Dbl Park phi15"])
row = 0
for c in range(1, 5):
    if c == 1:
        for n in range(0, 41):
            for i in range(0, 20):
                data_df.iloc[row, 0] = str(c)
                data_df.iloc[row, 1] = int(truck_scenarios[n])
                data_df.iloc[row, 2] = i+1
                data_df.iloc[row, 3] = float(dbl_park_Opt_inst_phi15_low_res.iloc[n][c][i])
                
                #data_df.iloc[row, 4] = float(sum_service[i])
                row += 1
                #print(row)
    elif c == 2:
        for n in range(0, 41):
            for i in range(0, 20):
                data_df.iloc[row, 0] = str(c)
                data_df.iloc[row, 1] = int(truck_scenarios[n])
                data_df.iloc[row, 2] = i+1
                data_df.iloc[row, 3] = float(dbl_park_Opt_inst_phi15_low_res.iloc[n][c][i])
                
                #data_df.iloc[row, 4] = float(sum_service[i])
                row += 1
                #print(row)
    elif c == 3:
        for n in range(0, 41):
            for i in range(0, 20):
                data_df.iloc[row, 0] = str(c)
                data_df.iloc[row, 1] = int(truck_scenarios[n])
                data_df.iloc[row, 2] = i+1
                data_df.iloc[row, 3] = float(dbl_park_Opt_inst_phi15_low_res.iloc[n][c][i])
                
                #data_df.iloc[row, 4] = float(sum_service[i])
                row += 1
                #print(row)
    elif c == 4:
        for n in range(0, 41):
            for i in range(0, 20):
                data_df.iloc[row, 0] = str(c)
                data_df.iloc[row, 1] = int(truck_scenarios[n])
                data_df.iloc[row, 2] = i+1
                data_df.iloc[row, 3] = float(dbl_park_Opt_inst_phi15_low_res.iloc[n][c][i])
                
                
                #data_df.iloc[row, 4] = float(sum_service[i])
                row += 1
                #print(row)
   

#plot minutes of lane obstruction between uncoord and coord
plt.figure()
import seaborn as sns
import matplotlib.pyplot as plt
#fig, ax1 = plt.subplots(1,1)

sns.lineplot(data = data_df, x = "Vehicles", y = "Total Dbl Park phi15", hue = "Parking Spaces",
              palette = "tab10", ci = 95, linestyle = 'solid', legend = 'full')

plt.suptitle("Average of Total Double Parking Minutes (phi = 15)")
plt.title('95% Confidence Interval')
plt.xlabel("Quantity of Delivery Vehicles")
plt.ylabel('Avg Double Parking (min)')
plt.legend(title = 'Parking Spaces', loc = 'lower right', prop={'size': 8})
plt.show()
##############################################################################






##############################################################################
#Average of Total Minutes of Lane Obstruction phi = 15

df = net_dbl_park_minutes_df_inst_phi15
df = df.applymap(lambda x: np.mean(x))
df['Trucks'] = truck_scenarios
df = df.set_index('Trucks')
plt.figure()
df.plot()
plt.title("Average of Net Dbl Parking Minutes (phi = 15)")
plt.xlabel("Quantity of Delivery Vehicles")
plt.ylabel('Avg Double Parking (min)')
plt.legend(title = 'Parking Spaces', loc = 'lower right')
plt.show()



#Confidence interval graphic generation
data_df = pd.DataFrame(np.empty((3280, 4), dtype = float), columns = ["Parking Spaces","Vehicles", "Inst", "Net Dbl Park phi15"])
row = 0
for c in range(1, 5):
    if c == 1:
        for n in range(0, 41):
            for i in range(0, 20):
                data_df.iloc[row, 0] = str(c)
                data_df.iloc[row, 1] = int(truck_scenarios[n])
                data_df.iloc[row, 2] = i+1
                data_df.iloc[row, 3] = float(net_dbl_park_minutes_df_inst_phi15[c][n][i])
                
                #data_df.iloc[row, 4] = float(sum_service[i])
                row += 1
                #print(row)
    elif c == 2:
        for n in range(0, 41):
            for i in range(0, 20):
                data_df.iloc[row, 0] = str(c)
                data_df.iloc[row, 1] = int(truck_scenarios[n])
                data_df.iloc[row, 2] = i+1
                data_df.iloc[row, 3] = float(net_dbl_park_minutes_df_inst_phi15[c][n][i])
                
                #data_df.iloc[row, 4] = float(sum_service[i])
                row += 1
                #print(row)
    elif c == 3:
        for n in range(0, 41):
            for i in range(0, 20):
                data_df.iloc[row, 0] = str(c)
                data_df.iloc[row, 1] = int(truck_scenarios[n])
                data_df.iloc[row, 2] = i+1
                data_df.iloc[row, 3] = float(net_dbl_park_minutes_df_inst_phi15[c][n][i])
                
                #data_df.iloc[row, 4] = float(sum_service[i])
                row += 1
                #print(row)
    elif c == 4:
        for n in range(0, 41):
            for i in range(0, 20):
                data_df.iloc[row, 0] = str(c)
                data_df.iloc[row, 1] = int(truck_scenarios[n])
                data_df.iloc[row, 2] = i+1
                data_df.iloc[row, 3] = float(net_dbl_park_minutes_df_inst_phi15[c][n][i])
                
                
                #data_df.iloc[row, 4] = float(sum_service[i])
                row += 1
                #print(row)


#plot minutes of lane obstruction between uncoord and coord
plt.figure()
import seaborn as sns
import matplotlib.pyplot as plt
#fig, ax1 = plt.subplots(1,1)

sns.lineplot(data = data_df, x = "Vehicles", y = "Net Dbl Park phi15", hue = "Parking Spaces",
              palette = "tab10", ci = 95, linestyle = 'solid', legend = 'full')

plt.suptitle("Average of Lane Obstruction Minutes (phi = 15)")
plt.title('95% Confidence Interval')
plt.xlabel("Quantity of Delivery Vehicles")
plt.ylabel('Avg Lane Obstruction Parking (min)')
plt.legend(title = 'Parking Spaces', loc = 'lower right')
plt.show()
##############################################################################







##############################################################################
#compare lane obstruction graphic
df = net_dbl_park_minutes_df_inst_phi30
df = df.applymap(lambda x: np.mean(x))
df['Trucks'] = truck_scenarios
df = df.set_index('Trucks')
plt.figure()
plt.plot(df[1], label = 'Coord 1')
plt.plot(df[2], label = 'Coord 2')
plt.plot(df[3], label = 'Coord 3')
plt.plot(df[4], label = 'Coord 4')
df = net_dbl_park_minutes_df_inst_FCFS
df = df.applymap(lambda x: np.mean(x))
df['Trucks'] = truck_scenarios
df = df.set_index('Trucks')
plt.plot(df[1], color = 'blue', linestyle = 'dashed', label = 'Uncoord 1')
plt.plot(df[2], color = 'orange', linestyle = 'dashed', label = 'Uncoord 2')
plt.plot(df[3], color = 'green', linestyle = 'dashed', label = 'Uncoord 3')
plt.plot(df[4], color = 'red', linestyle = 'dashed', label = 'Uncoord 4')
plt.legend(title = 'Parking Spaces', loc = 'lower right')
plt.title("Comparison of Minutes of Lane Obstruction (phi = 30)")
plt.xlabel("Quantity of Delivery Vehicles")
plt.ylabel('Avg Minutes of Lane Obstruction')
plt.show()

##############################################################################


##############################################################################
#compare lane obstruction graphic w/ CI

#Confidence interval graphic generation
data_df = pd.DataFrame(np.empty((3280, 5), dtype = float), columns = ["Parking Spaces","Vehicles", "Inst", "Net Dbl Park FCFS", "Net Dbl Park phi30"])
#data_df = pd.DataFrame(np.empty((2460, 5), dtype = float), columns = ["Parking Spaces","Vehicles", "Inst", "Net Dbl Park FCFS", "Net Dbl Park phi30"])

row = 0
for c in range(1, 5):
    if c == 1:
        for n in range(0, 41):
            for i in range(0, 20):
                data_df.iloc[row, 0] = str(c)
                data_df.iloc[row, 1] = int(truck_scenarios[n])
                data_df.iloc[row, 2] = i+1
                data_df.iloc[row, 3] = float(net_dbl_park_minutes_df_inst_FCFS[c][n][i])/60
                data_df.iloc[row, 4] = float(net_dbl_park_minutes_df_inst_phi30[c][n][i])/60
                #data_df.iloc[row, 4] = float(sum_service[i])
                row += 1
                #print(row)
    elif c == 2:
    #if c == 2:
        for n in range(0, 41):
            for i in range(0, 20):
                data_df.iloc[row, 0] = str(c)
                data_df.iloc[row, 1] = int(truck_scenarios[n])
                data_df.iloc[row, 2] = i+1
                data_df.iloc[row, 3] = float(net_dbl_park_minutes_df_inst_FCFS[c][n][i])/60
                data_df.iloc[row, 4] = float(net_dbl_park_minutes_df_inst_phi30[c][n][i])/60
                #data_df.iloc[row, 4] = float(sum_service[i])
                row += 1
                #print(row)
    elif c == 3:
        for n in range(0, 41):
            for i in range(0, 20):
                data_df.iloc[row, 0] = str(c)
                data_df.iloc[row, 1] = int(truck_scenarios[n])
                data_df.iloc[row, 2] = i+1
                data_df.iloc[row, 3] = float(net_dbl_park_minutes_df_inst_FCFS[c][n][i])/60
                data_df.iloc[row, 4] = float(net_dbl_park_minutes_df_inst_phi30[c][n][i])/60
                #data_df.iloc[row, 4] = float(sum_service[i])
                row += 1
                #print(row)
    elif c == 4:
        for n in range(0, 41):
            for i in range(0, 20):
                data_df.iloc[row, 0] = str(c)
                data_df.iloc[row, 1] = int(truck_scenarios[n])
                data_df.iloc[row, 2] = i+1
                data_df.iloc[row, 3] = float(net_dbl_park_minutes_df_inst_FCFS[c][n][i])/60
                data_df.iloc[row, 4] = float(net_dbl_park_minutes_df_inst_phi30[c][n][i])/60
                
                #data_df.iloc[row, 4] = float(sum_service[i])
                row += 1
                #print(row)
   

#plot minutes of lane obstruction between uncoord and coord
plt.figure()
import seaborn as sns
import matplotlib.pyplot as plt
fig, ax1 = plt.subplots(1,1)

sns.lineplot(data = data_df, x = "Vehicles", y = "Net Dbl Park FCFS", hue = "Parking Spaces",
              palette = "tab10", ci = 95, linestyle = 'solid', legend = 'full')
sns.lineplot(data = data_df, x = "Vehicles", y = "Net Dbl Park phi30", hue = "Parking Spaces",
              palette = "tab10", ci = 95, linestyle = '--', legend = False)


plt.legend(title = '   Parking Spaces\n (Solid = Uncoord\nDashed = Optimal)', loc = 'lower right')
plt.suptitle("Comparison of Avg Minutes of Lane Obstruction (phi = 30)")
plt.title('95% Confidence Interval')
plt.xticks(np.arange(0, 220, step = 20))
plt.xlabel("Quantity of Delivery Vehicles")
plt.ylabel('Avg Total Lane Obstruction (hours)')

plt.show()
##############################################################################





##############################################################################
#Why are the net double parking events weird?  Having an impact on the flex results
net_dbl_park_minutes_Diff_df_inst_phi15 = pd.DataFrame(index = range(len(truck_scenarios)), columns = ['Trucks', 1, 2, 3, 4], dtype = object).applymap(lambda x: [])
AVG_net_dbl_park_minutes_Diff_df_inst_phi15 = pd.DataFrame(index = range(len(truck_scenarios)), columns = ['Trucks', 1, 2, 3, 4], dtype = object).applymap(lambda x: [])


for c in range(1, 5):
    for n in range(0, 41):
        for i in range(0, 20):
            if net_dbl_park_events_df_inst_phi15[c][n][i].empty == True:
                net_dbl_park_minutes_Diff_df_inst_phi15.iloc[n][c].append(0)
            elif net_dbl_park_events_df_inst_FCFS[c][n][i].empty == True:
                net_dbl_park_minutes_Diff_df_inst_phi15.iloc[n][c].append(0)
            else:
                net_dbl_park_minutes_Diff_df_inst_phi15.iloc[n][c].append(np.sum(net_dbl_park_events_df_inst_FCFS[c][n][i]['Total']) - np.sum(net_dbl_park_events_df_inst_phi15[c][n][i]['Total']))

df = net_dbl_park_minutes_Diff_df_inst_phi15
df = df.applymap(lambda x: np.mean(x))
df['Trucks'] = truck_scenarios
df = df.set_index('Trucks')

plt.figure()
df.plot()
plt.title("Avg Reduction of Net Dbl Parking Minutes (phi15)")
plt.xlabel("Quantity of Delivery Vehicles")
plt.ylabel('Avg Reduction Net Dbl Parking (min)')
plt.legend(title = 'Parking Spaces', loc = 'upper right')
plt.show()

##############################################################################



##############################################################################
# Reduction in lane obstruction events with CI

#Confidence interval graphic generation
data_df = pd.DataFrame(np.empty((3280, 4), dtype = float), columns = ["Parking Spaces","Vehicles", "Inst", "Net Dbl Park Diff phi15"])
row = 0
for c in range(1, 5):
    if c == 1:
        for n in range(0, 41):
            for i in range(0, 20):
                data_df.iloc[row, 0] = str(c)
                data_df.iloc[row, 1] = int(truck_scenarios[n])
                data_df.iloc[row, 2] = i+1
                data_df.iloc[row, 3] = float(net_dbl_park_minutes_Diff_df_inst_phi15[c][n][i])
                
                #data_df.iloc[row, 4] = float(sum_service[i])
                row += 1
                #print(row)
    elif c == 2:
        for n in range(0, 41):
            for i in range(0, 20):
                data_df.iloc[row, 0] = str(c)
                data_df.iloc[row, 1] = int(truck_scenarios[n])
                data_df.iloc[row, 2] = i+1
                data_df.iloc[row, 3] = float(net_dbl_park_minutes_Diff_df_inst_phi15[c][n][i])
                
                #data_df.iloc[row, 4] = float(sum_service[i])
                row += 1
                #print(row)
    elif c == 3:
        for n in range(0, 41):
            for i in range(0, 20):
                data_df.iloc[row, 0] = str(c)
                data_df.iloc[row, 1] = int(truck_scenarios[n])
                data_df.iloc[row, 2] = i+1
                data_df.iloc[row, 3] = float(net_dbl_park_minutes_Diff_df_inst_phi15[c][n][i])
                
                #data_df.iloc[row, 4] = float(sum_service[i])
                row += 1
                #print(row)
    elif c == 4:
        for n in range(0, 41):
            for i in range(0, 20):
                data_df.iloc[row, 0] = str(c)
                data_df.iloc[row, 1] = int(truck_scenarios[n])
                data_df.iloc[row, 2] = i+1
                data_df.iloc[row, 3] = float(net_dbl_park_minutes_Diff_df_inst_phi15[c][n][i])
                
                
                #data_df.iloc[row, 4] = float(sum_service[i])
                row += 1
                #print(row)


#plot minutes of reduction of lane obstruction between uncoord and coord
plt.figure()
import seaborn as sns
import matplotlib.pyplot as plt
#fig, ax1 = plt.subplots(1,1)

sns.lineplot(data = data_df, x = "Vehicles", y = "Net Dbl Park Diff phi15", hue = "Parking Spaces",
              palette = "tab10", ci = 95, linestyle = 'solid', legend = 'full')

plt.suptitle("Avg Reduction of Lane Obstruction Minutes (phi = 15)")
plt.title('95% Confidence Interval')
plt.xlabel("Quantity of Delivery Vehicles")
plt.ylabel('Avg Reduction in Lane Obstruction (min)')
plt.legend(title = 'Parking Spaces', loc = 'upper right')
plt.ylim(0, 185)
plt.show()



##############################################################################









df = veh_in_queue_inst_phi5
df = df.applymap(lambda x: np.mean(x))
df['Trucks'] = truck_scenarios
df = df.set_index('Trucks')
plt.figure()
df.plot()
plt.title("Average Vehicles in the Queue (phi = 5)")
plt.xlabel("Quantity of Delivery Vehicles")
plt.ylabel('Avg Vehicles in Queue')
plt.legend(title = 'Parking Spaces', loc = 'lower right')
plt.show()


df = avg_veh_delay_inst_phi5
df = df.applymap(lambda x: np.mean(x))
df['Trucks'] = truck_scenarios
df = df.set_index('Trucks')
plt.figure()
df.plot()
plt.title("Average of the Average Vehicle Delay (phi = 5)")
plt.xlabel("Quantity of Delivery Vehicles")
plt.ylabel('Avg of Avg Vehicle Delay (min)')
plt.legend(title = 'Parking Spaces', loc = 'lower right')
plt.show()


df = AVG_veh_in_queue_Diff_inst_phi5
df['Trucks'] = truck_scenarios
df = df.set_index('Trucks')
plt.figure()
df.plot()
plt.title("Avg Reduction of Vehicles in the Queue (phi = 5)")
plt.xlabel("Quantity of Delivery Vehicles")
plt.ylabel('Avg Reduction of Vehicles in the Queue')
plt.legend(title = 'Parking Spaces', loc = 'upper right')
plt.show()







##############################################################################
#Limit graphics

#plot the queue from a specific scenario and instance as an illustrative example
df = veh_in_queue_inst_phi5[1][5][1]
plt.figure()
plt.plot(df, linestyle = 'dashed', label = 'phi5')
df = veh_in_queue_inst_FCFS[1][5][1]
plt.plot(df, linestyle = 'dotted', label = 'FCFS')
plt.legend()
plt.show()

##############################################################################









##############################################################################
# Queuing Total Minutes of Vehicle Delay Calc

import numpy as np
import scipy.integrate as integrate



#infinite queue, madeup case
def piece(x):
    if (x >= 0) and (x < 120):
        return 0.5*x
    elif (x >= 120) and (x < 180):
        return 2*x - 180
    else:
        return 1*x


[total_veh_delay, error] = integrate.quad(lambda x: 1*x - piece(x), 0, 180)
print(total_veh_delay)

[total_veh_delay_arrival, error] = integrate.quad(lambda x: 1*x, 0, 180)

[total_veh_delay_depart, error] = integrate.quad(lambda x: piece(x), 0, 180)

total_veh_delay2 = total_veh_delay_arrival - total_veh_delay_depart
print(total_veh_delay)

# x = np.linspace(0, 180, 10)
# condlist = []
# funclist = []

# funclist.append(lambda x: 0.5*x)
# funclist.append(lambda x: 2*x - 180)

# condlist.append(np.logical_and((x >= 0), (x < 120)))
# condlist.append(np.logical_and((x >= 120), (x < 180)))


# func = lambda x: np.piecewise(x, condlist, funclist)

# [total_veh_delay_arrival, error] = integrate.quad(lambda x: 1*x, 0, 180)

# [total_veh_delay_depart, error] = integrate.quad(func, 0, 180)

# total_veh_delay = total_veh_delay_arrival - total_veh_delay_depart



#Max Queue = 30, madeup case
def piece(x):
    if (x >= 0) and (x < 60):
        return 0.5*x
    elif (x >= 60) and (x < 120):
        return 1*x - 30
    elif (x >= 120) and (x < 150):
        return 2*x - 150
    else:
        return 1*x


[total_veh_delay, error] = integrate.quad(lambda x: 1*x - piece(x), 0, 180)
print(total_veh_delay)



#infinite queue, medium rates
def piece(x):
    if (x >= 0) and (x < 500):
        return 8.333*x
    elif (x >= 500) and (x < 1000):
        return 16.6667*x - 4166.667
    else:
        return 12.5*x


[total_veh_delay, error] = integrate.quad(lambda x: 12.5*x - piece(x), 0, 1000)
print(total_veh_delay)

##############################################################################




#extra graphics
df = AVG_queue_duration_Diff_inst_phi5
df['Trucks'] = truck_scenarios
df = df.set_index('Trucks')

plt.figure()
df.plot()
plt.title("Average Reduction in Total Queue Duration (phi = 5)")
plt.xlabel("Quantity of Delivery Vehicles")
plt.ylabel('Average Reduction in Total Queue Duration (min)')
plt.legend(title = 'Parking Spaces', loc = 'upper right')
plt.show()


df = AVG_veh_in_queue_Diff_inst_phi5
df['Trucks'] = truck_scenarios
df = df.set_index('Trucks')

plt.figure()
df.plot()
plt.title("Average Reduction in Total Vehicles in the Queue (phi = 5)")
plt.xlabel("Quantity of Delivery Vehicles")
plt.ylabel('Average Reduction in Total Vehicles in the Queue')
plt.legend(title = 'Parking Spaces', loc = 'upper right')
plt.show()


df = AVG_avg_veh_delay_Diff_inst_phi5
df['Trucks'] = truck_scenarios
df = df.set_index('Trucks')

plt.figure()
df.plot()
plt.title("Average Reduction in Average Vehicle Delay (phi = 5)")
plt.xlabel("Quantity of Delivery Vehicles")
plt.ylabel('Average Reduction in Average Vehicle Delay (min)')
plt.legend(title = 'Parking Spaces', loc = 'upper right')
plt.show()


df = AVG_avg_len_queue_Diff_inst_phi5
df['Trucks'] = truck_scenarios
df = df.set_index('Trucks')

plt.figure()
df.plot()
plt.title("Average Reduction in Average Queue Length (phi = 5)")
plt.xlabel("Quantity of Delivery Vehicles")
plt.ylabel('Average Reduction in Average Queue Length')
plt.legend(title = 'Parking Spaces', loc = 'upper right')
plt.show()

    




