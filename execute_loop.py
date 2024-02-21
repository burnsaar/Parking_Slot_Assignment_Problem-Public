# -*- coding: utf-8 -*-
"""
Created on Tue Nov  2 11:40:53 2021

@author: Burns
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

iterations = 50 #added
max_parking_spaces = 7 #also known as c #added
max_hr_demand_per_space = 6
max_DVs = max_parking_spaces * max_hr_demand_per_space * 11 #needs to bee changed to 20 when using the Pitt dataset, 11 for Aspen
#also known as n, need to size to the largest possible number of trucks scenario, #added (to get back to original, change 40 to max_parking_spaces)

#set up set of flexibility scenarios
#phi = [0, 1, 2, 5, 10, 15, 30]
phi = [5] #added
#phi = [30]
#schedule buffer between reservations
buffer = 15 #added


#dataframe initialization
n_index_lst_df = pd.DataFrame()
n_index_norm_lst_df = pd.DataFrame()

arrival_dfs_df = pd.DataFrame()
sum_service_df = pd.DataFrame()

dbl_park_FCFS_instance_df = pd.DataFrame()
dbl_park_FCFS_cancelled_inst_df = pd.DataFrame()
dbl_park_events_df_inst_FCFS_df = pd.DataFrame()
legal_park_events_df_inst_FCFS_df = pd.DataFrame()
park_events_df_inst_FCFS_df = pd.DataFrame()

#initialize dataframes based on the contents of phi
for flex in phi:
    if flex == 0:
        dbl_park_Opt_status_inst_phi0_df = pd.DataFrame()
        dbl_park_Opt_inst_phi0_df = pd.DataFrame()
        dbl_park_Diff_inst_phi0_df = pd.DataFrame()
        park_demand_Opt_inst_phi0_df = pd.DataFrame()
        PAPvAP_inst_phi0_df = pd.DataFrame()
        dbl_park_events_df_inst_phi0_df = pd.DataFrame()
        park_events_df_inst_phi0_df = pd.DataFrame()
    elif flex == 1:
        dbl_park_Opt_status_inst_phi1_df = pd.DataFrame()
        dbl_park_Opt_inst_phi1_df = pd.DataFrame()
        dbl_park_Diff_inst_phi1_df = pd.DataFrame()
        park_demand_Opt_inst_phi1_df = pd.DataFrame()
        PAPvAP_inst_phi1_df = pd.DataFrame()
        dbl_park_events_df_inst_phi1_df = pd.DataFrame()
        park_events_df_inst_phi1_df = pd.DataFrame()
    elif flex == 2:
        dbl_park_Opt_status_inst_phi2_df = pd.DataFrame()
        dbl_park_Opt_inst_phi2_df = pd.DataFrame()
        dbl_park_Diff_inst_phi2_df = pd.DataFrame()
        park_demand_Opt_inst_phi2_df = pd.DataFrame()
        PAPvAP_inst_phi2_df = pd.DataFrame()
        dbl_park_events_df_inst_phi2_df = pd.DataFrame()
        park_events_df_inst_phi2_df = pd.DataFrame()
    elif flex == 5:
        dbl_park_Opt_status_inst_phi5_df = pd.DataFrame()
        dbl_park_Opt_inst_phi5_df = pd.DataFrame()
        dbl_park_Diff_inst_phi5_df = pd.DataFrame()
        park_demand_Opt_inst_phi5_df = pd.DataFrame()
        PAPvAP_inst_phi5_df = pd.DataFrame()
        dbl_park_events_df_inst_phi5_df = pd.DataFrame()
        park_events_df_inst_phi5_df = pd.DataFrame()
    elif flex == 10:
        dbl_park_Opt_status_inst_phi10_df = pd.DataFrame()
        dbl_park_Opt_inst_phi10_df = pd.DataFrame()
        dbl_park_Diff_inst_phi10_df = pd.DataFrame()
        park_demand_Opt_inst_phi10_df = pd.DataFrame()
        PAPvAP_inst_phi10_df = pd.DataFrame()
        dbl_park_events_df_inst_phi10_df = pd.DataFrame()
        park_events_df_inst_phi10_df = pd.DataFrame()
    elif flex == 15:
        dbl_park_Opt_status_inst_phi15_df = pd.DataFrame()
        dbl_park_Opt_inst_phi15_df = pd.DataFrame()
        dbl_park_Diff_inst_phi15_df = pd.DataFrame()
        park_demand_Opt_inst_phi15_df = pd.DataFrame()
        PAPvAP_inst_phi15_df = pd.DataFrame()
        dbl_park_events_df_inst_phi15_df = pd.DataFrame()
        park_events_df_inst_phi15_df = pd.DataFrame()
    elif flex == 30:
        dbl_park_Opt_status_inst_phi30_df = pd.DataFrame()
        dbl_park_Opt_inst_phi30_df = pd.DataFrame()
        dbl_park_Diff_inst_phi30_df = pd.DataFrame()
        park_demand_Opt_inst_phi30_df = pd.DataFrame()
        PAPvAP_inst_phi30_df = pd.DataFrame()
        dbl_park_events_df_inst_phi30_df = pd.DataFrame()
        park_events_df_inst_phi30_df = pd.DataFrame()


#track the number of instances of time limit issues
count_tl = 0
#flag for breaking out of the instance for loop when there is a time limit issue
time_limit = 0
#track the number of instances where n_index > n from PAP instance
count_n = 0



#Initialize the n_index dataframe, do this upfront for the purposes of debugging
#Otherwise, the random draw is dependent on all of the other events in the loop
for c_index in range(1, max_parking_spaces +1):


    #initialize the list to store each of the randomly drawn delivery vehicle scenarios, initialize for each new parking space
    n_index_lst = []
    n_index_norm_lst = []
    #Q data
    arrival_dfs = []
    sum_service = [] #used for graphic normalization    

    for i_index in range(1, iterations +1): 
        #print(i_index)
        #if i_index == 24:
            #print('stop')
        
        #next, create the vehicle arrival matrix based on a randomly determined number of deliver vehicles
        
        #what is the lower and upper bound of the number of DVs, which is dependent on the number of parking spaces
        lower_DVs = 1 #this is the lowest possible number of DVs to experience over the day, could go higher, but engineering judgement
        upper_DVs = max_hr_demand_per_space*11*c_index #we want 6 veh/hr*11hr scenario window*the number of parking spaces #added
        
        #draw a random integer between the upper and lower number of DVs to expect
        n_index = np.random.randint(lower_DVs, upper_DVs +1) #+1 becuase it is exclusive of the upper value
        n_index_lst.append(n_index)
        n_index_norm = n_index / 11 / c_index #variable available for storage
        n_index_norm_lst.append(n_index_norm)
        
        #generate a random set of vehicle arrival requests based on the number of
        #delivery vehicles in the scenario
        if dataset == 'Aspen':
            Q, sum_service = gen.gen_veh_arrivals(n_index, end, buffer)
        elif dataset == 'Pitt':
            Q, sum_service = gen_Pitt.gen_Pitt_arrivals(n_index, end, buffer)
            
        arrival_dfs.append(Q)


    #add the populated lists of data for the current parking space to the initialized dataframes
    n_index_lst_df[c_index] = n_index_lst
    n_index_norm_lst_df[c_index] = n_index_norm_lst
    #Q data
    arrival_dfs_df[c_index] = arrival_dfs
    sum_service_df[c_index] = sum_service #used for graphic normalization





#set the number of parking spaces
#for c_index in range(1, max_parking_spaces +1):
for c_index in [1,2,4,7]: #used for the R&R cases
#for c_index in range(2,3):
    
    #FCFS statistics
    dbl_park_FCFS_instance = []
    dbl_park_FCFS_cancelled_inst = []
    dbl_park_events_df_inst_FCFS = []
    legal_park_events_df_inst_FCFS = []
    park_events_df_inst_FCFS = []
    #Flexibility statistics
    dbl_park_Opt_status_inst_phi0 = []
    dbl_park_Opt_status_inst_phi1 = []
    dbl_park_Opt_status_inst_phi2 = []
    dbl_park_Opt_status_inst_phi5 = []
    dbl_park_Opt_status_inst_phi10 = []
    dbl_park_Opt_status_inst_phi15 = []
    dbl_park_Opt_status_inst_phi30 = []
    
    PAPvAP_inst_phi0 = []
    PAPvAP_inst_phi1 = []
    PAPvAP_inst_phi2 = []
    PAPvAP_inst_phi5 = []
    PAPvAP_inst_phi10 = []
    PAPvAP_inst_phi15 = []
    PAPvAP_inst_phi30 = []
    
    dbl_park_Opt_inst_phi0 = []
    dbl_park_Diff_inst_phi0 = []
    park_demand_Opt_inst_phi0 = []
    dbl_park_events_df_inst_phi0 = []
    park_events_df_inst_phi0 = []
    
    dbl_park_Opt_inst_phi1 = []
    dbl_park_Diff_inst_phi1 = []
    park_demand_Opt_inst_phi1 = []
    dbl_park_events_df_inst_phi1 = []
    park_events_df_inst_phi1 = []
    
    dbl_park_Opt_inst_phi2 = []
    dbl_park_Diff_inst_phi2 = []
    park_demand_Opt_inst_phi2 = []
    dbl_park_events_df_inst_phi2 = []
    park_events_df_inst_phi2 = []
    
    dbl_park_Opt_inst_phi5 = []
    dbl_park_Diff_inst_phi5 = []
    park_demand_Opt_inst_phi5 = []
    dbl_park_events_df_inst_phi5 = []
    park_events_df_inst_phi5 = []
    
    dbl_park_Opt_inst_phi10 = []
    dbl_park_Diff_inst_phi10 = []
    park_demand_Opt_inst_phi10 = []
    dbl_park_events_df_inst_phi10 = []
    park_events_df_inst_phi10 = []
    
    dbl_park_Opt_inst_phi15 = []
    dbl_park_Diff_inst_phi15 = []
    park_demand_Opt_inst_phi15 = []
    dbl_park_events_df_inst_phi15 = []
    park_events_df_inst_phi15 = []
    
    dbl_park_Opt_inst_phi30 = []
    dbl_park_Diff_inst_phi30 = []
    park_demand_Opt_inst_phi30 = []
    dbl_park_events_df_inst_phi30 = []
    park_events_df_inst_phi30 = []
    

    
    #set the vehicle arrival matrix
    #for i_index in range(22,23):
    for i_index in range(1, iterations +1):
        #if (i_index == 4) and (c_index == 2):
            #print('stop')
        
        
        Q = arrival_dfs_df.iloc[i_index-1, c_index-1]
        
        
        #run the FCFS calcuations
        #dbl_park_seq, cancelled, count_cancelled = seq_curb_old.seq_curb(c_index, n_index, Q_sub, end)
        dbl_park_seq, dbl_parked_events, legal_parked_events, park_events_FCFS = seq_curb.seq_curb(c_index, Q, end)
        #print('dbl parking = ' + str(dbl_park_seq))
        
        #record the number of double parking minutes per day
        dbl_park_FCFS_instance.append(dbl_park_seq)
        
        #record the number of double parked vehicles
        dbl_park_FCFS_cancelled_inst.append(len(dbl_parked_events))

        #record the schedule of dbl parking events
        dbl_park_events_df_inst_FCFS.append(dbl_parked_events)

        #record the schedule of legal parking events
        legal_park_events_df_inst_FCFS.append(legal_parked_events)
        
        #record the full parking event schedule
        park_events_df_inst_FCFS.append(park_events_FCFS)
        
        timed_out_flag = False 


        #loop on phi/flexibility
        for flex in phi:
            
            n_index = len(Q)
            #run the optimal calculations
            print('c = ' + str(c_index) + ' ' + 'i = ' + str(i_index) + ' ' + 'n = ' + str(n_index) + ' ' + 'phi = ' + str(flex))


            #run PAP as long as possible before it times out, then transition to the AP
            if timed_out_flag == False:
                
                #Let's just prevent the case that for the first level of flex
                #there isn't a warm start at risk of not being able to provide
                #a feasible starting solution
                if flex == 0:
                    t_initialize = [None]
                    x_initialize = [None] #* n_index
                    
                t_initialize = [None] #added for buffer case
                x_initialize = [None] #added for buffer case

                
                runtime, status, obj, count_b_i, end_state_t_i, end_state_x_ij, dbl_park_events, park_events \
                    = MOD_flex.MOD_flex(flex, n_index, c_index, Q, buffer, start, end, t_initialize, x_initialize)
                t_initialize = end_state_t_i
                x_initialize = end_state_x_ij
                
                #align PAP outputs with AP outputs for data storage
                dbl_park_Opt = obj
                park_demand = sum(Q['s_i'])
                PAPvAP = 'PAP'
            
            
                #if the PAP times out, set the flag as true
                if status == 9:
                    timed_out_flag = True
                    
                    #execute the AP
                    x_initialize = [None] #* n_index
            
                    bids = genBids.genBids(n_index, end, Q, flex)

                    runtime, status, obj, dbl_park_Opt, park_demand, end_state_x_i_j, dbl_park_events, park_events = AP.AP(n_index, end, Q, c_index, bids, flex, buffer, x_initialize)
            
                    x_initialize = end_state_x_i_j
                    
                    PAPvAP = 'AP'

            elif timed_out_flag == True:
                
                
                bids = genBids.genBids(n_index, end, Q, flex)
                                    
                runtime, status, obj, dbl_park_Opt, park_demand, end_state_x_i_j, dbl_park_events, park_events = AP.AP(n_index, end, Q, c_index, bids, flex, buffer, x_initialize)
                
                x_initialize = end_state_x_i_j
                
                PAPvAP = 'AP'



            #record the optimal status of current scenario and which algorithm was used
            if flex == 0:
                dbl_park_Opt_status_inst_phi0.append(status)
                PAPvAP_inst_phi0.append(PAPvAP)
            elif flex == 1:
                dbl_park_Opt_status_inst_phi1.append(status)
                PAPvAP_inst_phi1.append(PAPvAP)
            elif flex == 2:
                dbl_park_Opt_status_inst_phi2.append(status)
                PAPvAP_inst_phi2.append(PAPvAP)
            elif flex == 5:
                dbl_park_Opt_status_inst_phi5.append(status)
                PAPvAP_inst_phi5.append(PAPvAP)
            elif flex == 10:
                dbl_park_Opt_status_inst_phi10.append(status)
                PAPvAP_inst_phi10.append(PAPvAP)
            elif flex == 15:
                dbl_park_Opt_status_inst_phi15.append(status)
                PAPvAP_inst_phi15.append(PAPvAP)
            elif flex == 30:
                dbl_park_Opt_status_inst_phi30.append(status)
                PAPvAP_inst_phi30.append(PAPvAP)

                    
            #if the current iteration is time limited, break out of the flexibility loop
            #loop not necessary for PAP status 9 becuase the new status is followed up
            #with by the AP which is usually not time limited
            if status == 9:
                time_limit = 1
                count_tl += 1
                phi_flag = flex
                break

            if flex == 0:
                #store the double parking minutes for this instance and flex
                dbl_park_Opt_inst_phi0.append(dbl_park_Opt)
                #store the difference between double parking minutes and FCFS
                dbl_park_Diff_inst_phi0.append(dbl_park_seq - dbl_park_Opt)
                #store the total demanded service time for Q_sub
                park_demand_Opt_inst_phi0.append(park_demand)
                #store the dfs of double parking events from each optimization
                dbl_park_events_df_inst_phi0.append(dbl_park_events)
                park_events_df_inst_phi0.append(park_events)
            elif flex == 1:
                dbl_park_Opt_inst_phi1.append(dbl_park_Opt)
                dbl_park_Diff_inst_phi1.append(dbl_park_seq - dbl_park_Opt)
                park_demand_Opt_inst_phi1.append(park_demand)
                dbl_park_events_df_inst_phi1.append(dbl_park_events)
                park_events_df_inst_phi1.append(park_events)
            elif flex == 2:
                dbl_park_Opt_inst_phi2.append(dbl_park_Opt)
                dbl_park_Diff_inst_phi2.append(dbl_park_seq - dbl_park_Opt)
                park_demand_Opt_inst_phi2.append(park_demand)
                dbl_park_events_df_inst_phi2.append(dbl_park_events)
                park_events_df_inst_phi2.append(park_events)
            elif flex == 5:
                dbl_park_Opt_inst_phi5.append(dbl_park_Opt)
                dbl_park_Diff_inst_phi5.append(dbl_park_seq - dbl_park_Opt)
                park_demand_Opt_inst_phi5.append(park_demand)
                dbl_park_events_df_inst_phi5.append(dbl_park_events)
                park_events_df_inst_phi5.append(park_events)
            elif flex == 10:
                dbl_park_Opt_inst_phi10.append(dbl_park_Opt)
                dbl_park_Diff_inst_phi10.append(dbl_park_seq - dbl_park_Opt)
                park_demand_Opt_inst_phi10.append(park_demand)
                dbl_park_events_df_inst_phi10.append(dbl_park_events)
                park_events_df_inst_phi10.append(park_events)
            elif flex == 15:
                dbl_park_Opt_inst_phi15.append(dbl_park_Opt)
                dbl_park_Diff_inst_phi15.append(dbl_park_seq - dbl_park_Opt)
                park_demand_Opt_inst_phi15.append(park_demand)
                dbl_park_events_df_inst_phi15.append(dbl_park_events)
                park_events_df_inst_phi15.append(park_events)
            elif flex == 30:
                dbl_park_Opt_inst_phi30.append(dbl_park_Opt)
                dbl_park_Diff_inst_phi30.append(dbl_park_seq - dbl_park_Opt)
                park_demand_Opt_inst_phi30.append(park_demand)
                dbl_park_events_df_inst_phi30.append(dbl_park_events)
                park_events_df_inst_phi30.append(park_events)

    
    #FCFS statistics
    dbl_park_FCFS_instance_df[c_index] = dbl_park_FCFS_instance
    dbl_park_FCFS_cancelled_inst_df[c_index] = dbl_park_FCFS_cancelled_inst
    dbl_park_events_df_inst_FCFS_df[c_index] = dbl_park_events_df_inst_FCFS
    legal_park_events_df_inst_FCFS_df[c_index] = legal_park_events_df_inst_FCFS
    park_events_df_inst_FCFS_df[c_index] = park_events_df_inst_FCFS
    #Flexibility statistics
    #dbl_park_Opt_status_inst_phi0_df[c_index] = dbl_park_Opt_status_inst_phi0
    #dbl_park_Opt_status_inst_phi1_df[c_index] = dbl_park_Opt_status_inst_phi1
    #dbl_park_Opt_status_inst_phi2_df[c_index] = dbl_park_Opt_status_inst_phi2
    dbl_park_Opt_status_inst_phi5_df[c_index] = dbl_park_Opt_status_inst_phi5
    #dbl_park_Opt_status_inst_phi10_df[c_index] = dbl_park_Opt_status_inst_phi10
    #dbl_park_Opt_status_inst_phi15_df[c_index] = dbl_park_Opt_status_inst_phi15
    #dbl_park_Opt_status_inst_phi30_df[c_index] = dbl_park_Opt_status_inst_phi30
    
    #PAPvAP_inst_phi0_df[c_index] = PAPvAP_inst_phi0
    #PAPvAP_inst_phi1_df[c_index] = PAPvAP_inst_phi1
    #PAPvAP_inst_phi2_df[c_index] = PAPvAP_inst_phi2
    PAPvAP_inst_phi5_df[c_index] = PAPvAP_inst_phi5
    #PAPvAP_inst_phi10_df[c_index] = PAPvAP_inst_phi10
    #PAPvAP_inst_phi15_df[c_index] = PAPvAP_inst_phi15
    #PAPvAP_inst_phi30_df[c_index] = PAPvAP_inst_phi30
    
    # dbl_park_Opt_inst_phi0_df[c_index] = dbl_park_Opt_inst_phi0
    # dbl_park_Diff_inst_phi0_df[c_index] = dbl_park_Diff_inst_phi0
    # park_demand_Opt_inst_phi0_df[c_index] = park_demand_Opt_inst_phi0
    # dbl_park_events_df_inst_phi0_df[c_index] = dbl_park_events_df_inst_phi0
    # park_events_df_inst_phi0_df[c_index] = park_events_df_inst_phi0
    
    # dbl_park_Opt_inst_phi1_df[c_index] = dbl_park_Opt_inst_phi1
    # dbl_park_Diff_inst_phi1_df[c_index] = dbl_park_Diff_inst_phi1
    # park_demand_Opt_inst_phi1_df[c_index] = park_demand_Opt_inst_phi1
    # dbl_park_events_df_inst_phi1_df[c_index] = dbl_park_events_df_inst_phi1
    # park_events_df_inst_phi1_df[c_index] = park_events_df_inst_phi1
    
    # dbl_park_Opt_inst_phi2_df[c_index] = dbl_park_Opt_inst_phi2
    # dbl_park_Diff_inst_phi2_df[c_index] = dbl_park_Diff_inst_phi2
    # park_demand_Opt_inst_phi2_df[c_index] = park_demand_Opt_inst_phi2
    # dbl_park_events_df_inst_phi2_df[c_index] = dbl_park_events_df_inst_phi2
    # park_events_df_inst_phi2_df[c_index] = park_events_df_inst_phi2
    
    dbl_park_Opt_inst_phi5_df[c_index] = dbl_park_Opt_inst_phi5
    dbl_park_Diff_inst_phi5_df[c_index] = dbl_park_Diff_inst_phi5
    park_demand_Opt_inst_phi5_df[c_index] = park_demand_Opt_inst_phi5
    dbl_park_events_df_inst_phi5_df[c_index] = dbl_park_events_df_inst_phi5
    park_events_df_inst_phi5_df[c_index] = park_events_df_inst_phi5
    
    # dbl_park_Opt_inst_phi10_df[c_index] = dbl_park_Opt_inst_phi10
    # dbl_park_Diff_inst_phi10_df[c_index] = dbl_park_Diff_inst_phi10
    # park_demand_Opt_inst_phi10_df[c_index] = park_demand_Opt_inst_phi10
    # dbl_park_events_df_inst_phi10_df[c_index] = dbl_park_events_df_inst_phi10
    # park_events_df_inst_phi10_df[c_index] = park_events_df_inst_phi10
    
    # dbl_park_Opt_inst_phi15_df[c_index] = dbl_park_Opt_inst_phi15
    # dbl_park_Diff_inst_phi15_df[c_index] = dbl_park_Diff_inst_phi15
    # park_demand_Opt_inst_phi15_df[c_index] = park_demand_Opt_inst_phi15
    # dbl_park_events_df_inst_phi15_df[c_index] = dbl_park_events_df_inst_phi15
    # park_events_df_inst_phi15_df[c_index] = park_events_df_inst_phi15
    
    # dbl_park_Opt_inst_phi30_df[c_index] = dbl_park_Opt_inst_phi30
    # dbl_park_Diff_inst_phi30_df[c_index] = dbl_park_Diff_inst_phi30
    # park_demand_Opt_inst_phi30_df[c_index] = park_demand_Opt_inst_phi30
    # dbl_park_events_df_inst_phi30_df[c_index] = dbl_park_events_df_inst_phi30
    # park_events_df_inst_phi30_df[c_index] = park_events_df_inst_phi30
    









toc = time.time()

runtime = toc-tic
print('runtime: ' + str(runtime))


#save data from the run
import pickle
with open('pub_Pitt_run_for_record_18_Jan_2024_buffer_15.pkl', 'wb') as file:
    pickle.dump([n_index_lst_df,
                  n_index_norm_lst_df,
                  arrival_dfs_df,
                  sum_service_df,
                  dbl_park_FCFS_instance_df,
                  dbl_park_FCFS_cancelled_inst_df,
                  dbl_park_events_df_inst_FCFS_df,
                  legal_park_events_df_inst_FCFS_df,
                  park_events_df_inst_FCFS_df,
                  #dbl_park_Opt_status_inst_phi0_df,
                  #dbl_park_Opt_status_inst_phi1_df,
                  #dbl_park_Opt_status_inst_phi2_df,
                  dbl_park_Opt_status_inst_phi5_df,
                  #dbl_park_Opt_status_inst_phi10_df,
                  #dbl_park_Opt_status_inst_phi15_df,
                  #dbl_park_Opt_status_inst_phi30_df,
                  #PAPvAP_inst_phi0_df,
                  #PAPvAP_inst_phi1_df,
                  #PAPvAP_inst_phi2_df,
                  PAPvAP_inst_phi5_df,
                  #PAPvAP_inst_phi10_df,
                  #PAPvAP_inst_phi15_df,
                  #PAPvAP_inst_phi30_df,
                  #dbl_park_Opt_inst_phi0_df,
                  #dbl_park_Opt_inst_phi1_df,
                  #dbl_park_Opt_inst_phi2_df,
                  dbl_park_Opt_inst_phi5_df,
                  #dbl_park_Opt_inst_phi10_df,
                  #dbl_park_Opt_inst_phi15_df,
                  #dbl_park_Opt_inst_phi30_df,
                  #dbl_park_Diff_inst_phi0_df,
                  #dbl_park_Diff_inst_phi1_df,
                  #dbl_park_Diff_inst_phi2_df,
                  dbl_park_Diff_inst_phi5_df,
                  #dbl_park_Diff_inst_phi10_df,
                  #dbl_park_Diff_inst_phi15_df,
                  #dbl_park_Diff_inst_phi30_df,
                  #park_demand_Opt_inst_phi0_df,
                  #park_demand_Opt_inst_phi1_df,
                  #park_demand_Opt_inst_phi2_df,
                  park_demand_Opt_inst_phi5_df,
                  #park_demand_Opt_inst_phi10_df,
                  #park_demand_Opt_inst_phi15_df,
                  #park_demand_Opt_inst_phi30_df,
                  #dbl_park_events_df_inst_phi0_df,
                  #dbl_park_events_df_inst_phi1_df,
                  #dbl_park_events_df_inst_phi2_df,
                  dbl_park_events_df_inst_phi5_df,
                  #dbl_park_events_df_inst_phi10_df,
                  #dbl_park_events_df_inst_phi15_df,
                  #dbl_park_events_df_inst_phi30_df,
                  #park_events_df_inst_phi0_df,
                  #park_events_df_inst_phi1_df,
                  #park_events_df_inst_phi2_df,
                  park_events_df_inst_phi5_df,
                  #park_events_df_inst_phi10_df,
                  #park_events_df_inst_phi15_df,
                  #park_events_df_inst_phi30_df,
                  runtime,
                  buffer,
                  end,
                  iterations,
                  max_parking_spaces,
                  phi],
                file)
