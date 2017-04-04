# Table of Contents
1. [Introduction](README.md#introduction)
2. [Description of Execution](README.md#description-of-execution)
2. [Details of Implementation](README.md#details-of-implementation)

# Introduction

This challenge is completed by python 3. The packages that will be used are:
sys, io, collections, datetime, heapq and queue (Queue in python 2).

For the required 4 features, they are implemented by the **process_log.py**. There are two more extra features that I think important. The first feature (**e1.py**, output ../log_out/hours_new.txt and ../log_out/visit_analysis.txt) and the second feature (**e2.py**, output ../log_out/top_failure.txt). Details will be explained later.

# Description of Execution
To perform the calculation, run **run.sh** and **run_extra.sh** separately. The first one will extract the 4 essential features and the second one will extract some other features that are also interesting.

# Details of Implementation

For the 4 essential features, the implementation is well documentted in the process_log.py file. 

For feature 1 and 2, I use a dictionary to store the number of visit for each IP and the bandwidth for each resources respectively. For feature 1 and 2, I store the negative value in the counting which will be helpful for doing comparison later.

For feature 3, I use three list to store the identical timestamp, number of visit per second and number of visit per hour. Since timestamp is non-descending in the input file, there is no need to use dictionary with would take extra time to calculate the hashing function. 

For feature 1, 2 and 3, I use the data strcture called "heap" to find out the top 10 from the tuples of interested features. Heap can lower the time complexity to O(n) to find the most distinguishing items.

For feature 4, I use a dictionary to store all the related warnings, identified by the IP address. For each item in the dictionary, I use a queue to store up to 3 warnings. Queue is useful in this problem because we need to get rid of earlier recorded warning under certain conditions (the time interval between two warnings greater than 20s). The total time complexity is O(n).

The only thing to point out for feature 3 is that the extract most busiest hour, according to the definition in the description, will have overlap for most of the case. Time precision is only considered up to seconds and only count when there is an event happening. It is neither accurate nor meaningful to consider the businest time with lots of overlap. So I implement the extra feature that extract the busiest hour without overlap. I also count for the access time period based on weekdays as well as hours. This data will help estimate the frequency of different weekdays or hours. Such features are implemented in e1.py.

For e2.py, I count the most (top 10) frequent failed connection IP. This feature can help us prevent the connection from these sites or lower the priority of such connection in the website design.
