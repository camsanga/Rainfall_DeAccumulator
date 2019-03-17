======================
Rainfall_DeAccumulator
======================

Representative Response from Camillus Sanga for data scientist position for Mott Macdonald

================
Running the Code
================

1. Start virtual Environment
2. run "pip install numpy" and "pip install pandas" in the virtual environment
3. copy input data to the inputs folder in \Rainfall_DeAccumulator\src\rainfall_deaccumulator\Inputs such as accumRainfall.csv
4. navigate to Rainfall_DeAccumulator\src\rainfall_deaccumulator with the console and run the Deaccumulator.py scipt
5. When the script finishes the peak 30min period should be printed on the console
6. Navigate to the Outputs folder in  Rainfall_DeAccumulator\src\rainfall_deaccumulator\Outputs and the deAccumulated data files should be listed

===========
Assumptions
===========
1. Since the whole data set is 1hr running total, I assumed that the measuring device is running for 40 seconds for every observation
2. Each observartion is the total amount of rainwater collected within the 40 second window and is measured in Inches
3. When rainfall is being measured, the rate at which the water fills the measuring device is not constant every second since rain intensity can vary


============
Other Notes
============
1. The unit of the values is measured in Inches
2. For New datasets simply copy the new data files to the input folder and run the script again (assumming that it is in the same format as accumRainfall.csv)


