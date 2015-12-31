import constants
import dill as pickle
import hashlib
import logging
import os.path
import sc2reader
from replayparser import ReplayParser
from tree import Node, ReplayKDTree

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
		pass

	def add_tournament_replay(self, replay_file_path):
		'''
		check if we've already added this replay
		can assert not ladder type
		'''
		replay_id = hashlib.sha1(
			open(replay_file_path, mode = 'rb').read()
			).hexdigest()

		if replay_id in self.replay_ids:
			self.logger.warning('Replay already exists in database - {}'.format(replay_file_path))
			self.tree.visualize()
			return

		replay = self.parser.load_replay(replay_file_path)
		self.replay_ids.add(replay_id)

		for player in replay.players:
			node_kwargs = {
			'player_name' : player.name, 
			'player_race' : player.play_race,
			'hotkey_info' : self.parser.extract_hotkey_info(replay, player),
			}
			node = Node(**node_kwargs)
			self.tree_nodes.append(node)
			self.tree.add(node)

		with open(constants.PATH_REPLAY_IDS, mode = 'wb') as f:
			pickle.dump(self.replay_ids, f)

		with open(constants.PATH_TREE_NODES, mode = 'wb') as f:
			pickle.dump(self.tree_nodes, f)








if __name__ == '__main__':
	SC2BarcodeScannerAPI().add_tournament_replay('test.SC2Replay')