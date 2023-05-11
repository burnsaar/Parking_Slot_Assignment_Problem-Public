# -*- coding: utf-8 -*-
"""
Created on Sat Nov 27 15:52:13 2021

@author: Burns
"""

import numpy as np
import pandas as pd
import pickle
import time
from scipy.optimize import fsolve
import scipy.integrate as integrate

import warnings
warnings.filterwarnings("ignore")

tic = time.time()


# with open('pub_Aspen_net_dbl_parking_1_Dec_2022_buffer_5.pkl', 'rb') as file:
#     net_dbl_park_events_df_inst_FCFS, \
#     net_dbl_park_events_df_inst_phi5, \
#     max_parking_spaces, \
#     iterations\
#         = pickle.load(file)
        
# file.close()

with open('pub_Pitt_net_dbl_parking_2_Dec_2022_buffer_5.pkl', 'rb') as file:
    net_dbl_park_events_df_inst_FCFS, \
    net_dbl_park_events_df_inst_phi5, \
    max_parking_spaces, \
    iterations\
        = pickle.load(file)
        
file.close()

    

def piece(x, A_rate, D_rate, D_rate_dbl_park, df, Max_Q, len_scenario):
    from scipy.optimize import fsolve
    
    queue_buildup_rate = (A_rate) - (D_rate_dbl_park)
    
    #create a location to store the start and stop x values for each function in the piecewise equation
    points = pd.DataFrame(columns = ['Start_x', 'Stop_x'])

    
    #capture the case where the arrival rate is always less than either departure rates
    #e.g. the optimistic scenario
    if queue_buildup_rate < 0:
        funclist = [lambda x: x*A_rate]
        condlist = [(x >= 0) and (x <= len_scenario)]
        # points.iloc[-1]['Start_x'] = 0
        # points.iloc[-1]['Stop_x'] = len_scenario
        #points.loc[len(points.index)] = [0, len_scenario]
        
        queue_duration = [0]
        t_queue_remove = [0]
        
        val = np.piecewise(x, condlist, funclist)
               
        return val, queue_duration, t_queue_remove, points, condlist, funclist
        

    
    # if df.empty == True:
    #     func = lambda x: x*A_rate
    #     queue_duration = 0
    #     t_queue_remove = 0
        
    #     return func, queue_duration, t_queue_remove
    
    
    funclist = []
    condlist = []
    #set piecewise equation equal to the arrival rate until the first double parking event
    condlist.append((x >= 0) and (x < df.iloc[0]['Start']))
    funclist.append(lambda x: x*A_rate)
    # points.iloc[-1]['Start_x'] = 0
    # points.iloc[-1]['Stop_x'] = df.iloc[0]['Start']
    points.loc[len(points.index)] = [0, df.iloc[0]['Start']]
    
    
    
    
    if len(df) == 1:
        #first check to see if we will exceed the max queue length over this
        #net double parking event
        #if we will note exceed the max queue length, proceed as normal
        if df.iloc[0]['Total'] * queue_buildup_rate < Max_Q:
        
            condlist.append((x >= df.iloc[0]['Start']) and (x < df.iloc[0]['End']))
            funclist.append(lambda x: x*D_rate_dbl_park + (A_rate*df.iloc[0]['Start']) - (df.iloc[0]['Start']*D_rate_dbl_park))
            # points.iloc[-1]['Start_x'] = df.iloc[0]['Start']
            # points.iloc[-1]['Stop_x'] = df.iloc[0]['End']
            points.loc[len(points.index)] = [df.iloc[0]['Start'], df.iloc[0]['End']]
            
            
            #where does the previous equation end in the y value (number of trucks departed, will be less than those arrived)
            end_pt = df.iloc[0]['End']*D_rate_dbl_park + (A_rate*df.iloc[0]['Start']) - (df.iloc[0]['Start']*D_rate_dbl_park)
            
            start_point = ()
            points
            
            #lets determine how long it takes to dissapated the queue
            #new segment function with faster departures
            depart = lambda x: x*D_rate + end_pt - (df.iloc[0]['End']*D_rate)
            #need to compare departures to the overall number of trucks that have arrived
            arrivals = lambda x: x*A_rate
            #when que_remove = 0, the que has disappaited
            queue_remove = lambda x: arrivals(x) - depart(x)
            t_queue_remove = fsolve(queue_remove, [0], epsfcn = 0.001)
            
            
            condlist.append((x >= df.iloc[0]['End']) and (x < t_queue_remove[0]))
            funclist.append(depart)
            # points.iloc[-1]['Start_x'] = df.iloc[0]['End']
            # points.iloc[-1]['Stop_x'] = t_queue_remove[0]
            points.loc[len(points.index)] = [df.iloc[0]['End'], t_queue_remove[0]]
            
            #add in a default value for the set of functions, set equal to the arrival rate
            #so that no queue will be added and it will be easier to execute the integral
            #b/c we don't need to know the start and stop duration, can integrate over the scenario window
            funclist.append(lambda x: x*A_rate)
            condlist.append((x >= t_queue_remove[0]) and (x <= len_scenario))
            # points.iloc[-1]['Start_x'] = t_queue_remove[0]
            # points.iloc[-1]['Stop_x'] = len_scenario
            points.loc[len(points.index)] = [t_queue_remove[0], len_scenario]
            
            val = np.piecewise(x, condlist, funclist)
        
            queue_duration = t_queue_remove - df.iloc[0]['Start']
          
            return val, queue_duration, t_queue_remove, points, condlist, funclist
    
    
        #we will exceed the max queue length over this net dbl park event            
        elif df.iloc[0]['Total'] * queue_buildup_rate >= Max_Q:
            #how many minutes until the queue reaches max length
            max_queue_pt = Max_Q / queue_buildup_rate
            
            #record the dbl parking departure rate from start through max_queue_pt
            condlist.append((x >= df.iloc[0]['Start']) and (x < df.iloc[0]['Start'] +max_queue_pt))
            funclist.append(lambda x: x*D_rate_dbl_park + (A_rate*df.iloc[0]['Start']) - (D_rate_dbl_park*df.iloc[0]['Start']))
            # points.iloc[-1]['Start_x'] = df.iloc[0]['Start']
            # points.iloc[-1]['Stop_x'] = df.iloc[0]['Start'] +max_queue_pt
            points.loc[len(points.index)] = [df.iloc[0]['Start'], df.iloc[0]['Start'] +max_queue_pt]
            
            
            #record the constant queue length equation which is equivalent to
            #the A_rate*x - Max_Q, we want a parallel line shifted downward
            #by Max_Q
            condlist.append((x >= df.iloc[0]['Start'] +max_queue_pt) and (x < df.iloc[0]['End']))
            funclist.append(lambda x: x*A_rate - Max_Q)
            # points.iloc[-1]['Start_x'] = df.iloc[0]['Start'] +max_queue_pt
            # points.iloc[-1]['Stop_x'] = df.iloc[0]['End']
            points.loc[len(points.index)] = [df.iloc[0]['Start'] +max_queue_pt, df.iloc[0]['End']]

            end_pt = df.iloc[0]['End']*A_rate - Max_Q   
    
    
            #lets determine how long it takes to dissapated the queue
            #new segment function with faster departures
            depart = lambda x: x*D_rate + end_pt - (df.iloc[0]['End']*D_rate)
            #need to compare departures to the overall number of trucks that have arrived
            arrivals = lambda x: x*A_rate
            #when que_remove = 0, the que has disappaited
            queue_remove = lambda x: arrivals(x) - depart(x)
            t_queue_remove = fsolve(queue_remove, [0], epsfcn = 0.001)
            
            
            condlist.append((x >= df.iloc[0]['End']) and (x < t_queue_remove[0]))
            funclist.append(depart)
            # points.iloc[-1]['Start_x'] = df.iloc[0]['End']
            # points.iloc[-1]['Stop_x'] = t_queue_remove[0]
            points.loc[len(points.index)] = [df.iloc[0]['End'], t_queue_remove[0]]
            
            #add in a default value for the set of functions, set equal to the arrival rate
            #so that no queue will be added and it will be easier to execute the integral
            #b/c we don't need to know the start and stop duration, can integrate over the scenario window
            funclist.append(lambda x: x*A_rate)
            condlist.append((x >= t_queue_remove[0]) and (x <= len_scenario))
            # points.iloc[-1]['Start_x'] = t_queue_remove[0]
            # points.iloc[-1]['Stop_x'] = len_scenario
            points.loc[len(points.index)] = [t_queue_remove[0], len_scenario]
            
            val = np.piecewise(x, condlist, funclist)
        
            queue_duration = t_queue_remove - df.iloc[0]['Start']
          
            return val, queue_duration, t_queue_remove, points, condlist, funclist   
    
    
    
    else:
        queue_present_flag = 0
        queue_duration = []
        
        for row in range(0, len(df)):
            #we do not have a residual queue from the previous dbl park event and return to normal
            if queue_present_flag == 0:
                #first check to see if we will exceed the max queue length over this
                #net double parking event
                #if we will not exceed the max queue length, proceed as normal
                if df.iloc[row]['Total'] * queue_buildup_rate < Max_Q:
                
                    #bounds and rate function over the dbl parking event window
                    condlist.append((x >= df.iloc[row]['Start']) and (x < df.iloc[row]['End']))
                    funclist.append(lambda x, row=row: x*D_rate_dbl_park + (A_rate*df.iloc[row]['Start']) - (D_rate_dbl_park*df.iloc[row]['Start']))
                    # points.iloc[-1]['Start_x'] = df.iloc[row]['Start']
                    # points.iloc[-1]['Stop_x'] = df.iloc[row]['End']
                    points.loc[len(points.index)] = [df.iloc[row]['Start'], df.iloc[row]['End']]
                    
                    end_pt = df.iloc[row]['End']*D_rate_dbl_park + (A_rate*df.iloc[row]['Start']) - (D_rate_dbl_park*df.iloc[row]['Start'])
                
                    #after the dbl parking event, how quickly do we return
                    #new segment function with faster departures
                    depart = lambda x, row=row, end_pt=end_pt: x*D_rate + end_pt - df.iloc[row]['End']*D_rate
                    #need to compare departures to the overall number of trucks that have arrived
                    arrivals = lambda x: x*A_rate
                    #when queue_remove = 0, the queue has disappaited
                    queue_remove = lambda x, row=row, end_pt=end_pt: arrivals(x) - depart(x)
                    t_queue_remove = fsolve(queue_remove, [0], epsfcn = 0.001)
                
                
                    #are you on the last row of the dbl park events?
                    if row == len(df) -1:
                        #record when the queue will dissapate
                        condlist.append((x >= df.iloc[row]['End']) and (x < t_queue_remove[0]))
                        funclist.append(depart)
                        # points.iloc[-1]['Start_x'] = df.iloc[row]['End']
                        # points.iloc[-1]['Stop_x'] = t_queue_remove[0]
                        points.loc[len(points.index)] = [df.iloc[row]['End'], t_queue_remove[0]]
                    
                        queue_duration.append(t_queue_remove - df.iloc[row]['Start'])
                    
                    #we are not on the last row of the dbl park events
                    else:
                        #does the queue dissapate before the next dbl park event?
                        if t_queue_remove <= df.iloc[row +1]['Start']:
                            #split the time normal departure rate into two section, one for 
                            #the normal departure rate and once the queue disappates the function
                            #should be the same as the arrival rate
                            condlist.append((x >= df.iloc[row]['End'] and (x < t_queue_remove)))
                            funclist.append(depart)
                            # points.iloc[-1]['Start_x'] = df.iloc[row]['End']
                            # points.iloc[-1]['Stop_x'] = t_queue_remove[0]
                            points.loc[len(points.index)] = [df.iloc[row]['End'], t_queue_remove[0]]
                            
                            condlist.append((x >= t_queue_remove) and (x < df.iloc[row +1]['Start']))
                            funclist.append(arrivals)
                            # points.iloc[-1]['Start_x'] = t_queue_remove[0]
                            # points.iloc[-1]['Stop_x'] = df.iloc[row +1]['Start']
                            points.loc[len(points.index)] = [t_queue_remove[0], df.iloc[row +1]['Start']]
                            
                            queue_present_flag = 0
                            
                            #we started without and queue and remove the queue before the next
                            #double parking event, record the time in between
                            queue_duration.append(t_queue_remove - df.iloc[row]['Start'])
                    
                    
                        elif t_queue_remove > df.iloc[row +1]['Start']:
                            #no need to split the normal departure rate section, so store
                            #just a single set of conditions and a function.  We do need to record
                            #the end point for the depart function at the start of the next 
                            #double parking event as this will impact the y-intercept of the
                            #next equation
                            condlist.append((x >= df.iloc[row]['End']) and (x < df.iloc[row +1]['Start']))                
                            funclist.append(depart)
                            # points.iloc[-1]['Start_x'] = df.iloc[row]['End']
                            # points.iloc[-1]['Stop_x'] = df.iloc[row +1]['Start']
                            points.loc[len(points.index)] = [df.iloc[row]['End'], df.iloc[row +1]['Start']]
                            
                            new_end_pt = depart(df.iloc[row +1]['Start'])
                            queue_present_flag = 1
                            
                            #even though the queue isn't removed by the start of the next dbl
                            #park event, this is one way to capture the time in queue and
                            #then do this each time a queue is present
                            queue_duration.append(df.iloc[row +1]['Start'] - df.iloc[row]['Start'])
                
                #we will exceed the max queue length over this net dbl park event            
                elif df.iloc[row]['Total'] * queue_buildup_rate >= Max_Q:
                    #how many minutes until the queue reaches max length
                    max_queue_pt = Max_Q / queue_buildup_rate
                    
                    #record the dbl parking departure rate from start through max_queue_pt
                    condlist.append((x >= df.iloc[row]['Start']) and (x < df.iloc[row]['Start'] +max_queue_pt))
                                                        #update the slope    #where are you currently        #remove the contribution to the same location w/ the new slope
                    funclist.append(lambda x, row=row: x*D_rate_dbl_park + (A_rate*df.iloc[row]['Start']) - (D_rate_dbl_park*df.iloc[row]['Start']))
                    # points.iloc[-1]['Start_x'] = df.iloc[row]['Start']
                    # points.iloc[-1]['Stop_x'] = df.iloc[row]['Start'] +max_queue_pt
                    points.loc[len(points.index)] = [df.iloc[row]['Start'], df.iloc[row]['Start'] +max_queue_pt]
                    
                    #record the constant queue length equation which is equivalent to
                    #the A_rate*x - Max_Q, we want a parallel line shifted downward
                    #by Max_Q
                    condlist.append((x >= df.iloc[row]['Start'] +max_queue_pt) and (x < df.iloc[row]['End']))
                    funclist.append(lambda x, row=row: x*A_rate - Max_Q)
                    # points.iloc[-1]['Start_x'] = df.iloc[row]['Start'] +max_queue_pt
                    # points.iloc[-1]['Stop_x'] = df.iloc[row]['End']
                    points.loc[len(points.index)] = [df.iloc[row]['Start'] +max_queue_pt, df.iloc[row]['End']]
    
                    end_pt = df.iloc[row]['End']*A_rate - Max_Q
                
                    #after the dbl parking event, how quickly do we return
                    #new segment function with faster departures
                    depart = lambda x, row=row, end_pt=end_pt: x*D_rate + end_pt - df.iloc[row]['End']*D_rate
                    #need to compare departures to the overall number of trucks that have arrived
                    arrivals = lambda x: x*A_rate
                    #when queue_remove = 0, the queue has disappaited
                    queue_remove = lambda x, row=row, end_pt=end_pt: arrivals(x) - depart(x)
                    t_queue_remove = fsolve(queue_remove, [0], epsfcn = 0.001)
    
    
                    #are you on the last row of the dbl park events?
                    if row == len(df) -1:
                        #record when the queue will dissapate
                        condlist.append((x >= df.iloc[row]['End']) and (x < t_queue_remove[0]))
                        funclist.append(depart)
                        # points.iloc[-1]['Start_x'] = df.iloc[row]['End']
                        # points.iloc[-1]['Stop_x'] = t_queue_remove[0]
                        points.loc[len(points.index)] = [df.iloc[row]['End'], t_queue_remove[0]]
                    
                        queue_duration.append(t_queue_remove - df.iloc[row]['Start'])    
    
                    #we are not on the last row of the dbl park events
                    else:
                        #does the queue dissapate before the next dbl park event?
                        if t_queue_remove <= df.iloc[row +1]['Start']:
                            #split the time normal departure rate into two section, one for 
                            #the normal departure rate and once the queue disappates the function
                            #should be the same as the arrival rate
                            condlist.append((x >= df.iloc[row]['End'] and (x < t_queue_remove)))
                            funclist.append(depart)
                            # points.iloc[-1]['Start_x'] = df.iloc[row]['End']
                            # points.iloc[-1]['Stop_x'] = t_queue_remove[0]
                            points.loc[len(points.index)] = [df.iloc[row]['End'], t_queue_remove[0]]
                            
                            condlist.append((x >= t_queue_remove) and (x < df.iloc[row +1]['Start']))
                            funclist.append(arrivals)
                            # points.iloc[-1]['Start_x'] = t_queue_remove[0]
                            # points.iloc[-1]['Stop_x'] = df.iloc[row +1]['Start']
                            points.loc[len(points.index)] = [t_queue_remove[0], df.iloc[row +1]['Start']]
                            
                            queue_present_flag = 0
                            
                            #we started without and queue and remove the queue before the next
                            #double parking event, record the time in between
                            queue_duration.append(t_queue_remove - df.iloc[row]['Start'])
                    
                    
                        elif t_queue_remove > df.iloc[row +1]['Start']:
                            #no need to split the normal departure rate section, so store
                            #just a single set of conditions and a function.  We do need to record
                            #the end point for the depart function at the start of the next 
                            #double parking event as this will impact the y-intercept of the
                            #next equation
                            condlist.append((x >= df.iloc[row]['End']) and (x < df.iloc[row +1]['Start']))                
                            funclist.append(depart)
                            # points.iloc[-1]['Start_x'] = df.iloc[row]['End']
                            # points.iloc[-1]['Stop_x'] = df.iloc[row +1]['Start']
                            points.loc[len(points.index)] = [df.iloc[row]['End'], df.iloc[row +1]['Start']]
                            
                            new_end_pt = depart(df.iloc[row +1]['Start'])
                            queue_present_flag = 1
                            
                            #even though the queue isn't removed by the start of the next dbl
                            #park event, this is one way to capture the time in queue and
                            #then do this each time a queue is present
                            queue_duration.append(df.iloc[row +1]['Start'] - df.iloc[row]['Start'])    
    
    
    
    
    
            elif queue_present_flag == 1:
                
                #How long is the current queue?  new_end_pt is the y-value of the residual queue
                current_Q = df.iloc[row]['Start']*A_rate - new_end_pt
  
                #check to see if we will exceed the max queue length over this
                #net double parking event
                #if we will not exceed the max queue length, proceed as normal
                if df.iloc[row]['Total'] * queue_buildup_rate < Max_Q - current_Q:
                
      
                    #we may have a queue, but the start of the double parking event does not change
                    condlist.append((x >= df.iloc[row]['Start']) and (x < df.iloc[row]['End']))
                    #the function however will have a slightly lower y-intercept due to the queue
                    #the impact of which is captured by new_end_pt
                    funclist.append(lambda x, row=row, new_end_pt=new_end_pt: x*D_rate_dbl_park + (new_end_pt) - (D_rate_dbl_park*df.iloc[row]['Start']))
                    # points.iloc[-1]['Start_x'] = df.iloc[row]['Start']
                    # points.iloc[-1]['Stop_x'] = df.iloc[row]['End']
                    points.loc[len(points.index)] = [df.iloc[row]['Start'], df.iloc[row]['End']]
                    
                    end_pt = df.iloc[row]['End']*D_rate_dbl_park + (new_end_pt) - (D_rate_dbl_park*df.iloc[row]['Start'])
        
                    #after the dbl parking event, how quickly do we return
                    #new segment function with faster departures
                    depart = lambda x, row=row, end_pt=end_pt: x*D_rate + end_pt - df.iloc[row]['End']*D_rate
                    #need to compare departures to the overall number of trucks that have arrived
                    arrivals = lambda x: x*A_rate
                    #when que_remove = 0, the que has disappaited
                    queue_remove = lambda x, row=row, end_pt=end_pt: arrivals(x) - depart(x)
                    t_queue_remove = fsolve(queue_remove, [0], epsfcn = 0.001)
        
        
                    #are you on the last row of the dbl park events?
                    if row == len(df) -1:
                        #record when the queue will dissapate
                        condlist.append((x >= df.iloc[row]['End']) and (x < t_queue_remove[0]))
                        funclist.append(depart)
                        # points.iloc[-1]['Start_x'] = df.iloc[row]['End']
                        # points.iloc[-1]['Stop_x'] = t_queue_remove[0]
                        points.loc[len(points.index)] = [df.iloc[row]['End'], t_queue_remove[0]]
                        
                        queue_duration.append(t_queue_remove - df.iloc[row]['Start'])
                        
                    #we are not on the last row of the dbl park events
                    else:
                        #does the queue dissapate before the next dbl park event?
                        if t_queue_remove <= df.iloc[row +1]['Start']:
                            #split the time normal departure rate into two section, one for 
                            #the normal departure rate and once the queue disappates the function
                            #should be the same as the arrival rate
                            condlist.append((x >= df.iloc[row]['End'] and (x < t_queue_remove)))
                            funclist.append(depart)
                            # points.iloc[-1]['Start_x'] = df.iloc[row]['End']
                            # points.iloc[-1]['Stop_x'] = t_queue_remove[0]
                            points.loc[len(points.index)] = [df.iloc[row]['End'], t_queue_remove[0]]
                            
                            condlist.append((x >= t_queue_remove) and (x < df.iloc[row +1]['Start']))
                            funclist.append(arrivals)
                            # points.iloc[-1]['Start_x'] = t_queue_remove[0]
                            # points.iloc[-1]['Stop_x'] = df.iloc[row +1]['Start']
                            points.loc[len(points.index)] = [t_queue_remove[0], df.iloc[row +1]['Start']]
                            
                            queue_present_flag = 0
                            
                            #eventhough we started with a queue, this length of time has already
                            #been recorded, so just record the new additional queue time
                            queue_duration.append(t_queue_remove - df.iloc[row]['Start'])
            
                        elif t_queue_remove > df.iloc[row +1]['Start']:
                            #no need to split the normal departure rate section, so store
                            #just a single set of conditions and a function.  We do need to record
                            #the end point for the depart function at the start of the next 
                            #double parking event as this will impact the y-intercept of the
                            #next equation
                            condlist.append((x >= df.iloc[row]['End']) and (x < df.iloc[row +1]['Start']))                
                            funclist.append(depart)
                            # points.iloc[-1]['Start_x'] = df.iloc[row]['End']
                            # points.iloc[-1]['Stop_x'] = df.iloc[row +1]['Start']
                            points.loc[len(points.index)] = [df.iloc[row]['End'], df.iloc[row +1]['Start']]
                            
                            new_end_pt = depart(df.iloc[row +1]['Start'])
                            queue_present_flag = 1
                            
                            #eventhough we started with a queue, this length of time has already
                            #been recorded, so just record the new additional queue time
                            queue_duration.append(df.iloc[row +1]['Start'] - df.iloc[row]['Start'])
        

                #we will exceed the max queue length over this net dbl park event 
                elif df.iloc[row]['Total'] * queue_buildup_rate >= Max_Q - current_Q:        
    
                    #how many minutes until the queue reaches max length
                    max_queue_pt = (Max_Q - current_Q) / queue_buildup_rate
    
                    #record the dbl parking departure rate from start through max_queue_pt
                    condlist.append((x >= df.iloc[row]['Start']) and (x < df.iloc[row]['Start'] +max_queue_pt))
                    funclist.append(lambda x, row=row, new_end_pt=new_end_pt: x*D_rate_dbl_park + (new_end_pt) - (D_rate_dbl_park*df.iloc[row]['Start']))
                    # points.iloc[-1]['Start_x'] = df.iloc[row]['Start']
                    # points.iloc[-1]['Stop_x'] = df.iloc[row]['Start'] +max_queue_pt
                    points.loc[len(points.index)] = [df.iloc[row]['Start'], df.iloc[row]['Start'] +max_queue_pt]
                    
                    #record the constant queue length equation which is equivalent to
                    #the A_rate*x - Max_Q, we want a parallel line shifted downward
                    #by Max_Q
                    condlist.append((x >= df.iloc[row]['Start'] +max_queue_pt) and (x < df.iloc[row]['End']))
                    funclist.append(lambda x, row=row: x*A_rate - Max_Q)
                    # points.iloc[-1]['Start_x'] = df.iloc[row]['Start'] +max_queue_pt
                    # points.iloc[-1]['Stop_x'] = df.iloc[row]['End']
                    points.loc[len(points.index)] = [df.iloc[row]['Start'] +max_queue_pt, df.iloc[row]['End']]
    
                    end_pt = df.iloc[row]['End']*A_rate - Max_Q
                    
                    #after the dbl parking event, how quickly do we return
                    #new segment function with faster departures
                    depart = lambda x, row=row, end_pt=end_pt: x*D_rate + end_pt - df.iloc[row]['End']*D_rate
                    #need to compare departures to the overall number of trucks that have arrived
                    arrivals = lambda x: x*A_rate
                    #when que_remove = 0, the que has disappaited
                    queue_remove = lambda x, row=row, end_pt=end_pt: arrivals(x) - depart(x)
                    t_queue_remove = fsolve(queue_remove, [0], epsfcn = 0.001)
        
        
                    #are you on the last row of the dbl park events?
                    if row == len(df) -1:
                        #record when the queue will dissapate
                        condlist.append((x >= df.iloc[row]['End']) and (x < t_queue_remove[0]))
                        funclist.append(depart)
                        # points.iloc[-1]['Start_x'] = df.iloc[row]['End']
                        # points.iloc[-1]['Stop_x'] = t_queue_remove[0]
                        points.loc[len(points.index)] = [df.iloc[row]['End'], t_queue_remove[0]]
                        
                        queue_duration.append(t_queue_remove - df.iloc[row]['Start'])
                        
                    #we are not on the last row of the dbl park events
                    else:
                        #does the queue dissapate before the next dbl park event?
                        if t_queue_remove <= df.iloc[row +1]['Start']:
                            #split the time normal departure rate into two section, one for 
                            #the normal departure rate and once the queue disappates the function
                            #should be the same as the arrival rate
                            condlist.append((x >= df.iloc[row]['End'] and (x < t_queue_remove)))
                            funclist.append(depart)
                            # points.iloc[-1]['Start_x'] = df.iloc[row]['End']
                            # points.iloc[-1]['Stop_x'] = t_queue_remove[0]
                            points.loc[len(points.index)] = [df.iloc[row]['End'], t_queue_remove[0]]
                            
                            condlist.append((x >= t_queue_remove) and (x < df.iloc[row +1]['Start']))
                            funclist.append(arrivals)
                            # points.iloc[-1]['Start_x'] = t_queue_remove[0]
                            # points.iloc[-1]['Stop_x'] = df.iloc[row +1]['Start']
                            points.loc[len(points.index)] = [t_queue_remove[0], df.iloc[row +1]['Start']]
                            
                            queue_present_flag = 0
                            
                            #eventhough we started with a queue, this length of time has already
                            #been recorded, so just record the new additional queue time
                            queue_duration.append(t_queue_remove - df.iloc[row]['Start'])
            
                        elif t_queue_remove > df.iloc[row +1]['Start']:
                            #no need to split the normal departure rate section, so store
                            #just a single set of conditions and a function.  We do need to record
                            #the end point for the depart function at the start of the next 
                            #double parking event as this will impact the y-intercept of the
                            #next equation
                            condlist.append((x >= df.iloc[row]['End']) and (x < df.iloc[row +1]['Start']))                
                            funclist.append(depart)
                            # points.iloc[-1]['Start_x'] = df.iloc[row]['End']
                            # points.iloc[-1]['Stop_x'] = df.iloc[row +1]['Start']
                            points.loc[len(points.index)] = [df.iloc[row]['End'], df.iloc[row +1]['Start']]
                            
                            new_end_pt = depart(df.iloc[row +1]['Start'])
                            queue_present_flag = 1
                            
                            #eventhough we started with a queue, this length of time has already
                            #been recorded, so just record the new additional queue time
                            queue_duration.append(df.iloc[row +1]['Start'] - df.iloc[row]['Start'])                    
                   
    
        #add in a default value for the set of functions, set equal to the arrival rate
        #so that no queue will be added and it will be easier to execute the integral
        #b/c we don't need to know the start and stop duration, can integrate over the scenario window
        funclist.append(lambda x: x*A_rate)
        condlist.append((x >= t_queue_remove[0]) and (x <= len_scenario))
        # points.iloc[-1]['Start_x'] = t_queue_remove[0]
        # points.iloc[-1]['Stop_x'] = len_scenario
        points.loc[len(points.index)] = [t_queue_remove[0], len_scenario]
        
        val = np.piecewise(x, condlist, funclist)
        
        return val, sum(queue_duration), t_queue_remove, points, condlist, funclist
    
    

    
