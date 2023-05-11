# -*- coding: utf-8 -*-
"""
Created on Sat Jun 18 18:56:09 2022

@author: Aaron
"""

import numpy as np
import pandas as pd
import pickle
import time

tic = time.time()

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

        
        
        
        
        
        
        
#workflow
#pull the parking schedule
#shift each event by random, update the departure
#resort the schedule based on the new a_i
#store out the new schedule

max_DVs = max(n_index_lst_df.max())
     
park_events_df_inst_FCFS_shifted = pd.DataFrame(index = range(iterations), columns = range(max_parking_spaces +1), dtype = object).applymap(lambda x: [])
park_events_df_inst_phi5_shifted = pd.DataFrame(index = range(iterations), columns = range(max_parking_spaces +1), dtype = object).applymap(lambda x: [])


#shift for FCFS
for c in range(1, max_parking_spaces +1):
#for c in range(1,4):
    #for i in range(78,79):
    for i in range(0, iterations):
        print('FCFS: c = ', c, ' i = ', i)
        
        
        
        #adjust to the various number of delivery vehicles, 14 total option per
        #parking space, by the actual number of delivery vehicles varies based
        #on the number of parking spaces
        #n_index = int(DV_scenarios.iloc[n][c-1])
        
        OG_sched = park_events_df_inst_FCFS_df.iloc[i, c-1]
        #print(OG_sched)
        
        shift_sched = pd.DataFrame(columns = ['Truck', 't_i', 's_i', 'd_i', 'a_i_OG', 'd_i_OG', 'Park Type'])
        
        #step through the event in the original schedule and shift the arrival by a random normal
        for event in range(0, len(OG_sched)):
            data = []
            data.append(OG_sched['Truck'][event])
            shift_arrival = OG_sched['a_i'][event] + np.random.normal(0,2)
            if shift_arrival < 0:
                shift_arrival = 0
            #print(shift_arrival)
            data.append(shift_arrival)
            data.append(OG_sched['s_i'][event])
            data.append(shift_arrival + OG_sched['s_i'][event])
            data.append(OG_sched['a_i'][event])
            data.append(OG_sched['a_i'][event] + OG_sched['s_i'][event])
            data.append(OG_sched['Park Type'][event])
            shift_sched.loc[len(shift_sched)] = data
            
            #reset the new schedule based on ascending values of a_i
            shift_sched = shift_sched.sort_values(['t_i'], ascending = True)
            shift_sched.reset_index(level = 0, drop = True, inplace = True)


       # print(shift_sched)   
        
        park_events_df_inst_FCFS_shifted.iloc[i, c].append(shift_sched)
        

# #shift for phi5     
for c in range(1, max_parking_spaces +1):
#for c in range(1,4):
    #for i in range(78,79):
    for i in range(0, iterations):
        print('Phi5: c = ', c, ' i = ', i)
        
        #adjust to the various number of delivery vehicles, 14 total option per
        #parking space, by the actual number of delivery vehicles varies based
        #on the number of parking spaces
        #n_index = int(DV_scenarios.iloc[n][c-1])
        
        OG_sched = park_events_df_inst_phi5_df.iloc[i, c-1]
        #print(OG_sched)
        
        shift_sched = pd.DataFrame(columns = ['Truck', 't_i', 's_i', 'd_i', 'a_i_OG', 'd_i_OG', 'Park Type'])
        
        #step through the event in the original schedule and shift the arrival by a random normal
        for event in range(0, len(OG_sched)):
            data = []
            data.append(OG_sched['Truck'][event])
            shift_arrival = OG_sched['a_i'][event] + np.random.normal(0,2)
            if shift_arrival < 0:
                shift_arrival = 0
            #print(shift_arrival)
            data.append(shift_arrival)
            data.append(OG_sched['s_i'][event])
            data.append(shift_arrival + OG_sched['s_i'][event])
            data.append(OG_sched['a_i'][event])
            data.append(OG_sched['a_i'][event] + OG_sched['s_i'][event])
            data.append(OG_sched['Park Type'][event])
            shift_sched.loc[len(shift_sched)] = data
            
            #reset the new schedule based on ascending values of a_i
            shift_sched = shift_sched.sort_values(['t_i'], ascending = True)
            shift_sched.reset_index(level = 0, drop = True, inplace = True)


        #print(shift_sched)   
        
        park_events_df_inst_phi5_shifted.iloc[i, c].append(shift_sched)     
  
        
        
        
toc = time.time()

runtime = toc-tic
print('runtime: ' + str(runtime))



# #save data from the run
# import pickle
# with open('pub_Pitt_shifted_27_Nov_2022_buffer_5.pkl', 'wb') as file:
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
#           runtime, 
#           buffer,
#           end,
#           iterations,
#           max_parking_spaces,
#           phi],
#             file)


