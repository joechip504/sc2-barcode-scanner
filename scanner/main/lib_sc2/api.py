from . import constants
import dill as pickle
import hashlib
import logging
import math
import os
import os.path
import sc2reader
from .replayparser import ReplayParser
from .tree import Node, ReplayKDTree
import statistics
from collections import defaultdict
import math
from main.models import Player

class SC2BarcodeScannerAPI(object):

	def __init__(self):
		self.parser = ReplayParser()
		self.logger = logging.getLogger('SC2BarcodeScannerAPI')
		self.logger.setLevel(logging.DEBUG)

		# Initialize empty structures if necessary
		if not (os.path.isfile(constants.PATH_REPLAY_IDS) and
			os.path.isfile(constants.PATH_TREE_NODES)):
			with open(constants.PATH_REPLAY_IDS, mode = 'wb') as f:
				pickle.dump(set(), f)

			with open(constants.PATH_TREE_NODES, mode = 'wb') as f:
				pickle.dump(list(), f)

		# Load in existing replay data
		with open(constants.PATH_REPLAY_IDS, 'rb') as f:
			self.replay_ids = pickle.load(f)

		with open(constants.PATH_TREE_NODES, 'rb') as f:
			self.tree_nodes = pickle.load(f)

		# Initialize the tree
		self.tree = ReplayKDTree(self.tree_nodes)

	def guess_from_ladder_replay(self, replay_file_path):
		'''
		Open the replay and guess the identity of both players.
		{
			'player1_name' : [(.918, 'Huk'), (.771, 'CranK'), ...],
			'player2_name' : [(.555, 'Jobama'), (.412, 'sPringle'), ...],
		}
		'''
		replay = self.parser.load_replay(replay_file_path)
		neighbors = {}
		if not replay:
			return neighbors

		for player in replay.players:
			hotkey_info = self.parser.extract_hotkey_info(replay, player)
			node_kwargs = {
			'player_name' : player.name,
			'player_race' : player.play_race,
			'hotkey_info' : hotkey_info,
			}

			def gaussian(v1, v2):
				   	return float('{0:.2f}'.format(100 - sum([(i-j)**2 for i,j in zip(v1, v2)])**.5))

			def mean(v):
				return float('{0:.2f}'.format(statistics.mean(v)))

			def euclid_distance(v1 ,v2):
				dist = math.sqrt(sum([(i-j)**2 for i, j in zip(v1, v2)]))
				if v1.player_race != v2.player_race:
					dist += 10000
				return dist

			def square_rooted(x):
				return round(math.sqrt(sum([a*a for a in x])),3)

			def cosine_similarity(x,y):
				numerator = sum(a*b for a,b in zip(x,y))
				denominator = square_rooted(x)*square_rooted(y)
				denominator = 1 if denominator == 0 else denominator
				return round(numerator/float(denominator),3)
 
			node 	   = Node(**node_kwargs)
			# candidates = [node.data for node, dist in self.tree.search_knn(node, k = 5, dist = manhattan_distance)]

			candidates_by_race 	= [node.data for node, dist in self.tree.search_knn(node, k = 5, dist = euclid_distance) if float(dist) < 1000.0]
			# candidates_by_race 	= [node.data for node, dist in self.tree.search_knn(node, k = 5, dist = euclid_distance) if dist < 10000]

			candidate_dict 		= defaultdict(list)

			for node in candidates_by_race:
				candidate_dict[node.player_name].append(node)

			# Make sure at least 3 replays in this cluster match a player
			candidate_dict = {k : v for k,v in candidate_dict.items() if len(v) > 2}

			player_objs = []

			for p, nodes in candidate_dict.items():
				# percentages = [gaussian(hotkey_info, n.hotkey_info) for n in nodes]
				percentages = [100*cosine_similarity(hotkey_info, n.hotkey_info) for n in nodes]

				player_objs.append(Player(
					mean(percentages),
					len(percentages),
					nodes[0].player_url,
					p))

			neighbors[player.name] = sorted(player_objs, reverse = True)[:8]

			# neighbors[player.name] = sorted([(
			# 	mean(percentages), p, len(percentages)
			# 	) for p, percentages in candidate_dict.items()
			# 	], reverse = True)[:5]

			# neighbors[player.name] = sorted([(
			# 		gaussian(hotkey_info, node.hotkey_info), node.player_name
			# 		) for node in candidates
			# 	], reverse = True)[:5]

		from pprint import pprint
		pprint(neighbors)
		return neighbors

	def get_players(self, replay_file_path):
		replay = self.parser.load_replay(replay_file_path)
		return replay.players if replay else []


	def get_summary_info(self, replay_file_path):
		replay = self.parser.load_replay(replay_file_path)
		return {
			'match_title' : ' vs. '.join([p.name for p in replay.players]),
			'map_name'		: replay.map_name,
			'length'		: replay.game_length, # object
			'category'		: replay.category, # ladder, custom
			'winner'		: replay.winner.players[0].name,
		} if replay else {}

	def add_tournament_replay(self, replay_file_path):
		# Ignore duplicate replays
		replay_id = hashlib.sha1(
			open(replay_file_path, mode = 'rb').read()
			).hexdigest()

		if replay_id in self.replay_ids:
			self.logger.warning('Replay already exists in database - {}'.format(replay_file_path))
			return

		replay = self.parser.load_replay(replay_file_path)
		if not replay:
			return

		self.logger.warning('Adding - {}'.format(replay_file_path))
		self.replay_ids.add(replay_id)

		# Add new information to the tree
		for player in replay.players:
			node_kwargs = {
			'player_name' : player.name,
			'player_race' : player.play_race,
			'player_url' : player.url,
			'hotkey_info' : self.parser.extract_hotkey_info(replay, player),
			}
			node = Node(**node_kwargs)
			self.tree_nodes.append(node)
			self.tree.add(node)

		# Serialize
		with open(constants.PATH_REPLAY_IDS, mode = 'wb') as f:
			pickle.dump(self.replay_ids, f)

		with open(constants.PATH_TREE_NODES, mode = 'wb') as f:
			pickle.dump(self.tree_nodes, f)

	def add_tournament_replay_directory(self, replay_directory):
	    for (dirpath, dirnames, filenames) in os.walk(replay_directory):
	        for replay in filenames:
	            if replay.endswith('.SC2Replay'):
	                replay_file_path = '/'.join([dirpath, replay])
	                self.add_tournament_replay(replay_file_path)

# if __name__ == '__main__':
	## will need to run from django shell to update from now on
	# constants.PATH_TREE_NODES = constants.PATH_TREE_NODES_LOCAL
	# constants.PATH_REPLAY_IDS = constants.PATH_REPLAY_IDS_LOCAL
	# SC2BarcodeScannerAPI().add_tournament_replay('test.SC2Replay')
	# print(SC2BarcodeScannerAPI().guess_from_ladder_replay('test.SC2Replay'))
	# SC2BarcodeScannerAPI().add_tournament_replay_directory('../static/main/tournament_replays/')
