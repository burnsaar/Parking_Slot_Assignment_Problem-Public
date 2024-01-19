# -*- coding: utf-8 -*-
"""
Created on Sat Aug 27 08:21:16 2022

@author: Aaron
"""


import pickle


#load data from shift_sched_update, random shifted optimal data
with open('pub_Aspen_reassessed_phi5_18_Jan_2024_buffer_15.pkl', 'rb') as file:
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
     Events, \
     Events_dbl_park_wait_poss_start, \
     late_no_starts_1, \
     late_no_starts_more_1, \
     early_no_starts_1, \
     early_no_starts_more_1, \
     change_sum_dbl_parking, \
     change_legal_and_dbl \
         = pickle.load(file)
         
         
#load data from the random shift and reassess FCFS data, from script: prep_FCFS_post_random_shift.py
with open('pub_Aspen_reassessed_FCFS_18_Jan_2024_buffer_15.pkl', 'rb') as file:
     n_index_lst_df, \
     n_index_norm_lst_df, \
     arrival_dfs_df, \
     sum_service_df, \
     dbl_park_Opt_status_inst_phi5_df, \
     PAPvAP_inst_phi5_df, \
     park_demand_Opt_inst_phi5_df, \
     park_events_df_inst_FCFS_shifted, \
     park_events_df_inst_phi5_shifted, \
     dbl_park_events_df_inst_FCFS_df, \
     runtime, \
     buffer, \
     end, \
     iterations, \
     max_parking_spaces, \
     phi \
         = pickle.load(file)
         
         
         
#combine the two dataset and save, creates the input requires for the lane obstruction script         
with open('pub_Aspen_reassessed_combined_18_Jan_2024_buffer_15.pkl', 'wb') as file: 
    pickle.dump(
        [n_index_lst_df, 
          n_index_norm_lst_df, 
          arrival_dfs_df, 
          sum_service_df, 
          dbl_park_Opt_status_inst_phi5_df, 
          PAPvAP_inst_phi5_df, 
          park_demand_Opt_inst_phi5_df, 
          park_events_df_inst_FCFS_shifted, #this should be updated to FCFS at the next possible update
          park_events_df_inst_phi5_shifted,
          runtime, 
          buffer,
          end,
          iterations,
          max_parking_spaces,
          phi,
          park_events_df_inst_phi5_df, 
          dbl_park_events_df_inst_phi5_df,
          dbl_park_events_df_inst_FCFS_df,
          Events,
          late_no_starts_1,
          late_no_starts_more_1,
          early_no_starts_1,
          early_no_starts_more_1,
          change_sum_dbl_parking,
          change_legal_and_dbl
          ],
            file)







