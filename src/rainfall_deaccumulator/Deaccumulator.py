#required packages
import pandas as pd 
import numpy as np
import os


def generate_rain_value(timevalue, final_val, running_time):
    time_array = []
    val_array = []
    
    start = timevalue - running_time
    end = timevalue 
    for i in range(start,end):
        time_array.append(i)
        
    val_array = np.random.uniform(high=final_val, size=len(time_array))
    val_array = sorted(val_array)    
    
    time_array.append(timevalue)
    val_array.append(final_val)
    dfseconds = pd.DataFrame({'unixdatetime':time_array, 'value':val_array})
    return dfseconds.round(3)

def get_inputs():
    files = []
    files = os.listdir('Inputs')
    return (files)


def find_peak(data,peak_duration_minutes, total_running_time_minutes):
    peak_sum = 0
    current_sum = 0
    peak_time_higherbound = 0
    peak_time_lowerbound = 0
    index_span = int((len(data)/total_running_time_minutes)*peak_duration_minutes)
    #print(index_span)
    count = 0
    for i in range(0, len(data)-index_span):
        if count == 0:
            peak_sum = data[data.columns[1]][i: i+index_span].sum()
            peak_time_higherbound = data[data.columns[0]][i]
            peak_time_lowerbound = data[data.columns[0]][i+index_span]
        else:
            current_sum = data[data.columns[1]][i: i+index_span].sum()
            if (current_sum > peak_sum):
                peak_sum = current_sum
                peak_time_lowerbound = data[data.columns[0]][i]
                peak_time_higherbound = data[data.columns[0]][i+index_span]
        count+=1
    L_peak_time  = pd.to_datetime(peak_time_lowerbound , unit = 's')
    H_peak_time  = pd.to_datetime(peak_time_higherbound , unit = 's')
    message = 'Peak '+ str(peak_duration_minutes)+ ' minutes duration between: ' + str(L_peak_time) + ' and ' + str(H_peak_time)
    print(message)
    return([peak_sum,peak_time_lowerbound, peak_time_higherbound ])
  

def deaccumulate(file, total_duration_minutes, peak_duration_minutes):
    df = pd.read_table(file,sep = '\s+', encoding = 'utf-16', engine = 'python')
    peak = 0
    observation_time = int((total_duration_minutes*60)/len(df))
    count = 0
    
    first_date = df[df.columns[0]][0]
    last_date = df[df.columns[0]][len(df)-1]
    
    first_date = str(pd.to_datetime(first_date, unit = 's'))
    last_date = str(pd.to_datetime(last_date, unit = 's'))
    
    deacc_full_filename = first_date+'-'+last_date+'full_table.csv'
    deacc_full_filename = deacc_full_filename.replace(" ", '-')
    deacc_full_filename = deacc_full_filename.replace("00:00:00", '')
    
    
    for i in range(0,len(df)):
        final_time = df[df.columns[0]][i]
        final_val = df[df.columns[1]][i]
        time_String = str(pd.to_datetime(final_time, unit ='s'))

        filename = time_String+'deaccumulated.csv'
        filename = filename.replace(" ", '-')
        filename = filename.replace("00:00:00", '')
        
        df_deacc = generate_rain_value(final_time,final_val,observation_time)
        #print(filename)
        df_deacc.to_csv('Outputs/' + filename, sep=',')
        if(count == 0):
            df_deacc_full = df_deacc
        else:
            df_deacc_full = pd.concat([df_deacc_full,df_deacc], ignore_index = True)
            
        count+=1
            
    df_deacc_full.to_csv('Outputs/' + deacc_full_filename, sep = ',')
    find_peak(df,peak_duration_minutes,total_duration_minutes)
            
        

in_files = get_inputs()
print(in_files)

for file in in_files:
    deaccumulate('Inputs/'+file, 60, 30)

