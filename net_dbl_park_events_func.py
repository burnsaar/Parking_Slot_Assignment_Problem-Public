# -*- coding: utf-8 -*-
"""
Created on Fri Nov 26 15:57:27 2021

@author: Burns
"""



import numpy as np
import pandas as pd
import pickle
import time

tic = time.time()

# max_trucks = 200


# #new, random uniform number of DVs, 100 iteration, run for record, use below for non-buffer case
# with open('pub_Aspen_run_for_record_6_Nov_2022.pkl', 'rb') as file:
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





# optimal w/ buffer, randomly shifted arrivals, reassassed parking schedule, run
# the below load instead
# with open('pub_Aspen_reassessed_combined_18_Jan_2024_buffer_15.pkl', 'rb') as file:
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



#new, random uniform number of DVs, 100 iteration, run for record Pitt data, use below for non-buffer case
# with open('pub_Pitt_run_for_record_24_Nov_2022.pkl', 'rb') as file:
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


# Pitt optimal w/ buffer, randomly shifted arrivals, reassassed parking schedule, run
# the below load instead
with open('pub_Pitt_reassessed_combined_18_Jan_2024_buffer_15.pkl', 'rb') as file:
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
            


def net_dbl_park_events(df):
    
    #if there wasn't any double parking to begin with, then there will also not be any net double parking
    if df.empty == True:
        #net_dbl_park_events_df_inst_phi0.iloc[n][c].append(dbl_park_events_df_inst_phi0[c][N][i])
        #dbl_parked_events = 
        dbl_parked_events = pd.DataFrame(columns = ["Start", "End", "Total", "Num Dbl Parked"])
    
    #if there is only a single double parking event from the original schedule
    elif len(df) == 1:
        
        #initialize the net double parking events dataframe, new dataframe for each iteration
        dbl_parked_events = pd.DataFrame(columns = ["Start", "End", "Total", "Num Dbl Parked"])
        
        df = df
        
        dbl_park_start = df.iloc[0]['a_i']
        dbl_park_end = df.iloc[0]['d_i']
        
        num_dbl_parked = 1
        
        dbl_parked_data = [dbl_park_start, dbl_park_end, dbl_park_end - dbl_park_start, num_dbl_parked]
        
        #add the latest double park event to the bottom of the new net dbl parked dataframe
        dbl_parked_events.loc[len(dbl_parked_events.index)] = dbl_parked_data
    
    #if there were two or double parking events...
    else:
        
        #initialize the net double parking events dataframe, new dataframe for each iteration
        dbl_parked_events = pd.DataFrame(columns = ["Start", "End", "Total", "Num Dbl Parked"])
        
        #establish the row variable as a counter through the original double parked vehicles dataset
        row = 0
        
        #sort the double parked vehicles in ascending arrival order
        df = df.sort_values('a_i')
        
        #initialize the first double parking event
        dbl_park_start = df.iloc[row]['a_i']
        dbl_park_end = df.iloc[row]['d_i']
        
        #initialize the number of dbl parked vehicles variable
        num_dbl_parked = 1
        
        #move to the next double parked truck
        row += 1
        
        for event in range(row, len(df)):
            
            #are we on the last double parking event?
            if event == len(df) -1:
                
                #if the next double parked trucks arrives during the current double parked truck
                if df.iloc[event]['a_i'] <= dbl_park_end:
                    #increment counter
                    num_dbl_parked += 1
                    #if the new double parked truck leaves after the current double parked truck, extend the double parked window
                    if df.iloc[event]['d_i'] > dbl_park_end:
                        dbl_park_end = df.iloc[event]['d_i']
                        
                    dbl_parked_data = [dbl_park_start, dbl_park_end, dbl_park_end - dbl_park_start, num_dbl_parked]
                    
                    #add the latest double park event to the bottom of the new net dbl parked dataframe
                    dbl_parked_events.loc[len(dbl_parked_events.index)] = dbl_parked_data
                        
                    
                    
                    
                elif df.iloc[event]['a_i'] > dbl_park_end:
                
                    #record the previous net dbl parking window
                    dbl_parked_data = [dbl_park_start, dbl_park_end, dbl_park_end - dbl_park_start, num_dbl_parked]
                    
                    #add the latest double park event to the bottom of the new net dbl parked dataframe
                    dbl_parked_events.loc[len(dbl_parked_events.index)] = dbl_parked_data
                    
                    #reset the start and end of the double parking based on the new
                    #double parked vehicle
                    dbl_park_start = df.iloc[event]['a_i']
                    dbl_park_end = df.iloc[event]['d_i']
                    
                    #reset the number of dbl parked vehicle counter for the new window
                    num_dbl_parked = 1
                    
                    #and record the last vehicle double parking window
                    dbl_parked_data = [dbl_park_start, dbl_park_end, dbl_park_end - dbl_park_start, num_dbl_parked]
                    
                    dbl_parked_events.loc[len(dbl_parked_events.index)] = dbl_parked_data
                
                
            #we are not on the last double parking event
            else:
            
                #if the next double parked trucks arrives during the current double parked truck
                if df.iloc[event]['a_i'] <= dbl_park_end:
                    #increment counter
                    num_dbl_parked += 1
                    #if the new double parked truck leaves after the current double parked truck, extend the double parked window
                    if df.iloc[event]['d_i'] > dbl_park_end:
                        dbl_park_end = df.iloc[event]['d_i']
                #if the next double parked truck arrives after the end of the current double parked truck,
                #then there is no further change to the double parked event window and we need to record
                #the data
                elif df.iloc[event]['a_i'] > dbl_park_end:
                    dbl_parked_data = [dbl_park_start, dbl_park_end, dbl_park_end - dbl_park_start, num_dbl_parked]
                    #reset number of dbl parked vehicles in the window
                    num_dbl_parked = 0
                    
                    #add the latest double park event to the bottom of the new net dbl parked dataframe
                    dbl_parked_events.loc[len(dbl_parked_events.index)] = dbl_parked_data
                    
                    #reset the start and end of the double parking based on the new
                    #double parked vehicle
                    dbl_park_start = df.iloc[event]['a_i']
                    dbl_park_end = df.iloc[event]['d_i']
                    
                    #reset the number of dbl parked vehicle counter for the new window
                    num_dbl_parked = 1
      
        
    return dbl_parked_events

    
    
    