#traffic input parameters
A_rate_hr = 1833 #(veh/hr)
D_rate_hr = 2136 #(veh/hr)
D_rate_dbl_park_hr = 534 #departure rate when double parking is present

A_rate = A_rate_hr / 60 #veh/min
D_rate = D_rate_hr / 60 #veh/min
D_rate_dbl_park = D_rate_dbl_park_hr / 60

len_scenario = 1200 #660 min for Aspen, 1200 for Pitt

Max_Q = 30

#x = 0.00

# df = pd.DataFrame({'Start':[5, 30], 'End':[25, 35], 'Total':[20, 5]})
# # #df = pd.DataFrame({'Start':[5, 20, 45], 'End':[15, 25, 50], 'Total':[10, 5, 5]})
# df = pd.DataFrame({'Start':[5], 'End':[10], 'Total':[5]})
# df = pd.DataFrame({'Start':[5, 30], 'End':[10, 35], 'Total':[5, 5]})

# [func, queue_duration, t_queue_remove] = piece(x, A_rate, D_rate, D_rate_dbl_park, df, Max_Q)



#FCFS
net_dbl_park_minutes_df_inst_FCFS = pd.DataFrame(index = range(0, iterations), columns = [1, 2, 3, 4, 5, 6, 7], dtype = object).applymap(lambda x: [])
total_veh_delay_inst_FCFS = pd.DataFrame(index = range(0, iterations), columns = [1, 2, 3, 4, 5, 6, 7], dtype = object).applymap(lambda x: [])
#total_veh_delay_error_inst_FCFS = pd.DataFrame(index = range(0, iterations), columns = [1, 2, 3, 4, 5, 6, 7], dtype = object).applymap(lambda x: [])
queue_duration_inst_FCFS = pd.DataFrame(index = range(0, iterations), columns = [1, 2, 3, 4, 5, 6, 7], dtype = object).applymap(lambda x: [])
t_queue_remove_inst_FCFS = pd.DataFrame(index = range(0, iterations), columns = [1, 2, 3, 4, 5, 6, 7], dtype = object).applymap(lambda x: [])
#veh_in_queue_inst_FCFS = pd.DataFrame(index = range(0, iterations), columns = [1, 2, 3, 4, 5, 6, 7], dtype = object).applymap(lambda x: [])
#avg_veh_in_queue_inst_FCFS = pd.DataFrame(index = range(0, iterations), columns = [1, 2, 3, 4, 5, 6, 7], dtype = object).applymap(lambda x: [])
#max_veh_in_queue_inst_FCFS = pd.DataFrame(index = range(0, iterations), columns = [1, 2, 3, 4, 5, 6, 7], dtype = object).applymap(lambda x: [])
#avg_veh_delay_inst_FCFS = pd.DataFrame(index = range(0, iterations), columns = [1, 2, 3, 4, 5, 6, 7], dtype = object).applymap(lambda x: [])
avg_len_queue_inst_FCFS = pd.DataFrame(index = range(0, iterations), columns = [1, 2, 3, 4, 5, 6, 7], dtype = object).applymap(lambda x: [])

