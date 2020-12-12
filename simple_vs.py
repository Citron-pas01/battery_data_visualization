import numpy as np
import pandas as pd
import csv
import time
import matplotlib.pyplot as plt

'''
This simple_vs.py is to visulize the material properties directly from the dataset

Frequency vs. attributes (('Capacity','mAh/g'), ('Voltage','V'), ('Conductivity', 's/cm'), 
                ('Coulombic Efficiency', '%'), ('Energy', 'Wh/kg'))

That is the Figure 1 in the report.


Bo Nie
12/12/2020
'''

start_time = time.time()
battery_df =  pd.read_csv('C:\\Users\\Bo_Ni\\OneDrive - The Pennsylvania State University\\PSU\\1-Class\\IE 582\\Project\\battery.csv')

# clean the "Date" format
battery_df['Date'] = battery_df['Date'].str.replace('/','-')


feature = [('Capacity','mAh/g'), ('Voltage','V'), ('Conductivity', 's/cm'), 
                ('Coulombic Efficiency', '%'), ('Energy', 'Wh/kg')]
for category in feature:

    # start with the each attribute
    battery_capacity= battery_df[battery_df['Property']== category[0]]
    
    plt.rcParams.update({'figure.figsize':(7,5), 'figure.dpi':100})

    # Plot Histogram on x
    x = battery_capacity['Value'].values.tolist()

    if category[0] == 'Conductivity':

        #print('max:{} and min: {}'.format(np.max(result),np.min(result)))
        result = list(filter(lambda a: a > 10**(-12), x) )

        plt.hist(-np.log10(result), bins=100)
        plt.gca().set(title= category[0] + ' Frequency Histogram', ylabel='Frequency', xlabel = '-log10'+  ' (' + category[0] + ' (' + category[1] +')'+')');
        plt.xlim(0, 15)
        
    else:
        plt.hist(x, bins=100)
        plt.gca().set(title= category[0] + ' Frequency Histogram', ylabel='Frequency', xlabel = + category[0] + ' (' + category[1] +')');
        plt.xlim(0, 3000)
        plt.show()
        #plt.savefig(category[0] + '.png')
