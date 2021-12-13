#!python3

"""
Calculate the Shapley value in the ride-sharing problem,
with a single pickup location and a fixed dropoff order.
Reference:
Chaya Levinger, Noam Hazon, Amos Azaria (2019)
[Fair Sharing: The Shapley Value for Ride-Sharing and Routing Games](https://arxiv.org/abs/1909.04713)
Since: 2019-12
"""

import networkx
from networkx import Graph

import logging , sys
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.INFO)


def show(map_player_to_shapley_value):
	"""
	Print the Shapley values to screen.
	"""
	for player,value in map_player_to_shapley_value.items():
		print("Shapley value of {} is {}".format(player, value))


def shapley_values_efficient(road_graph:Graph, path:list):
	"""
	Calculates the Shapley values for all players in an instance of the ride-sharing problem.
	Uses an efficient calculation, based on Levinger, Hazon, and Azaria (2019)
	:param road_graph:  a weighted directed graph, representing travel costs between destinations.
	                    "0" denotes the source; all other nodes are destinations.
	:param path: the first element is the source; then comes the list of passangers, in the fixed order by which they should be dropped from the taxi.
	:return: a dict where each key is a single char representing a passanger, and each value is the player's Shapley value.
	"""
	source = path[0]
	# NOTE: player index starts at 1. Source is 0.
	map_player_to_value = {player:0.0 for player in path[1:]}


	for k in range(1, len(path)):  # NOTE: player index starts at 1. Source is 0.
		d_0_k = networkx.dijkstra_path_length(road_graph, source, path[k])
		logger.info("Calculate Shapley-values for sub-problem with only d[0,%d] (= %f):", k, d_0_k)
		logger.info("  Player %d adds d[0,%d] whenever he is first among 1,...,%d, which happens in 1/%d of the orders.", k, k, k, k)
		map_player_to_value[path[k]] += d_0_k / k  # player k adds d_0_k whenever he is first among 1,...,k, which happens in 1/k of the orders.
		print("		", map_player_to_value, '\n')

		for j in range(1, k):                          # each player j<k removes d_0_k whenever he is first among 1,...,k-1 that comes after k.
			logger.info("  Player %d removes d[0,%d] whenever he is first among 1,...,%d-1 that comes after %d, which happens in 1/%d*(%d-1) of the orders.", j, k, k, k,  k, k)
			map_player_to_value[path[j]] -= d_0_k / k / (k-1)  # This happens in 1/k(k-1) of the orders.
			print("		", map_player_to_value, '\n')

		for i in range(1, k):
			d_i_k = networkx.dijkstra_path_length(road_graph, path[i], path[k])
			logger.info("Calculate Shapley-values for sub-problem with only d[%d,%d] (= %f):", i, k, d_i_k)
			logger.info("  Players %d and %d add d[%d,%d] whenever %d is second and %d is first among %d,...,%d, which happens in 1/(%d-%d+1)*(%d-%d) of the orders.", i,k, i,k, i,k, i,k, k,i, k,i)
			map_player_to_value[path[i]] += d_i_k / (k-i+1) / (k-i)
			map_player_to_value[path[k]] += d_i_k / (k-i+1) / (k-i)
			print("		", map_player_to_value, '\n')

			for j in range(i+1, k):                         # each player j with i<j<k removes d_i_k whenever he is first among i+1,...,k-1 that comes after i,k.
				logger.info(
					"  Player %d removes d[%d,%d] whenever he is third and %d, %d are first, which happens in 2/(%d-%d+1)*(%d-%d)*(%d-%d-1) of the orders.",
					j, i, k, i,k, k, i, k, i , k, i)

				map_player_to_value[path[j]] -= d_i_k / (k-i+1) / (k-i) / (k-i-1) * 2
				print("		", map_player_to_value, '\n')

	return map_player_to_value


if __name__ == "__main__":
	print("\n## Ride-sharing example - 3 travelers")
	road_graph = networkx.Graph()
	road_graph.add_edge("Ariel", "X", weight=70)
	road_graph.add_edge("X", "Oranit", weight=20)
	road_graph.add_edge("X", "Shaare Tikva", weight=30)
	road_graph.add_edge("X", "Rosh Haayn", weight=40)

	print("\n#### Efficient calculation")
	show(shapley_values_efficient(road_graph, ["Ariel",  "Shaare Tikva", "Oranit", "Rosh Haayn"]))