#phiX
net_dbl_park_minutes_df_inst_phi5 = pd.DataFrame(index = range(0, iterations), columns = [1, 2, 3, 4, 5, 6, 7], dtype = object).applymap(lambda x: [])
total_veh_delay_inst_phi5 = pd.DataFrame(index = range(0, iterations), columns = [1, 2, 3, 4, 5, 6, 7], dtype = object).applymap(lambda x: [])
#total_veh_delay_error_inst_phi5 = pd.DataFrame(index = range(0, iterations), columns = [1, 2, 3, 4, 5, 6, 7], dtype = object).applymap(lambda x: [])
queue_duration_inst_phi5 = pd.DataFrame(index = range(0, iterations), columns = [1, 2, 3, 4, 5, 6, 7], dtype = object).applymap(lambda x: [])
t_queue_remove_inst_phi5 = pd.DataFrame(index = range(0, iterations), columns = [1, 2, 3, 4, 5, 6, 7], dtype = object).applymap(lambda x: [])
#veh_in_queue_inst_phi5 = pd.DataFrame(index = range(0, iterations), columns = [1, 2, 3, 4, 5, 6, 7], dtype = object).applymap(lambda x: [])
#avg_veh_in_queue_inst_phi5 = pd.DataFrame(index = range(0, iterations), columns = [1, 2, 3, 4, 5, 6, 7], dtype = object).applymap(lambda x: [])
#max_veh_in_queue_inst_phi5 = pd.DataFrame(index = range(0, iterations), columns = [1, 2, 3, 4, 5, 6, 7], dtype = object).applymap(lambda x: [])
#avg_veh_delay_inst_phi5 = pd.DataFrame(index = range(0, iterations), columns = [1, 2, 3, 4, 5, 6, 7], dtype = object).applymap(lambda x: [])
avg_len_queue_inst_phi5 = pd.DataFrame(index = range(0, iterations), columns = [1, 2, 3, 4, 5, 6, 7], dtype = object).applymap(lambda x: [])

