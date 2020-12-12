import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.mathtext as mathtext

'''
This battery_plot.py is to implement the ploting functions for the IE582.py
The attribute_time_plot() is to plot the materials distribution figure,
The network_graphe(),is to plot the network figure with all the nodes,
The network_graphe2(),is to plot the network figure with all the connected nodes,
the above network_graph functions give statistic summarization

Bo Nie
12/12/2020
'''

def attribute_time_plot(data, figNum):

    # name the figure title
    position = str(data['Property'].values[1] + ' development with publication time') #

    fig = plt.figure(figNum)
    ax = fig.add_subplot(211)
    
    # name the x-label and y-label
    ax.set_xlabel('Date (yy-mm)')
    ax.set_ylabel(str(data['Property'].values[1]) +' ('+ str(data['Unit'].values[1]) +')')
    
    # adjust the font
    mpl.rc("font", family="Times New Roman",weight='normal')
    plt.rcParams.update({'mathtext.default':  'regular' })
    
    cmap = plt.cm.tab10
    colors = cmap(np.arange(data.shape[0]) % cmap.N)

    ax.scatter(data['Year'], data['Value'], c= colors, label=data['Name'])

    ax.legend(fontsize='7',ncol=4, handleheight=0.8, labelspacing=0.03, \
                    loc='lower center',bbox_to_anchor=(0.2, 0.1), frameon=False)
    ax.set_title(position) 
    fig.savefig(str(data['Property'].values[1])+ '_vs' +'.png')
    plt.show()


def network_graph(data,assoc_dictionary):
    G = nx.Graph()

    # set the nodes sets
    for item in data['ID']:
        G.add_node(item)
    
    # set the edge sets and the weight
    for edge, weight in assoc_dictionary.items():
        G.add_edge(edge[0], edge[1], weight=weight)

    # Seed layout for reproducibility
    pos = nx.spring_layout(G, seed=10396953)  

    # draw the nodes, edges, and labels
    nx.draw_networkx_nodes(G, pos, node_size= 20, node_color= 'b')
    nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5)
    nx.draw_networkx_labels(G, pos, font_size=0.5, font_color="whitesmoke")
    nx.draw(G, pos)

    # save and show the figure
    plt.savefig(data['Property'][0]+"_network.png")
    plt.show()
    
    # generate the 'degree_centrality', 'closeness_centrality', 'betweenness_centrality'
    # statistics to describe the network
    degree_centrality = list(nx.degree_centrality(G).values())
    closeness_centrality = list(nx.closeness_centrality(G).values())
    betweenness_centrality = list(nx.betweenness_centrality(G).values())

    # calculate the mean value and std
    Analytic_mean = { "Degree centrality":np.mean(degree_centrality), "Closeness_centrality":np.mean(closeness_centrality),
               "Betweenness centrality":np.mean(betweenness_centrality)}
    Analytic_std = { "Degree centrality":np.std(degree_centrality), "Closeness_centrality":np.std(closeness_centrality),
               "Betweenness centrality":np.std(betweenness_centrality)}
    Analytic = pd.DataFrame(Analytic_mean, index = ['Mean'])
    Analytic = Analytic.append(Analytic_std, ignore_index=True)
    print(Analytic)

def network_graph2(assoc_dictionary):
    G = nx.Graph()

    # the dictionary are materials IDs which are all connected with edge
    data_tuple = list(assoc_dictionary.keys())
    data1, data2 = zip(*data_tuple)
    data = set(data1+data2)

    # set the nodes sets from the connected materials file
    for item in data:
        G.add_node(item)

    # set the edge sets and the weight
    for edge, weight in assoc_dictionary.items():
        G.add_edge(edge[0], edge[1], weight=weight)


    # Seed layout for reproducibility
    pos = nx.spring_layout(G, seed=63) 

    # draw the nodes, edges, and labels
    nx.draw_networkx_nodes(G, pos, node_size= 20, node_color= 'b')
    nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5)
    nx.draw_networkx_labels(G, pos, font_size=1, font_color="whitesmoke")
    nx.draw(G, pos)

    # save and show the figure
    plt.savefig('Capacity_network.png')
    plt.show()

    # generate the 'degree_centrality', 'closeness_centrality', 'betweenness_centrality'
    # statistics to describe the network
    degree_centrality = list(nx.degree_centrality(G).values())
    closeness_centrality = list(nx.closeness_centrality(G).values())
    betweenness_centrality = list(nx.betweenness_centrality(G).values())

    # calculate the mean value and std
    Analytic_mean = { "Degree centrality":np.mean(degree_centrality), "Closeness_centrality":np.mean(closeness_centrality),
               "Betweenness centrality":np.mean(betweenness_centrality)}
    Analytic_std = { "Degree centrality":np.std(degree_centrality), "Closeness_centrality":np.std(closeness_centrality),
               "Betweenness centrality":np.std(betweenness_centrality)}
    Analytic = pd.DataFrame(Analytic_mean, index = ['Mean'])
    Analytic = Analytic.append(Analytic_std, ignore_index=True)
    print('The next one should be...')
    print(Analytic)