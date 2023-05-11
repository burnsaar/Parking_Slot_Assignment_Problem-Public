# -*- coding: utf-8 -*-
"""
Created on Mon Jun 20 19:26:44 2022

@author: Aaron
"""

#******************************************************************************
#This workflow is for processing phiX or optimal controlled schedules only, not
#the FCFS schedule



import numpy as np
import pandas as pd
import pickle
import time

tic = time.time()


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
    
    
    
#establish the current schedule to update        
#OG_shift_sched = park_events_df_inst_phi5_shifted.iloc[50, 7][0]
#OG_shift_sched = park_events_df_inst_phi5_shifted.iloc[22, 2][0] #case where a truck loses a reservation, and another dbl parked DV takes its spot
#OG_shift_sched = park_events_df_inst_phi5_shifted.iloc[62, 4][0]

#OG_shift_sched = park_events_df_inst_phi5_shifted.iloc[66][1][0]

dbl_park_events_df_inst_phi5_df = pd.DataFrame() 
park_events_df_inst_phi5_df = pd.DataFrame() 

        
#end = 660
#buffer = 5  #set to zero for now, might still be able to debug, but really should be set to 5
max_wait = 5
        



late_no_starts_1 = []
late_no_starts_more_1 = []
early_no_starts_1 = []
early_no_starts_more_1 = []
change_sum_dbl_parking = []
change_legal_and_dbl = []


