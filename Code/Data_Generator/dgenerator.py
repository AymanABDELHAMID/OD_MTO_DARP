#  April 2020 - Ayman Mahmoud
#
# this code generates booking data
# input: (<--) :
# output: (-->) :

import numpy as np
import matplotlib.pyplot as plt
import itertools
import networkx as nx

"""
Generate a coordinate graph
"""
station_size = 50
total_size = station_size*9 # possible locations to have

Graph = nx.Graph()

Graph.add_nodes_from([2,3])