#print(dbl_park_events_df_inst_phi0[1][10][3])
#print(dbl_park_events_df_inst_phi2[1][20][3])

net_dbl_park_events_df_inst_FCFS = pd.DataFrame(index = range(0, iterations), columns = [1, 2, 3, 4, 5, 6, 7], dtype = object).applymap(lambda x: [])
#net_dbl_park_events_df_inst_FCFS['Trucks'] = truck_scenarios

net_dbl_park_events_df_inst_phi0 = pd.DataFrame(index = range(0, iterations), columns = [1, 2, 3, 4, 5, 6, 7], dtype = object).applymap(lambda x: [])
#net_dbl_park_events_df_inst_phi0['Trucks'] = truck_scenarios
#range(1, max_parking_spaces +1)

net_dbl_park_events_df_inst_phi1 = pd.DataFrame(index = range(0, iterations), columns = [1, 2, 3, 4, 5, 6, 7], dtype = object).applymap(lambda x: [])
#net_dbl_park_events_df_inst_phi1['Trucks'] = truck_scenarios

net_dbl_park_events_df_inst_phi2 = pd.DataFrame(index = range(0, iterations), columns = [1, 2, 3, 4, 5, 6, 7], dtype = object).applymap(lambda x: [])
#net_dbl_park_events_df_inst_phi2['Trucks'] = truck_scenarios

net_dbl_park_events_df_inst_phi5 = pd.DataFrame(index = range(0, iterations), columns = [1, 2, 3, 4, 5, 6, 7], dtype = object).applymap(lambda x: [])
#net_dbl_park_events_df_inst_phi5['Trucks'] = truck_scenarios