#Diff between FCFS and phiX metrics
net_dbl_park_minutes_Diff_df_inst_phi5 = pd.DataFrame(index = range(0, iterations), columns = [1, 2, 3, 4, 5, 6, 7], dtype = object).applymap(lambda x: [])
total_veh_delay_Diff_inst_phi5 = pd.DataFrame(index = range(0, iterations), columns = [1, 2, 3, 4, 5, 6, 7], dtype = object).applymap(lambda x: [])
#total_veh_delay_error_Diff_inst_phi5 = pd.DataFrame(index = range(0, iterations), columns = [1, 2, 3, 4, 5, 6, 7], dtype = object).applymap(lambda x: [])
queue_duration_Diff_inst_phi5 = pd.DataFrame(index = range(0, iterations), columns = [1, 2, 3, 4, 5, 6, 7], dtype = object).applymap(lambda x: [])
t_queue_remove_Diff_inst_phi5 = pd.DataFrame(index = range(0, iterations), columns = [1, 2, 3, 4, 5, 6, 7], dtype = object).applymap(lambda x: [])
#avg_veh_in_queue_Diff_inst_phi5 = pd.DataFrame(index = range(0, iterations), columns = [1, 2, 3, 4, 5, 6, 7], dtype = object).applymap(lambda x: [])
#max_veh_in_queue_Diff_inst_phi5 = pd.DataFrame(index = range(0, iterations), columns = [1, 2, 3, 4, 5, 6, 7], dtype = object).applymap(lambda x: [])
#avg_veh_delay_Diff_inst_phi5 = pd.DataFrame(index = range(0, iterations), columns = [1, 2, 3, 4, 5, 6, 7], dtype = object).applymap(lambda x: [])
avg_len_queue_Diff_inst_phi5 = pd.DataFrame(index = range(0, iterations), columns = [1, 2, 3, 4, 5, 6, 7], dtype = object).applymap(lambda x: [])


