# -*- coding: utf-8 -*-
"""
Created on Wed Sep  7 16:02:14 2022

@author: Aaron
"""

import numpy as np
import pandas as pd
import pickle
import time
import matplotlib.pyplot as plt
import seaborn as sns

tic = time.time()



#optimal w/ buffer, randomly shifted arrivals, reassassed parking schedule
with open('pub_Pitt_reassessed_combined_2_Dec_2022_buffer_5.pkl', 'rb') as file:
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



dbl_park_Diff_inst_phi5_df = pd.DataFrame()


for c_index in range(1, max_parking_spaces +1):
    
    dbl_park_Diff_instance = []
    
    for i_index in range(0, iterations):
        print('c = ' + str(c_index) + ' i = ' + str(i_index))
        
        #calc the sum of the dbl parking service duration for FCFS and phiX
        dbl_parking_FCFS_sum = np.sum(dbl_park_events_df_inst_FCFS_df.iloc[i_index, c_index -1]['s_i'])
        dbl_parking_phi5_sum = np.sum(dbl_park_events_df_inst_phi5_df.iloc[i_index, c_index -1]['s_i'])
        
        #take the diff or reduction in dbl parking (FCFS - phiX, want this value to be positive reduction)
        Diff = dbl_parking_FCFS_sum - dbl_parking_phi5_sum
        
        #store the Diff with the other instances for a fix parking space number, c_index
        dbl_park_Diff_instance.append(Diff)




    #at the completion of the iterations for a specific number of parking spaces, c_index
    #store the list of Diff in the larger dataframe
    dbl_park_Diff_inst_phi5_df[c_index] = dbl_park_Diff_instance



toc = time.time()

runtime = toc-tic
print('runtime: ' + str(runtime))

# import pickle
# with open('pub_Pitt_reassessed_combined_3_Dec_2022_buffer_5_redux_graphic_prep.pkl', 'wb') as file: 
#     pickle.dump(
#         [n_index_lst_df, 
#           n_index_norm_lst_df, 
#           arrival_dfs_df, 
#           sum_service_df, 
#           dbl_park_Opt_status_inst_phi5_df, 
#           PAPvAP_inst_phi5_df, 
#           park_demand_Opt_inst_phi5_df, 
#           park_events_df_inst_phi5_shifted,
#           park_events_df_inst_phi5_shifted,
#           runtime, 
#           buffer,
#           end,
#           iterations,
#           max_parking_spaces,
#           phi,
#           park_events_df_inst_phi5_df, 
#           dbl_park_events_df_inst_phi5_df,
#           dbl_park_events_df_inst_FCFS_df,
#           dbl_park_Diff_inst_phi5_df
#           ],
#             file)

