#for c in range(1, max_parking_spaces +1):
for c in range(7, 8):
    
    dbl_park_events_df_inst_phi5_lst = []
    park_events_df_inst_phi5_lst = []
    
    for i in range(76, 77):    
    #for i in range(0, iterations):
        print('c =', c, 'i =', i)
        
        OG_shift_sched = park_events_df_inst_phi5_shifted.iloc[i, c][0] 



        #create a full event list from the schedule, e.g. breakout the schedule into arrival and departure events
        Events = pd.DataFrame(columns = ['Truck', 't_i', 'Event Type', 's_i', 'd_i', 'a_i_OG', 'd_i_OG', 'Park Type OG', 'Park Type New', 'Updated Time', 'Lost Reservation'])
        
        #take each row in the parking schedule and breakout two events, one for the arrival and the other for the departure
        for row in range(0, len(OG_shift_sched)):
            data_arrival = []
            data_arrival.append(OG_shift_sched['Truck'][row])
            data_arrival.append(OG_shift_sched['t_i'][row])
            data_arrival.append('Arrival')
            data_arrival.append(OG_shift_sched['s_i'][row])
            data_arrival.append(OG_shift_sched['d_i'][row])
            data_arrival.append(OG_shift_sched['a_i_OG'][row])
            data_arrival.append(OG_shift_sched['d_i_OG'][row])
            data_arrival.append(OG_shift_sched['Park Type'][row])
            data_arrival.append('TBD')
            data_arrival.append(None)
            data_arrival.append(None)
            Events.loc[len(Events)] = data_arrival
            
            data_depart = []
            data_depart.append(OG_shift_sched['Truck'][row])
            data_depart.append(OG_shift_sched['d_i'][row])
            data_depart.append('Departure')
            data_depart.append(OG_shift_sched['s_i'][row])
            data_depart.append(OG_shift_sched['d_i'][row])
            data_depart.append(OG_shift_sched['a_i_OG'][row])
            data_depart.append(OG_shift_sched['d_i_OG'][row])
            data_depart.append(OG_shift_sched['Park Type'][row])
            data_depart.append('TBD')
            data_depart.append(None)
            data_depart.append(None)
            Events.loc[len(Events)] = data_depart
            
        #reset the new schedule based on ascending values of t_i
        Events = Events.sort_values(['t_i', 'Event Type'], ascending = [True, False])
        Events.reset_index(level = 0, drop = True, inplace = True)
        
        OG_Events = Events
            
        #print(OG_shift_sched)
        #print(Events)    
            
        #need a dataframe to track the dbl parking events while a vehicle is waiting for a possible start
        #e.g. the vehicle arrived super early and has to wait a couple minutes of an available space or
        #the vehicle arrived late and may have to wait for an available parking space.  These are likely short
        #duration dbl parking events, but they should be added to the full event schedule at the end of processing
        Events_dbl_park_wait_poss_start = pd.DataFrame(columns = ['Truck', 't_i', 'Event Type', 's_i', 'd_i', 'a_i_OG', 'd_i_OG', 'Park Type OG', 'Park Type New', 'Updated Time', 'Lost Reservation'])
        
        
        
        
        #reprocess the selected shifted schedule
        #c = 2
        parking_spaces_available = c
        
        
        
        r = 0 #basically the row counter to help select individual events from the Events schedule
        
        #iterate through the list of events
        while r != len(Events):
            print(r)
            if r == 148:
                print('stop')
            #if r == 273:
             #   print('stop')
            #if r == 343:
             #   print('stop')
        #for r in range(0, len(Events)):
            
            #establish the current event
            current_event = Events.iloc[r]
            
            
            #check all legal parked arrival events against the current event time to see if any are beyond
            #the buffer and therefore would need to be set as losing their reservation and 
            #dbl parking
            missed_arrivals = np.where( (Events['Event Type'] == 'Arrival') & 
                                       (Events['Park Type OG'] == 'Legal Park') &
                                       (Events['Park Type New'] == 'TBD') & 
                                       ( (current_event['t_i'] - Events['a_i_OG']) > 5) )
            
            for w in range(0, len(missed_arrivals[0])):
                Events.loc[missed_arrivals[0][w], 'Park Type OG'] = 'Dbl Park'
                Events.at[missed_arrivals[0][w], 'Park Type OG'] = 'Dbl Park'
                Events.at[missed_arrivals[0][w], 'Lost Reservation'] = 'Yes'
                #find the corresponding delivery vehicle departure event as well
                DV = Events.loc[missed_arrivals[0][w], 'Truck']
                DV_idx = np.where((Events['Truck'] == DV) & (Events['Event Type'] == 'Departure'))
                Events.loc[DV_idx[0], 'Park Type OG'] = 'Dbl Park'
                Events.at[DV_idx[0][0], 'Park Type OG'] = 'Dbl Park'
            
            #re-establish the current event, captures the case where the current event 
            #actually arrived greater than 5 minutes late and should now be handled as a double parked
            #vehicle
            current_event = Events.iloc[r]
            
            
            
            #is the current event an arrival?
            if current_event['Event Type'] == 'Arrival':
                
                #is the current event a legal parking event?
                if current_event['Park Type OG'] == 'Legal Park':
                
                    #has the current event already been processed?
                    if current_event['Park Type New'] == 'TBD':
                        
                        #is the current arrival late?
                        if current_event['t_i'] > current_event['a_i_OG']:
                            
                            #what is the window of time over which we need to consider upcoming vehicle events
                            window_start = current_event['t_i']
                            window_end = current_event['d_i_OG'] + buffer
                            
                            #what are the upcoming events?
                            upcoming = pd.DataFrame(columns = ['Truck', 't_i', 'Event Type', 's_i', 'd_i', 'a_i_OG', 'd_i_OG', 'Park Type OG', 'Park Type New', 'Updated Time'])
                            
                            #consider upcoming original reservations that have not been processed yet within the window
                            df = Events.loc[np.where((Events['Truck'] != current_event['Truck']) &
                                                (Events['Park Type OG'] == 'Legal Park') & 
                                                (Events['Event Type'] == 'Arrival') &
                                                (Events['Park Type New'] == 'TBD') &
                                                (Events['a_i_OG'] >= window_start - buffer) & #someone else could be arriving late, but was originally schedule to arrive before the current event time step
                                                (Events['a_i_OG'] < window_end)
                                                )]
                            upcoming = pd.concat([upcoming, df])
                            #consider scheduled, but unseen departures
                            df = Events.loc[np.where((Events['Truck'] != current_event['Truck']) &
                                                (Events['Park Type OG'] == 'Legal Park') & 
                                                (Events['Event Type'] == 'Departure') &
                                                (Events['Park Type New'] == 'TBD') &
                                                (Events['d_i_OG'] >= window_start - buffer) &
                                                (Events['d_i_OG'] < window_end)
                                                )]
                            upcoming = pd.concat([upcoming, df])
                            #consider new departures switched from dbl to legal parking
                            df = Events.loc[np.where((Events['Park Type OG'] == 'Dbl Park') & 
                                                (Events['Event Type'] == 'Departure') &
                                                (Events['Park Type New'] == 'Legal Park') &
                                                (Events['t_i'] >= window_start) &
                                                (Events['t_i'] < window_end)
                                                )]
                            upcoming = pd.concat([upcoming, df])
                            #consider scheduled, but shifted arrivals
                            df = Events.loc[np.where((Events['Park Type OG'] == 'Legal Park') & 
                                                (Events['Event Type'] == 'Arrival') &
                                                (Events['Park Type New'] == 'Legal Park') &
                                                (Events['Updated Time'] > window_start) & #only want to consider already processed arrivals that are > window start, b/c '=' window start is not technically upcoming,
                                                #had an issue where two vehicles arrived at t = 0, incorrectly double counted one of the arrivals
                                                (Events['Updated Time'] < window_end)
                                                )]
                            upcoming = pd.concat([upcoming, df])
                            #consider scheduled, but shifted departures
                            df = Events.loc[np.where((Events['Park Type OG'] == 'Legal Park') & 
                                                (Events['Event Type'] == 'Departure') &
                                                (Events['Park Type New'] == 'Legal Park') &
                                                (Events['Updated Time'] >= window_start) &
                                                (Events['Updated Time'] < window_end)
                                                )]
                            upcoming = pd.concat([upcoming, df])
                            
                            upcoming.reset_index(drop = True, inplace = True)
                            
                            
                            # #upcoming refinement
                            # #for a scheduled, but unseen arrival, if the arrival OG is less
                            # #that the current time, assume the worst, make the arrival OG
                            # #equal to arrival OG + buffer
                            # #but, added a section that considers if we should be full worst case or not based on s_i of current vehicle versus the unseen late vehicle
                            # for row in range(0, len(upcoming)):
                            #     #is this a legal parked arrival that has not yet been seen?
                            #     if (upcoming.iloc[row]['Event Type'] == 'Arrival') and (upcoming.iloc[row]['Park Type OG'] == 'Legal Park') and (upcoming.iloc[row]['Park Type New'] == 'TBD'):
                            #         #was the planned arrival time before the current event time?
                            #         if upcoming.iloc[row]['a_i_OG'] < current_event['t_i']:
                                        
                            #             #does the unseen late arrival have a larger s_i than the current arrival?
                            #             #if so, be conservative and try to save the unseen late arrival by adding the 
                            #             #full buffer to the a_i_OG and d_i_OG
                            #             if upcoming.iloc[row]['s_i'] > current_event['s_i']:
                                            
                            #                 #if so, then make the expected arrival the worst case, add to the end of the buffer from the OG arrival time
                            #                 upcoming.loc[row, 'a_i_OG'] = upcoming.iloc[row]['a_i_OG'] + buffer
                            #                 upcoming.loc[row, 'd_i_OG'] = upcoming.iloc[row]['d_i_OG'] + buffer
                                            
                            #                 #need to update to the worst case departure time as well
                            #                 #what truck is currently arriving?
                            #                 DV = upcoming.iloc[row]['Truck']
                            #                 #what is the index in upcoming of the DV departure event
                            #                 DV_idx = np.where((upcoming['Truck'] == DV) & (upcoming['Event Type'] == 'Departure'))
                            #                 upcoming.loc[DV_idx[0], 'd_i_OG'] = upcoming.iloc[DV_idx]['d_i_OG'] + buffer
                            #                 upcoming.loc[DV_idx[0], 'a_i_OG'] = upcoming.iloc[DV_idx]['a_i_OG'] + buffer
                                            
                            #             else:
                            #                 #if the s_i of the unseen late arrival is less than the current arrival
                            #                 #we want to try to schedule the current arrival, so do not put in the worst case
                            #                 #scenario, instead just assign the expected arrival time of the unseen arrival to
                            #                 #the current event time
                            #                 upcoming.loc[row, 'a_i_OG'] = current_event['t_i']
                            #                 upcoming.loc[row, 'd_i_OG'] = current_event['t_i'] + upcoming.iloc[row]['s_i']
                                            
                            #                 #need to update to the worst case departure time as well
                            #                 #what truck is currently arriving?
                            #                 DV = upcoming.iloc[row]['Truck']
                            #                 #what is the index in upcoming of the DV departure event
                            #                 DV_idx = np.where((upcoming['Truck'] == DV) & (upcoming['Event Type'] == 'Departure'))
                            #                 upcoming.loc[DV_idx[0], 'd_i_OG'] = current_event['t_i'] + upcoming.iloc[row]['s_i']
                            #                 upcoming.loc[DV_idx[0], 'a_i_OG'] = current_event['t_i']
                                            
                            #testing new upcoming refinement logic
                            for row in range(0, len(upcoming)):
                                #is this a legal parked arrival that has not yet been seen?
                                if (upcoming.iloc[row]['Event Type'] == 'Arrival') and (upcoming.iloc[row]['Park Type OG'] == 'Legal Park') and (upcoming.iloc[row]['Park Type New'] == 'TBD'):
                                    #was the planned arrival time before the current event time?
                                    if upcoming.iloc[row]['a_i_OG'] < current_event['t_i']:
                                    
                                        #if so, then make the expected arrival the worst case e.g. truck arrives at current time
                                        #and make the departure the worst case e.g. hold all the way through d_i_OG + buffer
                                        upcoming.loc[row, 'a_i_OG'] = current_event['t_i']
                                        upcoming.loc[row, 'd_i_OG'] = upcoming.iloc[row]['d_i_OG'] + buffer
                                        
                                        #need to update to the worst case departure time as well
                                        #what truck is currently arriving?
                                        DV = upcoming.iloc[row]['Truck']
                                        #what is the index in upcoming of the DV departure event
                                        DV_idx = np.where((upcoming['Truck'] == DV) & (upcoming['Event Type'] == 'Departure'))
                                        upcoming.loc[DV_idx[0], 'a_i_OG'] = current_event['t_i']
                                        upcoming.loc[DV_idx[0], 'd_i_OG'] = upcoming.iloc[DV_idx]['d_i_OG'] + buffer
                                        
                                        
                            #what does the final expected upcoming schedule look like?
                            #need to step through the upcoming sched and pull the relevant
                            #expected future time for each case, e.g. unseen arrival legal park, pull the a_i_OG
                            #post above worst case refinement, or for seen arrival legal park,
                            #pull the t_i from upcoming
                            upcoming.insert(7, 'Expected Time', None)
                            for row in range(0, len(upcoming)):
                                #unseen, legal park, arrival
                                if (upcoming.iloc[row]['Event Type'] == 'Arrival') & (upcoming.iloc[row]['Park Type OG'] == 'Legal Park') & (upcoming.iloc[row]['Park Type New'] == 'TBD'):
                                    upcoming.loc[row, 'Expected Time'] = upcoming.iloc[row]['a_i_OG']
                                #unseen, legal park, departure
                                if (upcoming.iloc[row]['Event Type'] == 'Departure') & (upcoming.iloc[row]['Park Type OG'] == 'Legal Park') & (upcoming.iloc[row]['Park Type New'] == 'TBD'):
                                    upcoming.loc[row, 'Expected Time'] = upcoming.iloc[row]['d_i_OG']
                                #seen, dbl park to legal park departure
                                if (upcoming.iloc[row]['Event Type'] == 'Departure') & (upcoming.iloc[row]['Park Type OG'] == 'Dbl Park') & (upcoming.iloc[row]['Park Type New'] == 'Legal Park'):
                                    upcoming.loc[row, 'Expected Time'] = upcoming.iloc[row]['Updated Time']
                                #seen, legal park, arrival
                                if (upcoming.iloc[row]['Event Type'] == 'Arrival') & (upcoming.iloc[row]['Park Type OG'] == 'Legal Park') & (upcoming.iloc[row]['Park Type New'] == 'Legal Park'):
                                    upcoming.loc[row, 'Expected Time'] = upcoming.iloc[row]['Updated Time']
                                #seen, legal park, departure
                                if (upcoming.iloc[row]['Event Type'] == 'Departure') & (upcoming.iloc[row]['Park Type OG'] == 'Legal Park') & (upcoming.iloc[row]['Park Type New'] == 'Legal Park'):
                                    upcoming.loc[row, 'Expected Time'] = upcoming.iloc[row]['Updated Time']
                            
                            upcoming = upcoming.sort_values(by = ['Expected Time', 'Event Type'], ascending = [True, False], ignore_index = True)  
        
        
                            #now we can start counting out the future parking availability
                            parking_space_sched = []
                            parking_space_sched.append(parking_spaces_available)
                            parking_counter = parking_spaces_available
                            for row in range(0, len(upcoming)):
                                if upcoming.iloc[row]['Event Type'] == 'Arrival':
                                    if parking_counter != 0:
                                        parking_counter -= 1
                                        parking_space_sched.append(parking_counter)
                                    else:
                                        parking_space_sched.append(parking_counter)
                                        print('late counter negative issue')
                                elif upcoming.iloc[row]['Event Type'] == 'Departure':
                                    if parking_counter != c:
                                        parking_counter += 1
                                        parking_space_sched.append(parking_counter)
                                    elif parking_counter == c:
                                        print('late counter issue')
                                        
                                        
                            #are there any zeros in the upcoming parking space schedule?
                            #which would mean that there may not be space for the current truck
                            num_zeros = parking_space_sched.count(0)
                            if num_zeros == 0: #no issues parking the current delivery vehicle at the current event time, update the events schedule
                                #first check to see if the randomly shifted t_i + service duration exceeds the end of the scenario, rare case, but could happen
                                if current_event['t_i'] + current_event['s_i'] <= end:
                                    current_DV = current_event['Truck']
                                    Events.loc[r, 'Park Type New'] = 'Legal Park'
                                    Events.loc[r, 'Updated Time'] = current_event['t_i']
                                    Events.at[r, 'Park Type New'] = 'Legal Park'
                                    Events.at[r, 'Updated Time'] = current_event['t_i']
                                    #same update for the departure event
                                    depart_idx = np.where((Events['Truck'] == current_DV) & (Events['Event Type'] == 'Departure'))
                                    Events.loc[depart_idx[0], 'Park Type New'] = 'Legal Park'
                                    Events.loc[depart_idx[0], 'Updated Time'] = current_event['t_i'] + current_event['s_i']
                                    Events.at[depart_idx[0][0], 'Park Type New'] = 'Legal Park'
                                    Events.at[depart_idx[0][0], 'Updated Time'] = current_event['t_i'] + current_event['s_i']
                                    #remove one parking space before heading to the next event in the schedule
                                    parking_spaces_available -= 1
                                    r += 1
                                else:
                                    #randomly shifted arrival time, t_i + service exceeds the end of the scenario, dbl park the delivery vehicle
                                    current_DV = current_event['Truck']
                                    Events.loc[r, 'Park Type New'] = 'Dbl Park'
                                    Events.loc[r, 'Updated Time'] = current_event['t_i']
                                    Events.at[r, 'Park Type New'] = 'Dbl Park'
                                    Events.at[r, 'Updated Time'] = current_event['t_i']
                                    #same update for the departure event
                                    depart_idx = np.where((Events['Truck'] == current_DV) & (Events['Event Type'] == 'Departure'))
                                    Events.loc[depart_idx[0], 'Park Type New'] = 'Dbl Park'
                                    Events.loc[depart_idx[0], 'Updated Time'] = current_event['t_i'] + current_event['s_i']
                                    Events.at[depart_idx[0][0], 'Park Type New'] = 'Dbl Park'
                                    Events.at[depart_idx[0][0], 'Updated Time'] = current_event['t_i'] + current_event['s_i']
                                    r += 1
                                 
                            
                            #need specific logic for a single zero in the parking space sched
                            elif num_zeros == 1:
                                possible_starts = []
                                idx_zero = np.where(np.array(parking_space_sched) == 0)
                                
                                #first possible start needs to compare the current event time
                                #to the zero in the schedule
                                
                                #what is the location of the zero
                                zero = idx_zero[0][0]
                                
                                #need a special case where the location of the zero is (not?) the first entry of the parking_space_sched, e.g. presently there are not any parking
                                #spaces available, slightly changes the upcoming reference location
                                if zero != 0:
                                    window = upcoming.iloc[zero -1]['Expected Time'] - window_start #-1 due to the difference between
                                    #the indexing of the parking space sched and upcoming, parking space sched has one extra current parking occupancy counter in the first entry
                                
                                    #retain the window if it can accomodate the delivery vehicle
                                    #service duration
                                    if window >= current_event['s_i']:
                                        possible_starts.append(window_start) #window start is current arrival time, no concern about dbl park while waiting
                                                                            #or being outside of the current_time + max wait time
                                    
                                #As long as the only zero in the parking space schedule 
                                #is not the last entry in the sched, proceed with finding the 
                                #second window / possible start
                                if parking_space_sched[-1] != 0:
                                    #how much time is available from the event after the zero
                                    #to the end of the delivery vehicle window
                                    window = window_end - upcoming.iloc[zero]['Expected Time']
                                    
                                    #retain the window if it can accomodate the delivery vehicle
                                    #service duration and doesn't require the delivery vehicle to start service after the current time + max wait time
                                    if (window >= current_event['s_i']) & (upcoming.iloc[zero]['Expected Time'] - current_event['t_i'] <= max_wait):
                                        possible_starts.append(upcoming.iloc[zero]['Expected Time'])
                                    
                                    
                                #now that we have the list of possible starts, if there actually
                                #are not any possible starts, then double park the delivery vehicle.
                                #If there are possible starts, pick the first possible start in 
                                #the list as the new arrival time
                                if possible_starts == []:
                                    #dbl park
                                    current_DV = current_event['Truck']
                                    Events.loc[r, 'Park Type New'] = 'Dbl Park'
                                    Events.loc[r, 'Updated Time'] = current_event['t_i']
                                    Events.at[r, 'Park Type New'] = 'Dbl Park'
                                    Events.at[r, 'Updated Time'] = current_event['t_i']
                                    #same update for the departure event
                                    depart_idx = np.where((Events['Truck'] == current_DV) & (Events['Event Type'] == 'Departure'))
                                    Events.loc[depart_idx[0], 'Park Type New'] = 'Dbl Park'
                                    Events.loc[depart_idx[0], 'Updated Time'] = current_event['t_i'] + current_event['s_i']
                                    Events.at[depart_idx[0][0], 'Park Type New'] = 'Dbl Park'
                                    Events.at[depart_idx[0][0], 'Updated Time'] = current_event['t_i'] + current_event['s_i']
                                    r += 1
                                    print('late no starts issue (1)') #want to see how often this happens, should not happen 
                                    late_no_starts_1.append([c,i,r, current_event['t_i'] - current_event['a_i_OG'], np.sum(Events['Lost Reservation'] == 'Yes')])
                                else:
                                    #first check to see if possible start + service duration exceeds the end of the scenario, rare case, but could happen
                                    if possible_starts[0] + current_event['s_i'] <= end:
                                        #sched for legal park at the first entry in the possible_starts list
                                        current_DV = current_event['Truck']
                                        Events.loc[r, 'Park Type New'] = 'Legal Park'
                                        Events.loc[r, 'Updated Time'] = possible_starts[0]
                                        Events.loc[r, 't_i'] = possible_starts[0]
                                        Events.at[r, 'Park Type New'] = 'Legal Park'
                                        Events.at[r, 'Updated Time'] = possible_starts[0]
                                        Events.at[r, 't_i'] = possible_starts[0]
                                        #same update for the departure event
                                        depart_idx = np.where((Events['Truck'] == current_DV) & (Events['Event Type'] == 'Departure'))
                                        Events.loc[depart_idx[0], 'Park Type New'] = 'Legal Park'
                                        Events.loc[depart_idx[0], 'Updated Time'] = possible_starts[0] + current_event['s_i']
                                        Events.loc[depart_idx[0], 't_i'] = possible_starts[0] + current_event['s_i']
                                        Events.at[depart_idx[0][0], 'Park Type New'] = 'Legal Park'
                                        Events.at[depart_idx[0][0], 'Updated Time'] = possible_starts[0] + current_event['s_i']
                                        Events.at[depart_idx[0][0], 't_i'] = possible_starts[0] + current_event['s_i']
                                        #because we are shifting the arrival of the current event
                                        #until a later time, we need to re-sort the event schedule
                                        #based on t_i.  AND also not increment the event counter.
                                        #Becuase we want to either explore the next event which may
                                        #occur before this current event that was now shifted, OR
                                        #we will encounter this current event, but handle the parking
                                        #availability reduction in another part of the if statements.
                                       
                                        #if the first entry in the possible starts list is the current
                                        #arrival time of the delivery vehicle, also captured by window_start
                                        #then the schedule does not need to be re-sorted and we can 
                                        #increment the schedule row counter.  If, however, the first 
                                        #possible start is anything after window_start, then we need to
                                        #sort the schedule matrix with the updated t_i values and
                                        #not increase the event counter
                                        
                                        if possible_starts[0] == window_start:
                                            r += 1
                                            #remove one parking space before heading to the next event in the schedule
                                            parking_spaces_available -= 1
                                        else:
                                            Events = Events.sort_values(by = ['t_i', 'Event Type'], ascending = [True, False], ignore_index = True)
                                            #also need to consider in this case that the vehicle will dbl park for a few minutes
                                            #record that, b/c the selected possible start is not the window_start, must be greater
                                            poss_start_dbl_park_data = [current_DV,
                                                                        current_event['t_i'], #t_i, could also be represented by window_start
                                                                        'Arrival',
                                                                        possible_starts[0] - window_start, #s_i
                                                                        possible_starts[0], #d_i
                                                                        current_event['a_i_OG'],
                                                                        current_event['d_i_OG'],
                                                                        current_event['Park Type OG'],
                                                                        'Dbl Park', #park type new
                                                                        window_start, #updated time
                                                                        None #lost reservation?                                           
                                                                        ]
                                            
                                            Events_dbl_park_wait_poss_start.loc[len(Events_dbl_park_wait_poss_start)] = poss_start_dbl_park_data
                                    
                                    else:
                                        #possible start + service exceeds the end of the scenario, dbl park the delivery vehicle
                                        current_DV = current_event['Truck']
                                        Events.loc[r, 'Park Type New'] = 'Dbl Park'
                                        Events.loc[r, 'Updated Time'] = current_event['t_i']
                                        Events.at[r, 'Park Type New'] = 'Dbl Park'
                                        Events.at[r, 'Updated Time'] = current_event['t_i']
                                        #same update for the departure event
                                        depart_idx = np.where((Events['Truck'] == current_DV) & (Events['Event Type'] == 'Departure'))
                                        Events.loc[depart_idx[0], 'Park Type New'] = 'Dbl Park'
                                        Events.loc[depart_idx[0], 'Updated Time'] = current_event['t_i'] + current_event['s_i']
                                        Events.at[depart_idx[0][0], 'Park Type New'] = 'Dbl Park'
                                        Events.at[depart_idx[0][0], 'Updated Time'] = current_event['t_i'] + current_event['s_i']
                                        r += 1
                                               
                            #there is more than one zero in the upcoming parking space sched,
                            #need to find the index of the zeros and consider the possible
                            #start time windows
                            else:
                                possible_starts = []
                                idx_zero = np.where(np.array(parking_space_sched) == 0)
                                
                                #first possible start needs to compare the current event time
                                #to the first upcoming zero
                                
                                #what is the location of the first zero
                                first_zero = idx_zero[0][0] -1 #-1 included because the upcoming schedule list starts with the current parking
                                #availability which is not part of the upcoming schedule
                                window = upcoming.iloc[first_zero]['Expected Time'] - window_start
                                
                                #retain the window if it can accomodate the delivery vehicle
                                #service duration
                                if window >= current_event['s_i']:
                                    possible_starts.append(window_start) #no issues here with window_start, e.g. exceeding max_wait b/c window_start = current truck arrival time
                                    
                                #next, iterate through the space between the zeros to find
                                #other possible starts, only step into this check if there
                                #are more than 1 zero in the upcoming parking space schedule,
                                #e.g. you need 2 or more zeros in the list
                                if len(idx_zero[0]) > 1:
                                    for z in range(0, len(idx_zero[0]) -1):
                                        current_zero = idx_zero[0][z]
                                        current_zero_in_upcoming = current_zero -1
                                        after_current_zero_time = upcoming.iloc[current_zero]['Expected Time']  #the indexing is slightly off, generally add -1, but since we want the 
                                        #next event after this current zero, we remove the -1
                                        
                                        next_zero = idx_zero[0][z+1]
                                        future_zero_time = upcoming.iloc[next_zero -1]['Expected Time'] #indexing needs a -1 because the parking_space_sched starts with the
                                        #current parking available, not the first row of the upcoming matrix
                                        
                                        #the possible window then is from the event after the zero event, e.g. parking becomes available
                                        #through the next zero event
                                        window = future_zero_time - after_current_zero_time
                                        
                                        #is the window long enough to accomodate the delivery vehicle service time
                                        #and does the window start within the current arrival time + max wait time
                                        if (window >= current_event['s_i']) & (after_current_zero_time - current_event['t_i'] <= max_wait):
                                            possible_starts.append(after_current_zero_time)
                                        
                                
                                #the last window to explore is from the last zero or only zero through the end of the window
                                
                                #what is the location of the last zero, but in the upcoming schedule, hence the -1
                                last_zero = idx_zero[0][-1] -1 #-1 due to the indexing issue mentioned above, first entry is not from upcoming
                                #but from the current parking space availability
                                
                                #want the time of the event right after the last zero in the upcoming schedule, increase the index by 1
                                after_last_zero = last_zero +1
                                
                                #is the last entry in the parking space sched a zero?
                                #this would mean that there isn't a window between the
                                #last zero and the end of the window
                                if parking_space_sched[-1] != 0:
                                    
                                    window = window_end - upcoming.iloc[after_last_zero]['Expected Time']
                                
                                    #retain the window if it can accomodate the delivery vehicle
                                    #service duration
                                    if (window >= current_event['s_i']) & (upcoming.iloc[after_last_zero]['Expected Time'] - current_event['t_i'] <= max_wait):
                                        possible_starts.append(upcoming.iloc[after_last_zero]['Expected Time'])
                                
                                
                                #now that we have the list of possible starts, if there actually
                                #are not any possible starts, then double park the delivery vehicle.
                                #If there are possible starts, pick the first possible start in 
                                #the list as the new arrival time
                                if possible_starts == []:
                                    #dbl park
                                    current_DV = current_event['Truck']
                                    Events.loc[r, 'Park Type New'] = 'Dbl Park'
                                    Events.loc[r, 'Updated Time'] = current_event['t_i']
                                    Events.at[r, 'Park Type New'] = 'Dbl Park'
                                    Events.at[r, 'Updated Time'] = current_event['t_i']
                                    #same update for the departure event
                                    depart_idx = np.where((Events['Truck'] == current_DV) & (Events['Event Type'] == 'Departure'))
                                    Events.loc[depart_idx[0], 'Park Type New'] = 'Dbl Park'
                                    Events.loc[depart_idx[0], 'Updated Time'] = current_event['t_i'] + current_event['s_i']
                                    Events.at[depart_idx[0][0], 'Park Type New'] = 'Dbl Park'
                                    Events.at[depart_idx[0][0], 'Updated Time'] = current_event['t_i'] + current_event['s_i']
                                    r += 1
                                    print('late no starts issue (1+)') #want to see how often this happens, should not happen 
                                    late_no_starts_more_1.append([c,i,r, current_event['t_i'] - current_event['a_i_OG'], np.sum(Events['Lost Reservation'] == 'Yes')])
                                else:
                                    #first check to see if possible start + service duration exceeds the end of the scenario, rare case, but could happen
                                    if possible_starts[0] + current_event['s_i'] <= end:
                                        #sched for legal park at the first entry in the possible_starts list
                                        current_DV = current_event['Truck']
                                        Events.loc[r, 'Park Type New'] = 'Legal Park'
                                        Events.loc[r, 'Updated Time'] = possible_starts[0]
                                        Events.loc[r, 't_i'] = possible_starts[0]
                                        Events.at[r, 'Park Type New'] = 'Legal Park'
                                        Events.at[r, 'Updated Time'] = possible_starts[0]
                                        Events.at[r, 't_i'] = possible_starts[0]
                                        #same update for the departure event
                                        depart_idx = np.where((Events['Truck'] == current_DV) & (Events['Event Type'] == 'Departure'))
                                        Events.loc[depart_idx[0], 'Park Type New'] = 'Legal Park'
                                        Events.loc[depart_idx[0], 'Updated Time'] = possible_starts[0] + current_event['s_i']
                                        Events.loc[depart_idx[0], 't_i'] = possible_starts[0] + current_event['s_i']
                                        Events.at[depart_idx[0][0], 'Park Type New'] = 'Legal Park'
                                        Events.at[depart_idx[0][0], 'Updated Time'] = possible_starts[0] + current_event['s_i']
                                        Events.at[depart_idx[0][0], 't_i'] = possible_starts[0] + current_event['s_i']
                                        #because we are shifting the arrival of the current event
                                        #until a later time, we need to re-sort the event schedule
                                        #based on t_i.  AND also not increment the event counter.
                                        #Becuase we want to either explore the next event which may
                                        #occur before this current event that was now shifted, OR
                                        #we will encounter this current event, but handle the parking
                                        #availability reduction in another part of the if statements.
                                       
                                        #if the first entry in the possible starts list is the current
                                        #arrival time of the delivery vehicle, also captured by window_start
                                        #then the schedule does not need to be re-sorted and we can 
                                        #increment the schedule row counter.  If, however, the first 
                                        #possible start is anything after window_start, then we need to
                                        #sort the schedule matrix with the updated t_i values and
                                        #not increase the event counter
                                        
                                        if possible_starts[0] == window_start:
                                            r += 1
                                            #remove one parking space before heading to the next event in the schedule
                                            parking_spaces_available -= 1
                                        else:
                                            Events = Events.sort_values(by = ['t_i', 'Event Type'], ascending = [True, False], ignore_index = True)
                                            #also need to consider in this case that the vehicle will dbl park for a few minutes
                                            #record that, b/c the selected possible start is not the window_start, must be greater
                                            poss_start_dbl_park_data = [current_DV,
                                                                        current_event['t_i'], #t_i, could also be represented by window_start
                                                                        'Arrival',
                                                                        possible_starts[0] - window_start, #s_i
                                                                        possible_starts[0], #d_i
                                                                        current_event['a_i_OG'],
                                                                        current_event['d_i_OG'],
                                                                        current_event['Park Type OG'],
                                                                        'Dbl Park', #park type new
                                                                        window_start, #updated time
                                                                        None #lost reservation?                                           
                                                                        ]
                                            
                                            Events_dbl_park_wait_poss_start.loc[len(Events_dbl_park_wait_poss_start)] = poss_start_dbl_park_data
                                    
                                    else:
                                        #possible start + service exceeds the end of the scenario, dbl park the delivery vehicle
                                        current_DV = current_event['Truck']
                                        Events.loc[r, 'Park Type New'] = 'Dbl Park'
                                        Events.loc[r, 'Updated Time'] = current_event['t_i']
                                        Events.at[r, 'Park Type New'] = 'Dbl Park'
                                        Events.at[r, 'Updated Time'] = current_event['t_i']
                                        #same update for the departure event
                                        depart_idx = np.where((Events['Truck'] == current_DV) & (Events['Event Type'] == 'Departure'))
                                        Events.loc[depart_idx[0], 'Park Type New'] = 'Dbl Park'
                                        Events.loc[depart_idx[0], 'Updated Time'] = current_event['t_i'] + current_event['s_i']
                                        Events.at[depart_idx[0][0], 'Park Type New'] = 'Dbl Park'
                                        Events.at[depart_idx[0][0], 'Updated Time'] = current_event['t_i'] + current_event['s_i']
                                        r += 1
                                
                                                    
                         
                        #or early?
                        elif current_event['t_i'] <= current_event['a_i_OG']:
                            
                            #what is the window of time over which we need to consider upcoming vehicle events
                            window_start = current_event['t_i']
                            window_end = current_event['d_i_OG'] + buffer
                            
                            #what are the upcoming events?
                            upcoming = pd.DataFrame(columns = ['Truck', 't_i', 'Event Type', 's_i', 'd_i', 'a_i_OG', 'd_i_OG', 'Park Type OG', 'Park Type New', 'Updated Time'])
                            
                            #consider upcoming original reservations that have not been processed yet within the window
                            df = Events.loc[np.where((Events['Truck'] != current_event['Truck']) &
                                                (Events['Park Type OG'] == 'Legal Park') & 
                                                (Events['Event Type'] == 'Arrival') &
                                                (Events['Park Type New'] == 'TBD') &
                                                (Events['a_i_OG'] >= window_start - buffer) & #someone else could be arriving late, but was originally schedule to arrive before the current event time step
                                                (Events['a_i_OG'] < window_end)
                                                )]
                            upcoming = pd.concat([upcoming, df])
                            #consider scheduled, but unseen departures
                            df = Events.loc[np.where((Events['Truck'] != current_event['Truck']) &
                                                (Events['Park Type OG'] == 'Legal Park') & 
                                                (Events['Event Type'] == 'Departure') &
                                                (Events['Park Type New'] == 'TBD') &
                                                (Events['d_i_OG'] >= window_start - buffer) &
                                                (Events['d_i_OG'] < window_end)
                                                )]
                            upcoming = pd.concat([upcoming, df])
                            #consider new departures switched from dbl to legal parking
                            df = Events.loc[np.where((Events['Park Type OG'] == 'Dbl Park') & 
                                                (Events['Event Type'] == 'Departure') &
                                                (Events['Park Type New'] == 'Legal Park') &
                                                (Events['t_i'] >= window_start) &
                                                (Events['t_i'] < window_end)
                                                )]
                            upcoming = pd.concat([upcoming, df])
                            #consider scheduled, but shifted arrivals
                            df = Events.loc[np.where((Events['Park Type OG'] == 'Legal Park') & 
                                                (Events['Event Type'] == 'Arrival') &
                                                (Events['Park Type New'] == 'Legal Park') &
                                                (Events['Updated Time'] > window_start) & #only want to consider already processed arrivals that are > window start, b/c '=' window start is not technically upcoming,
                                                #had an issue where two vehicles arrived at t = 0, incorrectly double counted one of the arrivals
                                                (Events['Updated Time'] < window_end)
                                                )]
                            upcoming = pd.concat([upcoming, df])
                            #consider scheduled, but shifted departures
                            df = Events.loc[np.where((Events['Park Type OG'] == 'Legal Park') & 
                                                (Events['Event Type'] == 'Departure') &
                                                (Events['Park Type New'] == 'Legal Park') &
                                                (Events['Updated Time'] >= window_start) &
                                                (Events['Updated Time'] < window_end)
                                                )]
                            upcoming = pd.concat([upcoming, df])
                            
                            upcoming.reset_index(drop = True, inplace = True)
                            
                            
                            # #upcoming refinement
                            # #for a scheduled, but unseen arrival, if the arrival OG is less
                            # #that the current time, assume the worst, make the arrival OG
                            # #equal to arrival OG + buffer
                            # #but, added a section that considers if we should be full worst case or not based on s_i of current vehicle versus the unseen late vehicle
                            # for row in range(0, len(upcoming)):
                            #     #is this a legal parked arrival that has not yet been seen?
                            #     if (upcoming.iloc[row]['Event Type'] == 'Arrival') and (upcoming.iloc[row]['Park Type OG'] == 'Legal Park') and (upcoming.iloc[row]['Park Type New'] == 'TBD'):
                            #         #was the planned arrival time before the current event time?
                            #         if upcoming.iloc[row]['a_i_OG'] < current_event['t_i']:
                                        
                            #             #does the unseen late arrival have a larger s_i than the current arrival?
                            #             #if so, be conservative and try to save the unseen late arrival by adding the 
                            #             #full buffer to the a_i_OG and d_i_OG
                            #             if upcoming.iloc[row]['s_i'] > current_event['s_i']:
                                            
                            #                 #if so, then make the expected arrival the worst case, add to the end of the buffer from the OG arrival time
                            #                 upcoming.loc[row, 'a_i_OG'] = upcoming.iloc[row]['a_i_OG'] + buffer
                            #                 upcoming.loc[row, 'd_i_OG'] = upcoming.iloc[row]['d_i_OG'] + buffer
                                            
                            #                 #need to update to the worst case departure time as well
                            #                 #what truck is currently arriving?
                            #                 DV = upcoming.iloc[row]['Truck']
                            #                 #what is the index in upcoming of the DV departure event
                            #                 DV_idx = np.where((upcoming['Truck'] == DV) & (upcoming['Event Type'] == 'Departure'))
                            #                 upcoming.loc[DV_idx[0], 'd_i_OG'] = upcoming.iloc[DV_idx]['d_i_OG'] + buffer
                            #                 upcoming.loc[DV_idx[0], 'a_i_OG'] = upcoming.iloc[DV_idx]['a_i_OG'] + buffer
                                            
                            #             else:
                            #                 #if the s_i of the unseen late arrival is less than the current arrival
                            #                 #we want to try to schedule the current arrival, so do not put in the worst case
                            #                 #scenario, instead just assign the expected arrival time of the unseen arrival to
                            #                 #the current event time
                            #                 upcoming.loc[row, 'a_i_OG'] = current_event['t_i']
                            #                 upcoming.loc[row, 'd_i_OG'] = current_event['t_i'] + upcoming.iloc[row]['s_i']
                                            
                            #                 #need to update to the worst case departure time as well
                            #                 #what truck is currently arriving?
                            #                 DV = upcoming.iloc[row]['Truck']
                            #                 #what is the index in upcoming of the DV departure event
                            #                 DV_idx = np.where((upcoming['Truck'] == DV) & (upcoming['Event Type'] == 'Departure'))
                            #                 upcoming.loc[DV_idx[0], 'd_i_OG'] = current_event['t_i'] + upcoming.iloc[row]['s_i']
                            #                 upcoming.loc[DV_idx[0], 'a_i_OG'] = current_event['t_i']
                            
                            #testing new upcoming refinement logic
                            for row in range(0, len(upcoming)):
                                #is this a legal parked arrival that has not yet been seen?
                                if (upcoming.iloc[row]['Event Type'] == 'Arrival') and (upcoming.iloc[row]['Park Type OG'] == 'Legal Park') and (upcoming.iloc[row]['Park Type New'] == 'TBD'):
                                    #was the planned arrival time before the current event time?
                                    if upcoming.iloc[row]['a_i_OG'] < current_event['t_i']:
                                    
                                        #if so, then make the expected arrival the worst case e.g. truck arrives at current time
                                        #and make the departure the worst case e.g. hold all the way through d_i_OG + buffer
                                        upcoming.loc[row, 'a_i_OG'] = current_event['t_i']
                                        upcoming.loc[row, 'd_i_OG'] = upcoming.iloc[row]['d_i_OG'] + buffer
                                        
                                        #need to update to the worst case departure time as well
                                        #what truck is currently arriving?
                                        DV = upcoming.iloc[row]['Truck']
                                        #what is the index in upcoming of the DV departure event
                                        DV_idx = np.where((upcoming['Truck'] == DV) & (upcoming['Event Type'] == 'Departure'))
                                        upcoming.loc[DV_idx[0], 'a_i_OG'] = current_event['t_i']
                                        upcoming.loc[DV_idx[0], 'd_i_OG'] = upcoming.iloc[DV_idx]['d_i_OG'] + buffer
                                        
                                        
                            #what does the final expected upcoming schedule look like?
                            #need to step through the upcoming sched and pull the relevant
                            #expected future time for each case, e.g. unseen arrival legal park, pull the a_i_OG
                            #post above worst case refinement, or for seen arrival legal park,
                            #pull the t_i from upcoming
                            upcoming.insert(7, 'Expected Time', None)
                            for row in range(0, len(upcoming)):
                                #unseen, legal park, arrival
                                if (upcoming.iloc[row]['Event Type'] == 'Arrival') & (upcoming.iloc[row]['Park Type OG'] == 'Legal Park') & (upcoming.iloc[row]['Park Type New'] == 'TBD'):
                                    upcoming.loc[row, 'Expected Time'] = upcoming.iloc[row]['a_i_OG']
                                #unseen, legal park, departure
                                if (upcoming.iloc[row]['Event Type'] == 'Departure') & (upcoming.iloc[row]['Park Type OG'] == 'Legal Park') & (upcoming.iloc[row]['Park Type New'] == 'TBD'):
                                    upcoming.loc[row, 'Expected Time'] = upcoming.iloc[row]['d_i_OG']
                                #seen, dbl park to legal park departure
                                if (upcoming.iloc[row]['Event Type'] == 'Departure') & (upcoming.iloc[row]['Park Type OG'] == 'Dbl Park') & (upcoming.iloc[row]['Park Type New'] == 'Legal Park'):
                                    upcoming.loc[row, 'Expected Time'] = upcoming.iloc[row]['Updated Time']
                                #seen, legal park, arrival
                                if (upcoming.iloc[row]['Event Type'] == 'Arrival') & (upcoming.iloc[row]['Park Type OG'] == 'Legal Park') & (upcoming.iloc[row]['Park Type New'] == 'Legal Park'):
                                    upcoming.loc[row, 'Expected Time'] = upcoming.iloc[row]['Updated Time']
                                #seen, legal park, departure
                                if (upcoming.iloc[row]['Event Type'] == 'Departure') & (upcoming.iloc[row]['Park Type OG'] == 'Legal Park') & (upcoming.iloc[row]['Park Type New'] == 'Legal Park'):
                                    upcoming.loc[row, 'Expected Time'] = upcoming.iloc[row]['Updated Time']
                            
                            upcoming = upcoming.sort_values(by = ['Expected Time', 'Event Type'], ascending = [True, False], ignore_index = True)            
                            
                            
                            #now we can start counting out the future parking availability
                            parking_space_sched = []
                            parking_space_sched.append(parking_spaces_available)
                            parking_counter = parking_spaces_available
                            for row in range(0, len(upcoming)):
                                if upcoming.iloc[row]['Event Type'] == 'Arrival':
                                    if parking_counter != 0:
                                        parking_counter -= 1
                                        parking_space_sched.append(parking_counter)
                                    else:
                                        parking_space_sched.append(parking_counter)
                                        print('early counter negative issue')
                                elif upcoming.iloc[row]['Event Type'] == 'Departure':
                                    if parking_counter != c:
                                        parking_counter += 1
                                        parking_space_sched.append(parking_counter)
                                    elif parking_counter == c:
                                        print('early counter issue')
                                        
                                        
                            #are there any zeros in the upcoming parking space schedule?
                            #which would mean that there may not be space for the current truck
                            num_zeros = parking_space_sched.count(0)
                            if num_zeros == 0: #no issues parking the current delivery vehicle at the current event time, update the events schedule
                                current_DV = current_event['Truck']
                                Events.loc[r, 'Park Type New'] = 'Legal Park'
                                Events.loc[r, 'Updated Time'] = current_event['t_i']
                                Events.at[r, 'Park Type New'] = 'Legal Park'
                                Events.at[r, 'Updated Time'] = current_event['t_i']
                                #same update for the departure event
                                depart_idx = np.where((Events['Truck'] == current_DV) & (Events['Event Type'] == 'Departure'))
                                Events.loc[depart_idx[0], 'Park Type New'] = 'Legal Park'
                                Events.loc[depart_idx[0], 'Updated Time'] = current_event['t_i'] + current_event['s_i']
                                Events.at[depart_idx[0][0], 'Park Type New'] = 'Legal Park'
                                Events.at[depart_idx[0][0], 'Updated Time'] = current_event['t_i'] + current_event['s_i']
                                #remove one parking space before heading to the next event in the schedule
                                parking_spaces_available -= 1
                                r += 1
                            
                            #need specific logic for a single zero in the parking space sched
                            elif num_zeros == 1:
                                possible_starts = []
                                idx_zero = np.where(np.array(parking_space_sched) == 0)
                                
                                #first possible start needs to compare the current event time
                                #to the zero in the schedule
                                
                                #what is the location of the zero
                                zero = idx_zero[0][0]
                                
                                #need a special case where the location of the zero is the first entry of the parking_space_sched, e.g. presently there are not any parking
                                #spaces available, slightly changes the upcoming reference location
                                if zero != 0:
                                    window = upcoming.iloc[zero -1]['Expected Time'] - window_start #-1 due to the difference between
                                    #the indexing of the parking space sched and upcoming, parking space sched has one extra current parking occupancy counter in the first entry
                                
                                    #retain the window if it can accomodate the delivery vehicle
                                    #service duration
                                    if window >= current_event['s_i']:
                                        possible_starts.append(window_start)
                                    
                                #As long as the only zero in the parking space schedule 
                                #is not the last entry in the sched, proceed with finding the 
                                #second window / possible start
                                if parking_space_sched[-1] != 0:
                                    #how much time is available from the event after the zero
                                    #to the end of the delivery vehicle window
                                    window = window_end - upcoming.iloc[zero]['Expected Time']
                                    
                                    #retain the window if it can accomodate the delivery vehicle
                                    #service duration
                                    if (window >= current_event['s_i']) & (upcoming.iloc[zero]['Expected Time'] - current_event['t_i'] <= max_wait):
                                        possible_starts.append(upcoming.iloc[zero]['Expected Time'])
                                    
                                    
                                #now that we have the list of possible starts, if there actually
                                #are not any possible starts, then double park the delivery vehicle.
                                #If there are possible starts, pick the first possible start in 
                                #the list as the new arrival time
                                if possible_starts == []:
                                    #dbl park
                                    current_DV = current_event['Truck']
                                    Events.loc[r, 'Park Type New'] = 'Dbl Park'
                                    Events.loc[r, 'Updated Time'] = current_event['t_i']
                                    Events.at[r, 'Park Type New'] = 'Dbl Park'
                                    Events.at[r, 'Updated Time'] = current_event['t_i']
                                    #same update for the departure event
                                    depart_idx = np.where((Events['Truck'] == current_DV) & (Events['Event Type'] == 'Departure'))
                                    Events.loc[depart_idx[0], 'Park Type New'] = 'Dbl Park'
                                    Events.loc[depart_idx[0], 'Updated Time'] = current_event['t_i'] + current_event['s_i']
                                    Events.at[depart_idx[0][0], 'Park Type New'] = 'Dbl Park'
                                    Events.at[depart_idx[0][0], 'Updated Time'] = current_event['t_i'] + current_event['s_i']
                                    r += 1
                                    print('early no starts issue (1)') #want to see how often this happens, should not happen 
                                    print(current_event['a_i_OG'] - window_start)
                                    early_no_starts_1.append([c,i,r,current_event['a_i_OG'] - window_start, np.sum(Events['Lost Reservation'] == 'Yes')])
                                else:
                                    #first check to see if possible start + service duration exceeds the end of the scenario, rare case, but could happen
                                    if possible_starts[0] + current_event['s_i'] <= end:
                                        #sched for legal park at the first entry in the possible_starts list
                                        current_DV = current_event['Truck']
                                        Events.loc[r, 'Park Type New'] = 'Legal Park'
                                        Events.loc[r, 'Updated Time'] = possible_starts[0]
                                        Events.loc[r, 't_i'] = possible_starts[0]
                                        Events.at[r, 'Park Type New'] = 'Legal Park'
                                        Events.at[r, 'Updated Time'] = possible_starts[0]
                                        Events.at[r, 't_i'] = possible_starts[0]
                                        #same update for the departure event
                                        depart_idx = np.where((Events['Truck'] == current_DV) & (Events['Event Type'] == 'Departure'))
                                        Events.loc[depart_idx[0], 'Park Type New'] = 'Legal Park'
                                        Events.loc[depart_idx[0], 'Updated Time'] = possible_starts[0] + current_event['s_i']
                                        Events.loc[depart_idx[0], 't_i'] = possible_starts[0] + current_event['s_i']
                                        Events.at[depart_idx[0][0], 'Park Type New'] = 'Legal Park'
                                        Events.at[depart_idx[0][0], 'Updated Time'] = possible_starts[0] + current_event['s_i']
                                        Events.at[depart_idx[0][0], 't_i'] = possible_starts[0] + current_event['s_i']
                                        #because we are shifting the arrival of the current event
                                        #until a later time, we need to re-sort the event schedule
                                        #based on t_i.  AND also not increment the event counter.
                                        #Becuase we want to either explore the next event which may
                                        #occur before this current event that was now shifted, OR
                                        #we will encounter this current event, but handle the parking
                                        #availability reduction in another part of the if statements.
                                       
                                        #if the first entry in the possible starts list is the current
                                        #arrival time of the delivery vehicle, also captured by window_start
                                        #then the schedule does not need to be re-sorted and we can 
                                        #increment the schedule row counter.  If, however, the first 
                                        #possible start is anything after window_start, then we need to
                                        #sort the schedule matrix with the updated t_i values and
                                        #not increase the event counter
                                        
                                        if possible_starts[0] == window_start:
                                            r += 1
                                            #remove one parking space before heading to the next event in the schedule
                                            parking_spaces_available -= 1
                                        else:
                                            Events = Events.sort_values(by = ['t_i', 'Event Type'], ascending = [True, False], ignore_index = True)
                                            
                                            #also need to consider in this case that the vehicle will dbl park for a few minutes
                                            #record that, b/c the selected possible start is not the window_start, must be greater
                                            poss_start_dbl_park_data = [current_DV,
                                                                        current_event['t_i'], #t_i, could also be represented by window_start
                                                                        'Arrival',
                                                                        possible_starts[0] - window_start, #s_i
                                                                        possible_starts[0], #d_i
                                                                        current_event['a_i_OG'],
                                                                        current_event['d_i_OG'],
                                                                        current_event['Park Type OG'],
                                                                        'Dbl Park', #park type new
                                                                        window_start, #updated time
                                                                        None #lost reservation?                                           
                                                                        ]
                                            
                                            Events_dbl_park_wait_poss_start.loc[len(Events_dbl_park_wait_poss_start)] = poss_start_dbl_park_data
                                    
                                    else:
                                        #possible start + service exceeds the end of the scenario, dbl park the delivery vehicle
                                        current_DV = current_event['Truck']
                                        Events.loc[r, 'Park Type New'] = 'Dbl Park'
                                        Events.loc[r, 'Updated Time'] = current_event['t_i']
                                        Events.at[r, 'Park Type New'] = 'Dbl Park'
                                        Events.at[r, 'Updated Time'] = current_event['t_i']
                                        #same update for the departure event
                                        depart_idx = np.where((Events['Truck'] == current_DV) & (Events['Event Type'] == 'Departure'))
                                        Events.loc[depart_idx[0], 'Park Type New'] = 'Dbl Park'
                                        Events.loc[depart_idx[0], 'Updated Time'] = current_event['t_i'] + current_event['s_i']
                                        Events.at[depart_idx[0][0], 'Park Type New'] = 'Dbl Park'
                                        Events.at[depart_idx[0][0], 'Updated Time'] = current_event['t_i'] + current_event['s_i']
                                        r += 1
                                            
                            
                            #there is more than one zero in the upcoming parking space sched,
                            #need to find the index of the zeros and consider the possible
                            #start time windows
                            else:
                                possible_starts = []
                                idx_zero = np.where(np.array(parking_space_sched) == 0)
                                
                                #first possible start needs to compare the current event time
                                #to the first upcoming zero
                                
                                #what is the location of the first zero
                                first_zero = idx_zero[0][0] #-1 included because the upcoming schedule list starts with the current parking
                                #availability which is not part of the upcoming schedule
                                window = upcoming.iloc[first_zero]['Expected Time'] - window_start
                                
                                #retain the window if it can accomodate the delivery vehicle
                                #service duration
                                if window >= current_event['s_i']:
                                    possible_starts.append(window_start)
                                    
                                #next, iterate through the space between the zeros to find
                                #other possible starts, only step into this check if there
                                #are more than 1 zero in the upcoming parking space schedule,
                                #e.g. you need 2 or more zeros in the list
                                if len(idx_zero[0]) > 1:
                                    for z in range(0, len(idx_zero[0]) -1): #-1 becuase we do not want to explore the last zero in the sched, that is in the next step
                                        current_zero = idx_zero[0][z]
                                        current_zero_in_upcoming = current_zero -1
                                        after_current_zero_time = upcoming.iloc[current_zero]['Expected Time']  #the indexing is slightly off, generally add -1, but since we want the 
                                        #next event after this current zero, we remove the -1
                                        
                                        next_zero = idx_zero[0][z+1]
                                        future_zero_time = upcoming.iloc[next_zero -1]['Expected Time'] #indexing needs a -1 because the parking_space_sched starts with the
                                        #current parking available, not the first row of the upcoming matrix
                                        
                                        #the possible window then is from the event after the zero event, e.g. parking becomes available
                                        #through the next zero event
                                        window = future_zero_time - after_current_zero_time
                                        
                                        #is the window long enough to accomodate the delivery vehicle service time
                                        #and does the window start within the current arrival time + max wait time
                                        if (window >= current_event['s_i']) & (after_current_zero_time - current_event['t_i'] <= max_wait):
                                            possible_starts.append(after_current_zero_time)
                                        
                                
                                #the last window to explore is from the last zero or only zero through the end of the window
                                
                                #what is the location of the last zero, but in the upcoming schedule, hence the -1
                                last_zero = idx_zero[0][-1] -1 #-1 due to the indexing issue mentioned above, first entry is not from upcoming
                                #but from the current parking space availability
                                
                                #want the time of the event right after the last zero in the upcoming schedule, increase the index by 1
                                after_last_zero = last_zero +1
                                
                                #is the last entry in the parking space sched a zero?
                                #this would mean that there isn't a window between the
                                #last zero and the end of the window
                                if parking_space_sched[-1] != 0:
                                    
                                    window = window_end - upcoming.iloc[after_last_zero]['Expected Time']
                                
                                    #retain the window if it can accomodate the delivery vehicle
                                    #service duration
                                    if (window >= current_event['s_i']) & (upcoming.iloc[after_last_zero]['Expected Time'] - current_event['t_i'] <= max_wait):
                                        possible_starts.append(upcoming.iloc[after_last_zero]['Expected Time'])
                            
                        
                                #now that we have the list of possible starts, if there actually
                                #are not any possible starts, then double park the delivery vehicle.
                                #If there are possible starts, pick the first possible start in 
                                #the list as the new arrival time
                                if possible_starts == []:
                                    #dbl park
                                    current_DV = current_event['Truck']
                                    Events.loc[r, 'Park Type New'] = 'Dbl Park'
                                    Events.loc[r, 'Updated Time'] = current_event['t_i']
                                    Events.at[r, 'Park Type New'] = 'Dbl Park'
                                    Events.at[r, 'Updated Time'] = current_event['t_i']
                                    #same update for the departure event
                                    depart_idx = np.where((Events['Truck'] == current_DV) & (Events['Event Type'] == 'Departure'))
                                    Events.loc[depart_idx[0], 'Park Type New'] = 'Dbl Park'
                                    Events.loc[depart_idx[0], 'Updated Time'] = current_event['t_i'] + current_event['s_i']
                                    Events.at[depart_idx[0][0], 'Park Type New'] = 'Dbl Park'
                                    Events.at[depart_idx[0][0], 'Updated Time'] = current_event['t_i'] + current_event['s_i']
                                    r += 1
                                    print('early no starts issue (1+)') #want to see how often this happens, should not happen 
                                    print(current_event['a_i_OG'] - window_start)
                                    early_no_starts_more_1.append([c,i,r,current_event['a_i_OG'] - window_start, np.sum(Events['Lost Reservation'] == 'Yes')])
                                else:
                                    #first check to see if possible start + service duration exceeds the end of the scenario, rare case, but could happen
                                    if possible_starts[0] + current_event['s_i'] <= end:
                                        #sched for legal park at the first entry in the possible_starts list
                                        current_DV = current_event['Truck']
                                        Events.loc[r, 'Park Type New'] = 'Legal Park'
                                        Events.loc[r, 'Updated Time'] = possible_starts[0]
                                        Events.loc[r, 't_i'] = possible_starts[0]
                                        Events.at[r, 'Park Type New'] = 'Legal Park'
                                        Events.at[r, 'Updated Time'] = possible_starts[0]
                                        Events.at[r, 't_i'] = possible_starts[0]
                                        #same update for the departure event
                                        depart_idx = np.where((Events['Truck'] == current_DV) & (Events['Event Type'] == 'Departure'))
                                        Events.loc[depart_idx[0], 'Park Type New'] = 'Legal Park'
                                        Events.loc[depart_idx[0], 'Updated Time'] = possible_starts[0] + current_event['s_i']
                                        Events.loc[depart_idx[0], 't_i'] = possible_starts[0] + current_event['s_i']
                                        Events.at[depart_idx[0][0], 'Park Type New'] = 'Legal Park'
                                        Events.at[depart_idx[0][0], 'Updated Time'] = possible_starts[0] + current_event['s_i']
                                        Events.at[depart_idx[0][0], 't_i'] = possible_starts[0] + current_event['s_i']
                                        #because we are shifting the arrival of the current event
                                        #until a later time, we need to re-sort the event schedule
                                        #based on t_i.  AND also not increment the event counter.
                                        #Becuase we want to either explore the next event which may
                                        #occur before this current event that was now shifted, OR
                                        #we will encounter this current event, but handle the parking
                                        #availability reduction in another part of the if statements.
                                       
                                        #if the first entry in the possible starts list is the current
                                        #arrival time of the delivery vehicle, also captured by window_start
                                        #then the schedule does not need to be re-sorted and we can 
                                        #increment the schedule row counter.  If, however, the first 
                                        #possible start is anything after window_start, then we need to
                                        #sort the schedule matrix with the updated t_i values and
                                        #not increase the event counter
                                        
                                        if possible_starts[0] == window_start:
                                            r += 1
                                            #remove one parking space before heading to the next event in the schedule
                                            parking_spaces_available -= 1
                                        else:
                                            Events = Events.sort_values(by = ['t_i', 'Event Type'], ascending = [True, False], ignore_index = True)
                                            
                                            #also need to consider in this case that the vehicle will dbl park for a few minutes
                                            #record that, b/c the selected possible start is not the window_start, must be greater
                                            poss_start_dbl_park_data = [current_DV,
                                                                        current_event['t_i'], #t_i, could also be represented by window_start
                                                                        'Arrival',
                                                                        possible_starts[0] - window_start, #s_i
                                                                        possible_starts[0], #d_i
                                                                        current_event['a_i_OG'],
                                                                        current_event['d_i_OG'],
                                                                        current_event['Park Type OG'],
                                                                        'Dbl Park', #park type new
                                                                        window_start, #updated time
                                                                        None #lost reservation?                                           
                                                                        ]
                                            
                                            Events_dbl_park_wait_poss_start.loc[len(Events_dbl_park_wait_poss_start)] = poss_start_dbl_park_data
                                    
                                    else:
                                        #possible start + service exceeds the end of the scenario, dbl park the delivery vehicle
                                        current_DV = current_event['Truck']
                                        Events.loc[r, 'Park Type New'] = 'Dbl Park'
                                        Events.loc[r, 'Updated Time'] = current_event['t_i']
                                        Events.at[r, 'Park Type New'] = 'Dbl Park'
                                        Events.at[r, 'Updated Time'] = current_event['t_i']
                                        #same update for the departure event
                                        depart_idx = np.where((Events['Truck'] == current_DV) & (Events['Event Type'] == 'Departure'))
                                        Events.loc[depart_idx[0], 'Park Type New'] = 'Dbl Park'
                                        Events.loc[depart_idx[0], 'Updated Time'] = current_event['t_i'] + current_event['s_i']
                                        Events.at[depart_idx[0][0], 'Park Type New'] = 'Dbl Park'
                                        Events.at[depart_idx[0][0], 'Updated Time'] = current_event['t_i'] + current_event['s_i']
                                        r += 1
                                    
                                    
                        
                    #the current event has already been processed    
                    elif (current_event['Park Type New'] == 'Legal Park'):
                        #in this instance, we are trying to account for late or early arrivals
                        #which shifted in from t_i to another future arrival time, generally
                        #within 5 minutes from t_i.  But, because there could be other
                        #events between this t_i and the new, processed arrival, we don't want to 
                        #consider the parking space availability change until late in time
                        #e.g. handle the parking space change when we come back to the 
                        #updated and process event.  We will have resorted the events matrix
                        #after processing
                        parking_spaces_available -= 1
                        r += 1
                        
                        
                        
                        
                        
                #is the current event instead a dbl park arrival?
                elif current_event['Park Type OG'] == 'Dbl Park':
                    
                    #has the current event already been processed?
                    if current_event['Park Type New'] == 'TBD':
                        
                        #if current parking is not available, dbl park the delivery vehicle
                        if parking_spaces_available == 0:
                            current_DV = current_event['Truck']
                            Events.loc[r, 'Park Type New'] = 'Dbl Park'
                            Events.loc[r, 'Updated Time'] = current_event['t_i']
                            Events.at[r, 'Park Type New'] = 'Dbl Park'
                            Events.at[r, 'Updated Time'] = current_event['t_i']
                            #same update for the departure event
                            depart_idx = np.where((Events['Truck'] == current_DV) & (Events['Event Type'] == 'Departure'))
                            Events.loc[depart_idx[0], 'Park Type New'] = 'Dbl Park'
                            Events.loc[depart_idx[0], 'Updated Time'] = current_event['t_i'] + current_event['s_i']
                            Events.at[depart_idx[0][0], 'Park Type New'] = 'Dbl Park'
                            Events.at[depart_idx[0][0], 'Updated Time'] = current_event['t_i'] + current_event['s_i']
                            r += 1
                        
                        #there is a parking space currently available, check to see if there are
                        #any conflicts in the upcoming schedule
                        else:
                            #what is the window of time over which we need to consider upcoming vehicle events
                            window_start = current_event['t_i']
                            window_end = current_event['t_i'] + current_event['s_i']
                            
                            #what are the upcoming events?
                            upcoming = pd.DataFrame(columns = ['Truck', 't_i', 'Event Type', 's_i', 'd_i', 'a_i_OG', 'd_i_OG', 'Park Type OG', 'Park Type New', 'Updated Time'])
                            
                            #consider upcoming original reservations that have not been processed yet within the window
                            df = Events.loc[np.where((Events['Truck'] != current_event['Truck']) &
                                                (Events['Park Type OG'] == 'Legal Park') & 
                                                (Events['Event Type'] == 'Arrival') &
                                                (Events['Park Type New'] == 'TBD') &
                                                (Events['a_i_OG'] >= window_start - buffer) & #someone else could be arriving late, but was originally schedule to arrive before the current event time step
                                                (Events['a_i_OG'] < window_end)
                                                )]
                            upcoming = pd.concat([upcoming, df])
                            #consider scheduled, but unseen departures
                            df = Events.loc[np.where((Events['Truck'] != current_event['Truck']) &
                                                (Events['Park Type OG'] == 'Legal Park') & 
                                                (Events['Event Type'] == 'Departure') &
                                                (Events['Park Type New'] == 'TBD') &
                                                (Events['d_i_OG'] >= window_start - buffer) &
                                                (Events['d_i_OG'] < window_end)
                                                )]
                            upcoming = pd.concat([upcoming, df])
                            #consider new departures switched from dbl to legal parking
                            df = Events.loc[np.where((Events['Park Type OG'] == 'Dbl Park') & 
                                                (Events['Event Type'] == 'Departure') &
                                                (Events['Park Type New'] == 'Legal Park') &
                                                (Events['t_i'] >= window_start) &
                                                (Events['t_i'] < window_end)
                                                )]
                            upcoming = pd.concat([upcoming, df])
                            #consider scheduled, but shifted arrivals
                            df = Events.loc[np.where((Events['Park Type OG'] == 'Legal Park') & 
                                                (Events['Event Type'] == 'Arrival') &
                                                (Events['Park Type New'] == 'Legal Park') &
                                                (Events['Updated Time'] > window_start) & #issue when multiple trucks arrive at time zero, don't want to double consider trucks that have already been accounted for when creating the parking space schedulde
                                                (Events['Updated Time'] < window_end)
                                                )]
                            upcoming = pd.concat([upcoming, df])
                            #consider scheduled, but shifted departures
                            df = Events.loc[np.where((Events['Park Type OG'] == 'Legal Park') & 
                                                (Events['Event Type'] == 'Departure') &
                                                (Events['Park Type New'] == 'Legal Park') &
                                                (Events['Updated Time'] >= window_start) &
                                                (Events['Updated Time'] < window_end)
                                                )]
                            upcoming = pd.concat([upcoming, df])
                            
                            upcoming.reset_index(drop = True, inplace = True)
                        
                        
                            # #upcoming refinement
                            # #for a scheduled, but unseen arrival, if the arrival OG is less
                            # #that the current time, assume the worst, make the arrival OG
                            # #equal to arrival OG + buffer
                            # #but, added a section that considers if we should be full worst case or not based on s_i of current vehicle versus the unseen late vehicle
                            # for row in range(0, len(upcoming)):
                            #     #is this a legal parked arrival that has not yet been seen?
                            #     if (upcoming.iloc[row]['Event Type'] == 'Arrival') and (upcoming.iloc[row]['Park Type OG'] == 'Legal Park') and (upcoming.iloc[row]['Park Type New'] == 'TBD'):
                            #         #was the planned arrival time before the current event time?
                            #         if upcoming.iloc[row]['a_i_OG'] < current_event['t_i']:
                                        
                            #             #does the unseen late arrival have a larger s_i than the current arrival?
                            #             #if so, be conservative and try to save the unseen late arrival by adding the 
                            #             #full buffer to the a_i_OG and d_i_OG
                            #             if upcoming.iloc[row]['s_i'] > current_event['s_i']:
                                            
                            #                 #if so, then make the expected arrival the worst case, add to the end of the buffer from the OG arrival time
                            #                 upcoming.loc[row, 'a_i_OG'] = upcoming.iloc[row]['a_i_OG'] + buffer
                            #                 upcoming.loc[row, 'd_i_OG'] = upcoming.iloc[row]['d_i_OG'] + buffer
                                            
                            #                 #need to update to the worst case departure time as well
                            #                 #what truck is currently arriving?
                            #                 DV = upcoming.iloc[row]['Truck']
                            #                 #what is the index in upcoming of the DV departure event
                            #                 DV_idx = np.where((upcoming['Truck'] == DV) & (upcoming['Event Type'] == 'Departure'))
                            #                 upcoming.loc[DV_idx[0], 'd_i_OG'] = upcoming.iloc[DV_idx]['d_i_OG'] + buffer
                            #                 upcoming.loc[DV_idx[0], 'a_i_OG'] = upcoming.iloc[DV_idx]['a_i_OG'] + buffer
                                            
                            #             else:
                            #                 #if the s_i of the unseen late arrival is less than the current arrival
                            #                 #we want to try to schedule the current arrival, so do not put in the worst case
                            #                 #scenario, instead just assign the expected arrival time of the unseen arrival to
                            #                 #the current event time
                            #                 upcoming.loc[row, 'a_i_OG'] = current_event['t_i']
                            #                 upcoming.loc[row, 'd_i_OG'] = current_event['t_i'] + upcoming.iloc[row]['s_i']
                                            
                            #                 #need to update to the worst case departure time as well
                            #                 #what truck is currently arriving?
                            #                 DV = upcoming.iloc[row]['Truck']
                            #                 #what is the index in upcoming of the DV departure event
                            #                 DV_idx = np.where((upcoming['Truck'] == DV) & (upcoming['Event Type'] == 'Departure'))
                            #                 upcoming.loc[DV_idx[0], 'd_i_OG'] = current_event['t_i'] + upcoming.iloc[row]['s_i']
                            #                 upcoming.loc[DV_idx[0], 'a_i_OG'] = current_event['t_i']
                            
                            #testing new upcoming refinement logic
                            for row in range(0, len(upcoming)):
                                #is this a legal parked arrival that has not yet been seen?
                                if (upcoming.iloc[row]['Event Type'] == 'Arrival') and (upcoming.iloc[row]['Park Type OG'] == 'Legal Park') and (upcoming.iloc[row]['Park Type New'] == 'TBD'):
                                    #was the planned arrival time before the current event time?
                                    if upcoming.iloc[row]['a_i_OG'] < current_event['t_i']:
                                    
                                        #if so, then make the expected arrival the worst case e.g. truck arrives at current time
                                        #and make the departure the worst case e.g. hold all the way through d_i_OG + buffer
                                        upcoming.loc[row, 'a_i_OG'] = current_event['t_i']
                                        upcoming.loc[row, 'd_i_OG'] = upcoming.iloc[row]['d_i_OG'] + buffer
                                        
                                        #need to update to the worst case departure time as well
                                        #what truck is currently arriving?
                                        DV = upcoming.iloc[row]['Truck']
                                        #what is the index in upcoming of the DV departure event
                                        DV_idx = np.where((upcoming['Truck'] == DV) & (upcoming['Event Type'] == 'Departure'))
                                        upcoming.loc[DV_idx[0], 'a_i_OG'] = current_event['t_i']
                                        upcoming.loc[DV_idx[0], 'd_i_OG'] = upcoming.iloc[DV_idx]['d_i_OG'] + buffer
        
        
                            #what does the final expected upcoming schedule look like?
                            #need to step through the upcoming sched and pull the relevant
                            #expected future time for each case, e.g. unseen arrival legal park, pull the a_i_OG
                            #post above worst case refinement, or for seen arrival legal park,
                            #pull the t_i from upcoming. One change is to be conservative
                            #with the upcoming, but unseen departures, go from d_i_OG + buffer
                            #this effectively may make the window of upcoming events longer
                            #making it more difficult to fit the current dbl parked truck
                            #that just arrived
                            upcoming.insert(7, 'Expected Time', None)
                            for row in range(0, len(upcoming)):
                                #unseen, legal park, arrival
                                if (upcoming.iloc[row]['Event Type'] == 'Arrival') & (upcoming.iloc[row]['Park Type OG'] == 'Legal Park') & (upcoming.iloc[row]['Park Type New'] == 'TBD'):
                                    upcoming.loc[row, 'Expected Time'] = upcoming.iloc[row]['a_i_OG']
                                #unseen, legal park, departure
                                if (upcoming.iloc[row]['Event Type'] == 'Departure') & (upcoming.iloc[row]['Park Type OG'] == 'Legal Park') & (upcoming.iloc[row]['Park Type New'] == 'TBD'):
                                    upcoming.loc[row, 'Expected Time'] = upcoming.iloc[row]['d_i_OG'] #+ buffer when the above section is added, the d_i_OG is already shifted by the buffer
                                #seen, dbl park to legal park departure
                                if (upcoming.iloc[row]['Event Type'] == 'Departure') & (upcoming.iloc[row]['Park Type OG'] == 'Dbl Park') & (upcoming.iloc[row]['Park Type New'] == 'Legal Park'):
                                    upcoming.loc[row, 'Expected Time'] = upcoming.iloc[row]['Updated Time']
                                #seen, legal park, arrival
                                if (upcoming.iloc[row]['Event Type'] == 'Arrival') & (upcoming.iloc[row]['Park Type OG'] == 'Legal Park') & (upcoming.iloc[row]['Park Type New'] == 'Legal Park'):
                                    upcoming.loc[row, 'Expected Time'] = upcoming.iloc[row]['Updated Time']
                                #seen, legal park, departure
                                if (upcoming.iloc[row]['Event Type'] == 'Departure') & (upcoming.iloc[row]['Park Type OG'] == 'Legal Park') & (upcoming.iloc[row]['Park Type New'] == 'Legal Park'):
                                    upcoming.loc[row, 'Expected Time'] = upcoming.iloc[row]['Updated Time']
                            
                            upcoming = upcoming.sort_values(by = ['Expected Time', 'Event Type'], ascending = [True, False], ignore_index = True)  
                            
                    
                            #now we can start counting out the future parking availability
                            parking_space_sched = []
                            parking_space_sched.append(parking_spaces_available)
                            parking_counter = parking_spaces_available
                            for row in range(0, len(upcoming)):
                                if upcoming.iloc[row]['Event Type'] == 'Arrival':
                                    if parking_counter != 0:
                                        parking_counter -= 1
                                        parking_space_sched.append(parking_counter)
                                    else:
                                        parking_space_sched.append(parking_counter)
                                        print('dbl park counter negative issue')
                                elif upcoming.iloc[row]['Event Type'] == 'Departure':
                                    if parking_counter != c:
                                        parking_counter += 1
                                        parking_space_sched.append(parking_counter)
                                    elif parking_counter == c:
                                        print('dbl park counter issue')
                                        
                                        
                            #are there any zeros in the upcoming parking space schedule?
                            #which would mean that there may not be space for the current truck
                            num_zeros = parking_space_sched.count(0)
                            if num_zeros == 0: #no issues parking the current delivery vehicle at the current event time, update the events schedule
                                #before assigning the delivery vehicle to legal park, make sure the arrival + service duration does not exceed the end of the scenario
                                if current_event['t_i'] + current_event['s_i'] > end:
                                    current_DV = current_event['Truck']
                                    Events.loc[r, 'Park Type New'] = 'Dbl Park'
                                    Events.loc[r, 'Updated Time'] = current_event['t_i']
                                    Events.at[r, 'Park Type New'] = 'Dbl Park'
                                    Events.at[r, 'Updated Time'] = current_event['t_i']
                                    #same update for the departure event
                                    depart_idx = np.where((Events['Truck'] == current_DV) & (Events['Event Type'] == 'Departure'))
                                    Events.loc[depart_idx[0], 'Park Type New'] = 'Dbl Park'
                                    Events.loc[depart_idx[0], 'Updated Time'] = current_event['t_i'] + current_event['s_i']
                                    Events.at[depart_idx[0][0], 'Park Type New'] = 'Dbl Park'
                                    Events.at[depart_idx[0][0], 'Updated Time'] = current_event['t_i'] + current_event['s_i']
                                    r += 1
                                else:                          
                                    current_DV = current_event['Truck']
                                    Events.loc[r, 'Park Type New'] = 'Legal Park'
                                    Events.loc[r, 'Updated Time'] = current_event['t_i']
                                    Events.at[r, 'Park Type New'] = 'Legal Park'
                                    Events.at[r, 'Updated Time'] = current_event['t_i']
                                    #same update for the departure event
                                    depart_idx = np.where((Events['Truck'] == current_DV) & (Events['Event Type'] == 'Departure'))
                                    Events.loc[depart_idx[0], 'Park Type New'] = 'Legal Park'
                                    Events.loc[depart_idx[0], 'Updated Time'] = current_event['t_i'] + current_event['s_i']
                                    Events.at[depart_idx[0][0], 'Park Type New'] = 'Legal Park'
                                    Events.at[depart_idx[0][0], 'Updated Time'] = current_event['t_i'] + current_event['s_i']
                                    #remove one parking space before heading to the next event in the schedule
                                    parking_spaces_available -= 1
                                    r += 1
                            
                            #if there is atleast 1 instance of zero in the upcoming schedule
                            #then, double park the the arriving delivery vehicle, do not need
                            #to search for possible start times because the window is only
                            #as long as the service duration and we assume that an originally
                            #double parked truck will not wait for a parking space
                            else:
                                #dbl park
                                current_DV = current_event['Truck']
                                Events.loc[r, 'Park Type New'] = 'Dbl Park'
                                Events.loc[r, 'Updated Time'] = current_event['t_i']
                                Events.at[r, 'Park Type New'] = 'Dbl Park'
                                Events.at[r, 'Updated Time'] = current_event['t_i']
                                #same update for the departure event
                                depart_idx = np.where((Events['Truck'] == current_DV) & (Events['Event Type'] == 'Departure'))
                                Events.loc[depart_idx[0], 'Park Type New'] = 'Dbl Park'
                                Events.loc[depart_idx[0], 'Updated Time'] = current_event['t_i'] + current_event['s_i']
                                Events.at[depart_idx[0][0], 'Park Type New'] = 'Dbl Park'
                                Events.at[depart_idx[0][0], 'Updated Time'] = current_event['t_i'] + current_event['s_i']
                                r += 1
                                
                            
            
            
            
            #is the current event a departure
            elif current_event['Event Type'] == 'Departure':
                
                #not a lot of logic in this section because the arrival event for a specific delivery vehicle
                #will always be processed first and the departure will be updated at the
                #same time
                
                #is the current event a legal park departure?
                if current_event['Park Type New'] == 'Legal Park':
                    parking_spaces_available += 1
                    r += 1
                
                #or is it a double park departure?
                elif current_event['Park Type New'] == 'Dbl Park':
                    r += 1
                    
                
                
            
            

            
                
        #Verification metrics to track how the parking schedule changes before
        #and after reassessing
        
        OG_dbl_parking = OG_shift_sched[(OG_shift_sched['Park Type'] == 'Dbl Park')]
        OG_sum = np.sum(OG_dbl_parking['s_i'])        
                
        New_dbl_parking = Events[(Events['Event Type'] == 'Arrival') & (Events['Park Type New'] == 'Dbl Park')]
        New_sum = np.sum(New_dbl_parking['s_i'])          
                
        #print('Reduction in dbl parking: ', OG_sum - New_sum)
                
        Dbl_to_Legal = Events[(Events['Event Type'] == 'Arrival') & (Events['Park Type OG'] == 'Dbl Park') & (Events['Park Type New'] == 'Legal Park')]
        dbl_to_legal_sum = np.sum(Dbl_to_Legal['s_i'])       
        
        Legal_to_Dbl_lost_resv = Events[Events['Lost Reservation'] == 'Yes']
        Legal_to_Dbl = Events[(Events['Park Type OG'] == 'Legal Park') & (Events['Park Type New'] == 'Dbl Park')]
        legal_to_dbl_sum = np.sum(Legal_to_Dbl['s_i'] + Legal_to_Dbl_lost_resv['s_i'])
        
        #print('Change in double parking: ', dbl_to_legal_sum - legal_to_dbl_sum)
        
        change_sum_dbl_parking.append([c, i, OG_sum, New_sum, OG_sum - New_sum])
        change_legal_and_dbl.append([c, i, dbl_to_legal_sum, legal_to_dbl_sum, dbl_to_legal_sum - legal_to_dbl_sum])
        #print('stop')
        
        
        #add the waiting for possible starts dbl parking events to the Events df and re-sort based on updated_time
        Events = pd.concat([Events, Events_dbl_park_wait_poss_start], ignore_index = True)
        Events = Events.sort_values(by = ['Updated Time', 'Event Type'], ascending = [True, False], ignore_index = True)
        
        
        #take the reassessed parking schedule and reformat into park events and dbl park events
        Event_arrivals = Events[Events['Event Type'] == 'Arrival']
        park_events_df_inst_phi5 = Event_arrivals[['Truck', 'Updated Time', 's_i', 'Park Type New']] 
        d_i = park_events_df_inst_phi5['Updated Time'] + park_events_df_inst_phi5['s_i'] 
        park_events_df_inst_phi5.insert(3, 'd_i', d_i) 
        park_events_df_inst_phi5 = park_events_df_inst_phi5.rename(columns = {'Updated Time': 'a_i', 'Park Type New': 'Park Type'}) 
        park_events_df_inst_phi5_lst.append(park_events_df_inst_phi5) 
        
        
        dbl_park_events_df_inst_phi5 = park_events_df_inst_phi5[park_events_df_inst_phi5['Park Type'] == 'Dbl Park'] 
        dbl_park_events_df_inst_phi5.drop(columns = ['Park Type'], inplace = True)
        dbl_park_events_df_inst_phi5_lst.append(dbl_park_events_df_inst_phi5) 
        
        
    #store the set of iteration park event dataframes in a larger dataframe, before incrementing to the next parking space, c
    dbl_park_events_df_inst_phi5_df[c] = dbl_park_events_df_inst_phi5_lst 
    park_events_df_inst_phi5_df[c] = park_events_df_inst_phi5_lst 
        
        
        
toc = time.time()

runtime = toc-tic
print('runtime: ' + str(runtime))
        
            
# with open('pub_Pitt_reassessed_phi5_27_Nov_2022_buffer_5.pkl', 'wb') as file: 
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
#           Events,
#           Events_dbl_park_wait_poss_start,
#           late_no_starts_1,
#           late_no_starts_more_1,
#           early_no_starts_1,
#           early_no_starts_more_1,
#           change_sum_dbl_parking,
#           change_legal_and_dbl
#           ],
#             file)












            