#AVG of Diff between FCFS and phiX metrics, not needed with the new random delivery vehicle scenarios
# AVG_net_dbl_park_minutes_Diff_df_inst_phi5 = pd.DataFrame(index = range(0, iterations), columns = [1, 2, 3, 4, 5, 6, 7], dtype = object).applymap(lambda x: [])
# AVG_total_veh_delay_Diff_inst_phi5 = pd.DataFrame(index = range(0, iterations), columns = [1, 2, 3, 4, 5, 6, 7], dtype = object).applymap(lambda x: [])
# AVG_total_veh_delay_error_Diff_inst_phi5 = pd.DataFrame(index = range(0, iterations), columns = [1, 2, 3, 4, 5, 6, 7], dtype = object).applymap(lambda x: [])
# AVG_queue_duration_Diff_inst_phi5 = pd.DataFrame(index = range(0, iterations), columns = [1, 2, 3, 4, 5, 6, 7], dtype = object).applymap(lambda x: [])
# AVG_t_queue_remove_Diff_inst_phi5 = pd.DataFrame(index = range(0, iterations), columns = [1, 2, 3, 4, 5, 6, 7], dtype = object).applymap(lambda x: [])
# AVG_veh_in_queue_Diff_inst_phi5 = pd.DataFrame(index = range(0, iterations), columns = [1, 2, 3, 4, 5, 6, 7], dtype = object).applymap(lambda x: [])
# AVG_max_veh_in_queue_Diff_inst_phi5 = pd.DataFrame(index = range(0, iterations), columns = [1, 2, 3, 4, 5, 6, 7], dtype = object).applymap(lambda x: [])
# AVG_avg_veh_delay_Diff_inst_phi5 = pd.DataFrame(index = range(0, iterations), columns = [1, 2, 3, 4, 5, 6, 7], dtype = object).applymap(lambda x: [])
# AVG_avg_len_queue_Diff_inst_phi5 = pd.DataFrame(index = range(0, iterations), columns = [1, 2, 3, 4, 5, 6, 7], dtype = object).applymap(lambda x: [])





