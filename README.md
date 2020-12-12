# battery_data_visualization
Lithium-ion battery material research data visualization

Firstly, the simple_vs.py is to visulize the material properties directly from the dataset
Frequency vs. attributes (('Capacity','mAh/g'), ('Voltage','V'), ('Conductivity', 's/cm'), 
                ('Coulombic Efficiency', '%'), ('Energy', 'Wh/kg'))

This battery_data_vs.py is to load the calculated files which is saved from ds.py
Then import the plot functions from batter_plot.py to plot the network graphes, material distribution, statistic summarization

The ds.py is to clean the database and regulated the materials to cathodes and anodes
Defining materials which have connection with other and calculate the weights:
    weights = 1/3(similarity_name + closeness of property value + closeness of date)
The database is huge, this project ramdonly select 5000 rows (5000 materials from 5000 literature) 
to process. Finally write the regulated and calculated file and save.

The battery_plot.py is to implement the ploting functions for the battery_data_vs.py. The attribute_time_plot() is to plot the materials distribution figure,
The network_graphe(),is to plot the network figure with all the nodes, The network_graphe2(),is to plot the network figure with all the connected nodes,
the above network_graph functions give statistic summarization.


Bill
12/12/2020
