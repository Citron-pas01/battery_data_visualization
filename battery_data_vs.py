import csv
import numpy as np
import pandas as pd
from battery_plot import attribute_time_plot, network_graph, network_graph2

'''
This IE582.py is to load the calculated files which is saved from ds.py
Then import the plot functions from batter_plot.py to plot the network graphes,
material distribution, statistic summarization

Bo Nie
12/12/2020
'''


for x in  ['Cathode','Anode']:

    assoc_data = []        
    rat_data = []
    clustering_data = []

    # these are the attribute name for the material properties which are used to name the calculated files
    name_list = ['Capacity', 'Voltage', 'Conductivity', 'Coulombic Efficiency','Energy']

    for file_name in name_list:
    
        # as the conductivity materials can't be divide as cathode or anode
        if file_name == 'Conductivity':

            # load the edge and edge weight dictionary file
            read_dictionary = np.load( file_name +'_assoc_dictionary.npy',allow_pickle='TRUE').item()
            assoc_data.append(read_dictionary)

            # load all the materials as the nodes in network
            load_1 =  pd.read_csv(file_name +'_vs.csv',encoding='cp1252')
            rat_data.append(load_1)

            # load community materials data file 
            load_2 =  pd.read_csv(file_name +'_cluster_element.csv',encoding='cp1252')
            clustering_data.append(load_2)
    
        else:

            # load the edge and edge weight dictionary file
            read_dictionary = np.load(x + '_' + file_name +'_assoc_dictionary.npy',allow_pickle='TRUE').item()
            assoc_data.append(read_dictionary)

            # load all the materials as the nodes in network
            load_1 =  pd.read_csv(x + '_' +file_name +'_vs.csv',encoding='cp1252')
            rat_data.append(load_1)

            # load community materials data file 
            load_2 =  pd.read_csv(x + '_' + file_name +'_cluster_element.csv',encoding='cp1252')
            clustering_data.append(load_2)

    for i in range(4):

        # other attributes except conductivity
        if len(rat_data) != 1:
        
            # draw the network with all nodes
            network_graph(rat_data[i],assoc_data[i])
    
            # draw the network with nodes that have edges
            network_graph2(assoc_data[i])

            # plot the materials distribution from the network community
            attribute_time_plot(clustering_data[i],figNum = i+1)

        # for the conductivity attribut file has only one column
        else:
             
            # draw the network with all nodes
            network_graph(rat_data[0],assoc_data[0])
    
            # draw the network with nodes that have edges
            network_graph2(assoc_data[0])

            # plot the materials distribution from the network community
            attribute_time_plot(clustering_data[0],figNum = 0+1)