#for c in range(1, max_parking_spaces +1):
for c in [1,2,4,7]: #added
   
            
    for i in range(0, iterations):
    #for i in range(32,33): #added

        print('c: ' + str(c) + ', i: ' + str(i))
        
        #FCFS metrics
        #n = 10
        #df = net_dbl_park_events_df_inst_FCFS[c][n][i] #added
        df = net_dbl_park_events_df_inst_FCFS.iloc[i, c-1][0] #i think this is what is needed, change n below to i
        
        if df.empty == True:
            net_dbl_park_minutes_df_inst_FCFS.iloc[i][c].append(0)
            total_veh_delay_inst_FCFS.iloc[i][c].append(0)
            #total_veh_delay_error_inst_FCFS.iloc[i][c].append(0)
            
            queue_duration_inst_FCFS.iloc[i][c].append(0)
            t_queue_remove_inst_FCFS.iloc[i][c].append(0)                

            #veh_in_queue_inst_FCFS.iloc[i][c].append(0)
            #max_veh_in_queue_inst_FCFS.iloc[i][c].append(0)

            #avg_veh_delay_inst_FCFS.iloc[i][c].append(0)

            avg_len_queue_inst_FCFS.iloc[i][c].append(0)
                            
        else:
            net_dbl_park_minutes_df_inst_FCFS.iloc[i][c].append(sum(df['Total']))
            
            #generate the piecewise function and output the function and the points dataframe
            [val, queue_duration, t_queue_remove, points, condlist, funclist] = piece(0, A_rate, D_rate, D_rate_dbl_park, df, Max_Q, len_scenario)
            #calc the start and stop y values based on the start and stop x values through the piecewise function
            #integrate.quad(lambda x: x*A_rate - piece(x, A_rate, D_rate, D_rate_dbl_park, df, Max_Q, len_scenario)[0], 0, len_scenario, limit = 1000, epsrel = .01) #, epsabs = 0.01, epsrel = 0.1, limit = 100
            
            #need to deal with the case where point might contain events exceeding len scenario.
            #Can be due to a vehicle being randomly shifted outside of the scenarion window.
            #Could also happen if a lane obstruction event ends prior to len scenario, but still needs
            #to burn off the queue.
            #First drop any rows in points which start after len scenario
            points.drop(points[points['Start_x'] >= len_scenario].index, inplace = True)
            #Second change any entries greater than len scenario to be equal to len scenario
            points.loc[points['Stop_x'] > len_scenario, 'Stop_x'] = len_scenario
            
            if points.empty == False:
                start_y_ls = []
                stop_y_ls = []
                for p in range(len(points)):
                    #establish the start x coordinate
                    x = points.iloc[p]['Start_x']
                    #run through the piecewise function to return the start y value
                    start_y_ls.append(piece(x, A_rate, D_rate, D_rate_dbl_park, df, Max_Q, len_scenario)[0])
                    
                    x = points.iloc[p]['Stop_x']
                    stop_y_ls.append(piece(x, A_rate, D_rate, D_rate_dbl_park, df, Max_Q, len_scenario)[0])
                    
                #append the list of the start and stop y values to the dataframe    
                points['Start_y'] = start_y_ls
                points['Stop_y'] = stop_y_ls
                #calc the area of each section under the curve of the departure curve, defined by the points dataframe
                points['Midpoint_Area'] = ((points['Start_y'] + points['Stop_y']) /2) * (points['Stop_x'] - points['Start_x']) 
                #calc the area under the arrival curve
                area_under_depart = np.sum(points['Midpoint_Area'])
                area_under_arrival = (len_scenario*(A_rate*len_scenario)) / 2 #base * height / x, area of a triangle
                #take the difference to get the space between the arrival and depart curve, aka the total vehicle delay
                total_veh_delay = area_under_arrival - area_under_depart
                #print(total_veh_delay)
            else:
                total_veh_delay = 0
            
            total_veh_delay_inst_FCFS.iloc[i][c].append(total_veh_delay)

            queue_duration_inst_FCFS.iloc[i][c].append(queue_duration[0])
            t_queue_remove_inst_FCFS.iloc[i][c].append(t_queue_remove[0])
            
            # veh_in_queue = []
            # for t in range(0, int(t_queue_remove[0])+1):
            #     veh_in_queue.append(t*A_rate - piece(t, A_rate, D_rate, D_rate_dbl_park, df, Max_Q, len_scenario)[0])
            
            # veh_in_queue_inst_FCFS.iloc[i][c].append(veh_in_queue)
            # avg_veh_in_queue_inst_FCFS.iloc[i][c].append(np.mean(veh_in_queue))
            # max_veh_in_queue_inst_FCFS.iloc[i][c].append(np.max(veh_in_queue))
            
            # avg_veh_delay = total_veh_delay / np.mean(veh_in_queue)
            # avg_veh_delay_inst_FCFS.iloc[i][c].append(avg_veh_delay)
            
            if queue_duration[0] == 0:
                avg_len_queue = 0
            else:
                avg_len_queue = total_veh_delay / queue_duration[0]
            avg_len_queue_inst_FCFS.iloc[i][c].append(avg_len_queue)         
        
        
        #phi of interest metrics
        #df = net_dbl_park_events_df_inst_phi5[c][n][i]
        df = net_dbl_park_events_df_inst_phi5.iloc[i, c-1][0]
        #df = pd.DataFrame({'Start':[5], 'End':[10], 'Total':[5]})
        
        #store the sum of the net minutes of double parking
        #store the total vehicle delay, determined through the integration of the 
        #arrivals and departure, and the error
        #store queue duration from the piece function
        #store time queue dissapated
        #store the number of vehicles in the queue
        #store the average vehicle delay
        #store the average queue length
        if df.empty == True:
            net_dbl_park_minutes_df_inst_phi5.iloc[i][c].append(0)
            total_veh_delay_inst_phi5.iloc[i][c].append(0)
            #total_veh_delay_error_inst_phi5.iloc[i][c].append(0)
            
            queue_duration_inst_phi5.iloc[i][c].append(0)
            t_queue_remove_inst_phi5.iloc[i][c].append(0)                

            #veh_in_queue_inst_phi5.iloc[i][c].append(0)
            #max_veh_in_queue_inst_phi5.iloc[i][c].append(0)

            #avg_veh_delay_inst_phi5.iloc[i][c].append(0)

            avg_len_queue_inst_phi5.iloc[i][c].append(0)
                            
        else:
            net_dbl_park_minutes_df_inst_phi5.iloc[i][c].append(sum(df['Total']))
            
            #generate the piecewise function and output the function and the points dataframe
            [val, queue_duration, t_queue_remove, points, condlist, funclist] = piece(0, A_rate, D_rate, D_rate_dbl_park, df, Max_Q, len_scenario)
            #calc the start and stop y values based on the start and stop x values through the piecewise function
            #integrate.quad(lambda x: x*A_rate - piece(x, A_rate, D_rate, D_rate_dbl_park, df, Max_Q, len_scenario)[0], 0, len_scenario, limit = 1000, epsrel = .01) #, epsabs = 0.01, epsrel = 0.1, limit = 100
            
            #need to deal with the case where point might contain events exceeding len scenario.
            #Can be due to a vehicle being randomly shifted outside of the scenarion window.
            #Could also happen if a lane obstruction event ends prior to len scenario, but still needs
            #to burn off the queue.
            #First drop any rows in points which start after len scenario
            points.drop(points[points['Start_x'] >= len_scenario].index, inplace = True)
            #Second change any entries greater than len scenario to be equal to len scenario
            points.loc[points['Stop_x'] > len_scenario, 'Stop_x'] = len_scenario
            
            if points.empty == False:
                start_y_ls = []
                stop_y_ls = []
                for p in range(len(points)):
                    #establish the start x coordinate
                    x = points.iloc[p]['Start_x']
                    #run through the piecewise function to return the start y value
                    start_y_ls.append(piece(x, A_rate, D_rate, D_rate_dbl_park, df, Max_Q, len_scenario)[0])
                    
                    x = points.iloc[p]['Stop_x']
                    stop_y_ls.append(piece(x, A_rate, D_rate, D_rate_dbl_park, df, Max_Q, len_scenario)[0])
                    
                #append the list of the start and stop y values to the dataframe    
                points['Start_y'] = start_y_ls
                points['Stop_y'] = stop_y_ls
                #calc the area of each section under the curve of the departure curve, defined by the points dataframe
                points['Midpoint_Area'] = ((points['Start_y'] + points['Stop_y']) /2) * (points['Stop_x'] - points['Start_x']) 
                #calc the area under the arrival curve
                area_under_depart = np.sum(points['Midpoint_Area'])
                area_under_arrival = (len_scenario*(A_rate*len_scenario)) / 2 #base * height / x, area of a triangle
                #take the difference to get the space between the arrival and depart curve, aka the total vehicle delay
                total_veh_delay = area_under_arrival - area_under_depart
                #print(total_veh_delay)
            else:
                total_veh_delay = 0
            
            
            total_veh_delay_inst_phi5.iloc[i][c].append(total_veh_delay)

            queue_duration_inst_phi5.iloc[i][c].append(queue_duration[0])
            t_queue_remove_inst_phi5.iloc[i][c].append(t_queue_remove[0])
            
            # veh_in_queue = []
            # for t in range(0, int(t_queue_remove[0])+1):
            #     veh_in_queue.append(t*A_rate - piece(t, A_rate, D_rate, D_rate_dbl_park, df, Max_Q, len_scenario)[0])
                
            # veh_in_queue_inst_phi5.iloc[i][c].append(veh_in_queue)
            # avg_veh_in_queue_inst_phi5.iloc[i][c].append(np.mean(veh_in_queue))
            # max_veh_in_queue_inst_phi5.iloc[i][c].append(np.max(veh_in_queue))
            
            # avg_veh_delay = total_veh_delay / np.mean(veh_in_queue)
            # avg_veh_delay_inst_phi5.iloc[i][c].append(avg_veh_delay)
            
            if queue_duration[0] == 0:
                avg_len_queue = 0
            else:
                avg_len_queue = total_veh_delay / queue_duration[0]
            avg_len_queue_inst_phi5.iloc[i][c].append(avg_len_queue)
            
            
        #add the diff metrics
        
        net_dbl_park_minutes_Diff_df_inst_phi5.iloc[i][c].append(net_dbl_park_minutes_df_inst_FCFS.iloc[i][c][0] - net_dbl_park_minutes_df_inst_phi5.iloc[i][c][0])
        total_veh_delay_Diff_inst_phi5.iloc[i][c].append(total_veh_delay_inst_FCFS.iloc[i][c][0] - total_veh_delay_inst_phi5.iloc[i][c][0])
        #total_veh_delay_error_Diff_inst_phi5.iloc[i][c].append(total_veh_delay_error_inst_FCFS.iloc[i][c][0] - total_veh_delay_error_inst_phi5.iloc[i][c][0])
        queue_duration_Diff_inst_phi5.iloc[i][c].append(queue_duration_inst_FCFS.iloc[i][c][0] - queue_duration_inst_phi5.iloc[i][c][0])
        t_queue_remove_Diff_inst_phi5.iloc[i][c].append(t_queue_remove_inst_FCFS.iloc[i][c][0] - t_queue_remove_inst_phi5.iloc[i][c][0])
        #avg_veh_in_queue_Diff_inst_phi5.iloc[i][c].append(np.mean(veh_in_queue_inst_FCFS.iloc[i][c][0]) - np.mean(veh_in_queue_inst_phi5.iloc[i][c][0]))
        #max_veh_in_queue_Diff_inst_phi5.iloc[i][c].append(max_veh_in_queue_inst_FCFS.iloc[i][c][0] - max_veh_in_queue_inst_phi5.iloc[i][c][0])
        #avg_veh_delay_Diff_inst_phi5.iloc[i][c].append(avg_veh_delay_inst_FCFS.iloc[i][c][0] - avg_veh_delay_inst_phi5.iloc[i][c][0])
        avg_len_queue_Diff_inst_phi5.iloc[i][c].append(avg_len_queue_inst_FCFS.iloc[i][c][0] - avg_len_queue_inst_phi5.iloc[i][c][0])



                
