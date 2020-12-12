import numpy as np
import pandas as pd
import csv
import time
import arrow
import itertools 
from difflib import SequenceMatcher

'''
This ds.py is to clean the database and regulated the materials to cathodes and anodes

Defining materials which have connection with other and calculate the weights:
    weights = 1/3(similarity_name + closeness of property value + closeness of date)

The database is huge, this project ramdonly select 5000 rows (5000 materials from 5000 literature) 
to process.

Finally write the regulated and calculated file and save.

Bo Nie
12/12/2020
'''

start_time = time.time()
battery_df =  pd.read_csv('C:\\Users\\Bo_Ni\\OneDrive - The Pennsylvania State University\\PSU\\1-Class\\IE 582\\Project\\battery.csv')

# calculate the similarity between two material names
def similar_1(a, b):
    return SequenceMatcher(None, a, b).ratio()

# calculate the closeness for two research paper publish date
def similar_2(d1,d2,date_range):
    d_range = arrow.get(date_range[0]) - arrow.get(date_range[1])
    delta = arrow.get(d1) - arrow.get(d2)
    date_ratio = delta.days/d_range.days
    return abs(date_ratio)

# calculate the closeness of the property value between two material research
def similar_3(c1, c2, property_range):
    property_ratio = abs(c1-c2)/property_range
    return property_ratio

def df_process(vs_set,category,electrode):

    # set the capacity unit
    vs_set['Unit'] = category[1] 

    #year_min, year_max = vs_set['Year'].min(), vs_set['Year'].max()

    # calculate the date range: the date form yy-mm-dd for numerical calculation is difficult
    d = vs_set['Date'].max()
    date_range = [str(vs_set['Date'].max()),str(vs_set['Date'].min())]
    property_range = vs_set['Value'].max() - vs_set['Value'].min()

    assoc_dictionary = dict()

    cluster_item = []
    relationships = []
    
    # calculate the similarities between two materials and determine whether an edge happens
    for item_i, item_j in itertools.combinations(vs_set['ID'],2):
        name_i = vs_set.loc[vs_set['ID'] == item_i, 'Name'].values[0] 
        name_j = vs_set.loc[vs_set['ID'] == item_j, 'Name'].values[0] 
    
        si = similar_1(name_i, name_j)

        # there are two important parameters (0.6 & 0.7) to determin the edge and clustering
        if si>0.6:
            k = (item_i, item_j)
            relationships.append(k)
                            
            # put this materials with a higher similarity (module density) in a list
            if si>0.7: 
                cluster_item.extend([item_i,item_j])

    # calculate the edge weight from the standardized value of 
    # the material name similarity, publishing date closeness, and property value closeness   
    for relationship in relationships:

        # material name similarity
        name_1 = vs_set.loc[vs_set['ID'] == relationship[0], 'Name'].values[0] 
        name_2 = vs_set.loc[vs_set['ID'] == relationship[1], 'Name'].values[0] 
        si_1 = similar_1(name_1, name_2)

        # publishing date closeness
        date_1 = vs_set[vs_set['ID'] == relationship[0]].index.values[0]  
        date_2 = vs_set[vs_set['ID'] == relationship[1]].index.values[0] 
        si_2 = similar_2(date_1, date_2, date_range)

        # property value closeness 
        Value_1 = vs_set.loc[vs_set['ID'] == relationship[0], 'Value'].values[0]  
        value_2 = vs_set.loc[vs_set['ID'] == relationship[1], 'Value'].values[0] 
        si_3 = similar_3(Value_1, value_2, property_range)

        assoc_dictionary[relationship] = (si_2 + si_2 + si_3)/3

    if electrode != 0:
        # combine each row of a dataframe together, using pd.concat is more efficient
        if len(cluster_item) != 0:
            cluster_set = pd.concat([vs_set.loc[vs_set['ID'] == k] for k in set(cluster_item)], ignore_index=True)

            with open(electrode + '_' + category[0] +'_cluster_element.csv', 'w', encoding='cp1252', errors='ignore') as f:
                cluster_set.to_csv(f)  
            
        # write and save a dictionary file to PC
        np.save(electrode + '_' + category[0] +'_assoc_dictionary.npy', assoc_dictionary) 
    
        with open(electrode + '_' + category[0] +'_vs.csv', 'w', encoding='cp1252', errors='ignore') as f:
            vs_set.to_csv(f)
    else:
         if len(cluster_item) != 0:
            print('I am here')
            cluster_set = pd.concat([vs_set.loc[vs_set['ID'] == k] for k in set(cluster_item)], ignore_index=True)
            with open(category[0] +'_cluster_element.csv', 'w', encoding='cp1252', errors='ignore') as f:
                cluster_set.to_csv(f)  
            
        # write and save a dictionary file to PC
         np.save(category[0] +'_assoc_dictionary.npy', assoc_dictionary) 
    
         with open(category[0] +'_vs.csv', 'w', encoding='cp1252', errors='ignore') as f:
            vs_set.to_csv(f)
        