net_dbl_park_events_df_inst_phi10 = pd.DataFrame(index = range(0, iterations), columns = [1, 2, 3, 4, 5, 6, 7], dtype = object).applymap(lambda x: [])
#net_dbl_park_events_df_inst_phi10['Trucks'] = truck_scenarios

net_dbl_park_events_df_inst_phi15 = pd.DataFrame(index = range(0, iterations), columns = [1, 2, 3, 4, 5, 6, 7], dtype = object).applymap(lambda x: [])
#net_dbl_park_events_df_inst_phi15['Trucks'] = truck_scenarios

net_dbl_park_events_df_inst_phi30 = pd.DataFrame(index = range(0, iterations), columns = [1, 2, 3, 4, 5, 6, 7], dtype = object).applymap(lambda x: [])
#net_dbl_park_events_df_inst_phi30['Trucks'] = truck_scenarios

#for c in range(1, max_parking_spaces +1):
for c in [1,2,4,7]:
#for c in range(2, 3):
    
    #n = 0
    
    for i in range(0, iterations):
    #for i in range(12, 13):
        
        print('c: ' + str(c) + ', i: ' + str(i))
        
        
        #net_dbl_park_events_df_inst_FCFS.iloc[i][c].append(net_dbl_park_events(dbl_park_events_df_inst_FCFS_df.iloc[i, c-1])) #needed for buffer
        net_dbl_park_events_df_inst_FCFS.iloc[i][c].append(net_dbl_park_events(dbl_park_events_df_inst_FCFS_df.iloc[i][c])) #for the R2R case
        #net_dbl_park_events_df_inst_phi0.iloc[i][c].append(net_dbl_park_events(dbl_park_events_df_inst_phi0_df.iloc[i, c-1]))
        #net_dbl_park_events_df_inst_phi1.iloc[i][c].append(net_dbl_park_events(dbl_park_events_df_inst_phi1_df.iloc[i, c-1]))
        #net_dbl_park_events_df_inst_phi2.iloc[i][c].append(net_dbl_park_events(dbl_park_events_df_inst_phi2_df.iloc[i, c-1]))
        #net_dbl_park_events_df_inst_phi5.iloc[i][c].append(net_dbl_park_events(dbl_park_events_df_inst_phi5_df.iloc[i, c-1])) #needed for buffer
        net_dbl_park_events_df_inst_phi5.iloc[i][c].append(net_dbl_park_events(dbl_park_events_df_inst_phi5_df.iloc[i][c])) #for the R2R case
        #net_dbl_park_events_df_inst_phi10.iloc[i][c].append(net_dbl_park_events(dbl_park_events_df_inst_phi10_df.iloc[i, c-1]))
        #net_dbl_park_events_df_inst_phi15.iloc[i][c].append(net_dbl_park_events(dbl_park_events_df_inst_phi15_df.iloc[i, c-1]))
        #net_dbl_park_events_df_inst_phi30.iloc[i][c].append(net_dbl_park_events(dbl_park_events_df_inst_phi30_df.iloc[i, c-1]))
       
         

toc = time.time()

runtime = toc-tic
print('runtime: ' + str(runtime))


# save data needed for the queuing model
# import pickle
# with open('pub_Pitt_net_dbl_parking_14_Feb_2024_buffer_15.pkl', 'wb') as file:
#     pickle.dump([net_dbl_park_events_df_inst_FCFS, #needed for buffer
#                   #net_dbl_park_events_df_inst_phi0,
#                   #net_dbl_park_events_df_inst_phi1,
#                   #net_dbl_park_events_df_inst_phi2,
#                   net_dbl_park_events_df_inst_phi5, #needed for buffer
#                   #net_dbl_park_events_df_inst_phi10,
#                   #net_dbl_park_events_df_inst_phi15,
#                   #net_dbl_park_events_df_inst_phi30,
#                   #truck_scenarios,
#                   max_parking_spaces,
#                   iterations],
#                   #max_trucks],
#                   file)