#the average metrics are not necessary any more becuase we are not doing 20 iterations on single number of delivery vehicles
# AVG_net_dbl_park_minutes_Diff_df_inst_phi5 = net_dbl_park_minutes_Diff_df_inst_phi5.applymap(lambda x: np.mean(x))            

# AVG_total_veh_delay_Diff_inst_phi5 = total_veh_delay_Diff_inst_phi5.applymap(lambda x: np.mean(x))     

# AVG_total_veh_delay_error_Diff_inst_phi5 = total_veh_delay_error_Diff_inst_phi5.applymap(lambda x: np.mean(x))     

# AVG_queue_duration_Diff_inst_phi5 = queue_duration_Diff_inst_phi5.applymap(lambda x: np.mean(x))     

# AVG_t_queue_remove_Diff_inst_phi5 = t_queue_remove_Diff_inst_phi5.applymap(lambda x: np.mean(x)) 

# AVG_avg_veh_in_queue_Diff_inst_phi5 = avg_veh_in_queue_Diff_inst_phi5.applymap(lambda x: np.mean(x))   

# AVG_max_veh_in_queue_Diff_inst_phi5 = max_veh_in_queue_Diff_inst_phi5.applymap(lambda x: np.mean(x))

# AVG_avg_veh_delay_Diff_inst_phi5 = avg_veh_delay_Diff_inst_phi5.applymap(lambda x: np.mean(x))  

