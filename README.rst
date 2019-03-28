======================
======================
Rainfall_DeAccumulator
======================
======================

Representative Response from Camillus Sanga for data scientist position for Mott Macdonald. 

=====
Brief
=====

Rainfall data is taken from a client that contains precipitaion in (inches) at irregular times. The data is taken at irregular intervals but always taken at a time of 12am. Furthermore all the entries has been recorded at a total time of 60 minutes. The aim of this project is to calculate the precipitaion values between the observed times. 

========
Solution
========

To calculate the values for the unobserved times. The data is split into years and the entries on each year is split into 4 seasons summer, winter, autumn and fall. The mean and standard deviation for each season is the calculated and used as parameters to generate reasonable rainfall values for the unobserved intervals. 

===========
Assumptions
===========

1. Since the whole data set is 1hr running total and there are only 90 entries in the data, I assumed that the measuring device is running for 40 seconds for every observation. Therefore, each observation is NOT an aggregate value of the rainfall that day but a 40 minute reading at 12am in that day.  

2. Rain intensity is heavily dependent on the current season and rainfall values is normally distributed in each season. 

3. Hourly rainfall distribution follows the same distribution as the seasonal rainfall and the same statistical parameters can be used to to generate values in an hourly basis. Furthermore without using other variables such as hourly temperature readings or cloud formation in a specific area, unobserved rainfall data can be randomly generated. 

4. The peak 30 minutes is the 30 minute span in the given data set that has the highest combined value. 


==================
Building the code
==================

The code is built using virtualenv and pyscaffold.
Dependencies include:

numpy 
pandas




================
Running the Code
================

1. Create a virtual environment
2. run "pip install numpy" and "pip install pandas" in the virtual environment
3. copy input data to the inputs folder in \ Rainfall_DeAccumulator\src\rainfall_deaccumulator\Inputs such as accumRainfall.csv
4. navigate to Rainfall_DeAccumulator \ src \ rainfall_deaccumulator with the console and run the DeaccumulatorV2.py scipt
5. When the script finishes the peak 30min period should be printed on the console
6. Navigate to the Outputs folder in  Rainfall_DeAccumulator\src\rainfall_deaccumulator\Corrected_output and the deAccumulated data files should be listed



============
Other Notes
============
1. The unit of the values is measured in Inches
2. For New datasets simply copy the new data files to the input folder and run the script again (assumming that it is in the same format as accumRainfall.csv)
3. Deaccumulator.py is an obsolete script and this outputs the incorrect values for each observation. Instead this scripts outputs the rainfall data while it is being observed. 
4. In order to accurately predict the unobserved data, more data is required such as the exact location of the observation site, the cloud formation and location data for that site and the temperature of the site. 