# clean the "Date" format
battery_df['Date'] = battery_df['Date'].str.replace('/','-')

# generate the material ID
battery_df['ID'] = battery_df.index

# generate a dataframe with voltage value
voltage_df = battery_df[battery_df['Property']=='Voltage']

# generate the dictionary with material name and voltage value
Voltage_dict = dict(zip(voltage_df['Name'], voltage_df['Value']))

# if the voltage less than 2 V, the material is an anode material
anode_name = [name for name, voltage in Voltage_dict.items() if voltage < 2]
cathode_name = [name for name, voltage in Voltage_dict.items() if voltage >= 2]

anode_df = pd.DataFrame(anode_name,columns=['Anode_name'])
cathode_df = pd.DataFrame(cathode_name,columns=['Cathode_name'])

# the names possibly cathode which should be removed from the anode list
delete_str = ['Mn','LFP','Ru','Nb','Mo','S','Se','La','Cr','Li3P','LPO','PO4','LMO','Sr','Na0.8Fe0.8Ti1.2O4','cathode']
anode_df = anode_df[~anode_df['Anode_name'].str.contains('|'.join(delete_str))]

# the names possibly anode which should be removed from the cathode list
searchfor_1 = ['anodes', 'CoFe2O4','Li3Ti4CoCrO12','Cu', 'Fe3O4', 'si', 'Si', 'Li4Ti5O12', 'SnO', 'SiO','TiO2','LTO',
               'CuFe2O4','Na4C24H8O8','Co3O4','CNT @ MnO','Sb','anode', 'NiO', 'Sn']
cathode_df = cathode_df[~cathode_df['Cathode_name'].str.contains('|'.join(searchfor_1))]

# filter the conductivity value more than 10^-12
Conductivity_df = battery_df[battery_df['Property']=='Conductivity']

# generate the dictionary with material ID and conductivity value
Conductivity_dict = dict(zip(Conductivity_df['ID'], Conductivity_df['Value']))

conductivity_ID = [ID for ID, conductivity in Conductivity_dict.items() if conductivity > 10**(-12)]

# these are the attribute name for the material properties which are used to regulate materials and properties
feature = [('Capacity','mAh/g'), ('Voltage','V'), ('Conductivity', 's/cm'), 
           ('Coulombic Efficiency', '%'), ('Energy', 'Wh/kg')]

cycle = 0
for category in feature:

    # start with the each property attribute
    battery_capacity= battery_df[battery_df['Property']== category[0]]

    cols = ['Name','Property','Value','Unit', 'Date','ID']

    # select the material name containing "O", probably the oxides
    m1 = battery_capacity['Name'].str.contains('O')

    d_set = battery_capacity.loc[m1,cols]

    # clean the rows and columns with 'Nan or None'
    searchfor_2 = ['None']
    d_set = d_set[~d_set['Date'].str.contains('|'.join(searchfor_2))]

    # get the year date out the yy-mm-dd format
    d_set['Year'] = d_set['Date'].str[0:4]
    
    # ramdonly generate 5000 rows from the database, if the attribute have > 5000 rows
    n = 5000
    if d_set.shape[0] > n:
        data_set = d_set.sample(n, random_state = 2)
    else:
        data_set = d_set
    
    # separate process the 'conductivity' attribute
    if category[0] == 'Conductivity':

        # find the dataset belonging to conductivity
        data_set = data_set[data_set['ID'].isin(conductivity_ID)]

        # calculate the edge and weight and save files
        df_process(data_set,category,0)
    
    else:

        for electrode in ['Cathode','Anode']:
            
            # loop running notifications
            cycle +=1
            print('It runs at cycle of:{}'.format(cycle))
            vs_set = data_set
            
            # drop the rows which is possibly the anode material as following (is / containing)
            if electrode == 'Cathode':
                vs_set = vs_set[~vs_set['Name'].str.contains('|'.join(searchfor_1))]

                # find the common name between the set and anode name df
                common_name = list(set(vs_set['Name']) & set(anode_df['Anode_name']))

                # drop those name exactly the name from the anode name set
                vs_set = vs_set[~vs_set['Name'].isin(common_name)]

            else:
                vs_set = vs_set[~vs_set['Name'].str.contains('|'.join(delete_str))]
                
                # find the common name between the set and cathode name df
                common_name = list(set(vs_set['Name']) & set(cathode_df['Cathode_name']))

                # drop those name exactly the name from the cathode name set
                vs_set = vs_set[~vs_set['Name'].isin(common_name)]
            
            # calculate the edge and weight and save files for both cathodes and anodes
            df_process(vs_set,category,electrode)

elapsed_time = (time.time() - start_time)
print('-------------------','%.2f' % round(elapsed_time, 2),'Seconds -----------------------')