# AVG_avg_len_queue_Diff_inst_phi5 = avg_len_queue_Diff_inst_phi5.applymap(lambda x: np.mean(x))   



# #save data needed for the graphic generation
# import pickle
# with open('pub_Pitt_queuing_data_post_process_phi5_limit30_midpt_24_Mar_2023_buffer_5_pessimistic.pkl', 'wb') as file:
#     pickle.dump([net_dbl_park_minutes_df_inst_FCFS,
#                   total_veh_delay_inst_FCFS,
#                   queue_duration_inst_FCFS,
#                   t_queue_remove_inst_FCFS,
#                   avg_len_queue_inst_FCFS,
#                   net_dbl_park_minutes_df_inst_phi5,
#                   total_veh_delay_inst_phi5,
#                   queue_duration_inst_phi5,
#                   t_queue_remove_inst_phi5,
#                   avg_len_queue_inst_phi5,
#                   net_dbl_park_minutes_Diff_df_inst_phi5,
#                   total_veh_delay_Diff_inst_phi5,
#                   queue_duration_Diff_inst_phi5,
#                   t_queue_remove_Diff_inst_phi5,
#                   avg_len_queue_Diff_inst_phi5],
#                   file)

# # file.close()


toc = time.time()

runtime = toc-tic
print('runtime: ' + str(runtime))






