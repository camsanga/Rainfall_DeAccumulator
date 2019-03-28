#required packages
import pandas as pd 
import numpy as np
import os


def get_inputs():
    #returns input files
    files = []
    files = os.listdir('Inputs')
    return (files)





def find_peak(data,peak_duration_minutes, total_running_time_minutes):
    #function calculates the sum value of every consecutive entries with a step of 1 and compares them
    
    peak_sum = 0
    current_sum = 0
    peak_time_higherbound = 0
    peak_time_lowerbound = 0
    index_span = int((len(data)/total_running_time_minutes)*peak_duration_minutes)
    #calculates the maximum number of steps that can be taken for comparison from given time interval
    
    count = 0
    for i in range(0, len(data)-index_span):
        #iterates through each step and compares the sum values
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




def calc_mean_year(data):
    #This function calculates the mean value and standard deviation for each seasons to generate values
    
    #US seasons 
    #spring march - may
    #summer june - august
    #fall september - novemvber
    #winter december - february
    # taken from:http://www.temple.edu/international/gp/future-students/philadelphia-weather.html
    
    #creates an array of numbers based on months that correspond for each season 
    winter = [12,1,2]
    spring = [3, 4, 5]
    summer = [6,7,8]
    fall = [9,10,11]
    
    #calculates datetime stamp from unix datetime
    data['datetime'] = pd.to_datetime(data['unixdatetime'], origin = 'unix', unit = 's')
    month = data.datetime.dt.month
    
    #Values are stored in each array
    winter_values = []
    spring_values = []
    summer_values = []
    fall_values = []
    
    means = []
    stds = []
    
    # classifies each values based on it's month and puts them into their corresponding seasons
    for i in range(0,len(data)):
        if(data.loc[i].datetime.month in winter):
            winter_values.append(data.loc[i].value)
        elif(data.loc[i].datetime.month in spring):
            spring_values.append(data.loc[i].value)
        elif(data.loc[i].datetime.month in summer):
            summer_values.append(data.loc[i].value)
        elif(data.loc[i].datetime.month in fall):
            fall_values.append(data.loc[i].value)
            
    #calculates the means and standard deviations of each seasons
    means.append(np.mean(winter_values))
    stds.append(np.std(winter_values))
    means.append(np.mean(spring_values))
    stds.append(np.std(spring_values))
    means.append(np.mean(summer_values))
    stds.append(np.std(summer_values))
    means.append(np.mean(fall_values))
    stds.append(np.std(fall_values))
    return([means, stds])
    

def value_generator(start, end,mean,sd):
    #This function generate values using a normal distribution based on the mean and standard deviation of the existing data
    
    #calculates the unixdatetime between each observation with a window of 30 minutes
    unixdatetime = []
    for time in range(start, end,1800):
        unixdatetime.append(time)
    values = []
    
    #values are generated using a normal curve based on the parameters of the exisiting observations
    values = np.random.normal(mean, sd, len(unixdatetime))
    d = {'Unixdatetime': unixdatetime, 'values': values}
    df = pd.DataFrame(data=d)
   
    return(df.abs())


def get_years(data):
    #This function returns an array of the years that the dataset covers
    data['datetime'] = pd.to_datetime(data['unixdatetime'], origin = 'unix', unit = 's')
    ddt = data.datetime.dt.year
    unique = 0
    years = []
    #iterates through each row and adds the different years in the array
    for i in ddt:
        if ((i != unique) and (i not in years)):
            years.append(i)
            unique = i
    #returns an array of years
    return(years)


def month_class(unixdt):
    #this function classifies and returns the corresponding season for a given unixdatetime
    datetime = pd.to_datetime(unixdt, origin = 'unix', unit = 's')
    month = datetime.month
    if(month in [12,1,2]):
        return(0)
    elif(month in [3,4,5]):
        return(1)
    elif(month in [6,7,8]):
        return(2)
    elif(month in [9,10,11]):
        return(3)

    
def deaccumulate(file):
    #Imports file as a dataframe
    df = pd.read_table(file,sep = '\s+', encoding = 'utf-16', engine = 'python')
    
    #calculates the mean and std for each seasons
    seasonal_parameters = calc_mean_year(df)
    
    #calculates the years of the given data
    years = get_years(df)
    
    #calculates the datetime of the dataframe
    df['datetime'] = pd.to_datetime(df['unixdatetime'], origin = 'unix', unit = 's')
    yr = df.datetime.dt.year
    count = 0
    
    #retrieves the start and end dates as a string to create a folder
    start_date = str(df.datetime.min()).replace(" 00:00:00", '')
    end_date = str(df.datetime.max()).replace(" 00:00:00", '')
    folder_name = start_date+'-'+ end_date
    
    #calculates the peak 30 minutes
    peak = find_peak(df,30,60)
    
    #creates a folder to store the deaccumulated data
    output_dir = 'Corrected_output/'+folder_name+'/'
    os.mkdir(output_dir)
    
    
    #iterates through each year
    for year in years:
        
        #iterates through each observations in the given year 
        current_year_df = df[yr == year]
        previous = 0
        nextt = 0
        for i in range(0, len(current_year_df)-1):
            previous = current_year_df['unixdatetime'][i]
            nextt = current_year_df['unixdatetime'][i+1]
            
            #classifies the given time to seasons
            season =  month_class(nextt)
            
            #retrieves the mean and standard deviation for that season
            mean = seasonal_parameters[0][season]
            std = seasonal_parameters[1][season]
            
            #generates the un-observed values 
            generated = value_generator(previous, nextt,mean,std)
            generated = generated.round(2)
            
            #writes the values to a specific csv file
            
            timestring1 = str(pd.to_datetime(previous, origin = 'unix', unit = 's'))
            timestring2 = str(pd.to_datetime(nextt, origin = 'unix', unit = 's'))
            timestring = timestring1 +'-'+timestring2+'_'
            filename = timestring+'deaccumulated.csv'
            filename = filename.replace(" ", '-')
            filename = filename.replace("00:00:00", '')
            generated.to_csv(output_dir+filename, sep = ',')
            count+=1
            
            
        
    

in_files = get_inputs()
print(in_files)

for file in in_files:
    deaccumulate('Inputs/'+file)

