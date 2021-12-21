#!python3

"""
Demo of Shapley value calculation in the ride-sharing problem.
Programmer: Erel Segal-Halevi
Since: 2019-12
"""
import networkx
from networkx import DiGraph


import ridesharing, logging, sys
ridesharing.logger.addHandler(logging.StreamHandler(sys.stdout))
ridesharing.logger.setLevel(logging.INFO)

import shapley
shapley.logger.addHandler(logging.StreamHandler(sys.stdout))
shapley.logger.setLevel(logging.INFO)

if __name__ == '__main__':


    print("\n## Ride-sharing example - 3 travelers")
    road_graph = networkx.Graph()
    road_graph.add_edge("Ariel", "X", weight=70)
    road_graph.add_edge("X", "Oranit", weight=20)
    road_graph.add_edge("X", "Shaare Tikva", weight=30)
    road_graph.add_edge("X", "Rosh Haayn", weight=40)


    print("\n#### Efficient calculation")
    shapley.show(ridesharing.shapley_values_efficient(road_graph, ["Ariel",  "Oranit", "Shaare Tikva", "Rosh Haayn"]))