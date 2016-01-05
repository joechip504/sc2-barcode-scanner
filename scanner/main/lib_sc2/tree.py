from . import constants
from . import kdtree
import dill as pickle

class Node(object):

	def __init__(self, **kwargs):
		self.player_name  = kwargs.get('player_name')
		self.player_race  = kwargs.get('player_race')
		self.hotkey_info  = kwargs.get('hotkey_info')
		self.player_url  = kwargs.get('player_url')


	def __repr__(self):
		return '{} - {} - {}'.format(self.player_name, self.player_race, self.hotkey_info)

	def __getitem__(self, item):
		return self.hotkey_info[item]

	def __len__(self):
		return len(self.hotkey_info)

class ReplayKDTree(object):

	def __init__(self, nodes):
		self.tree = kdtree.create(nodes, dimensions = 10)

	def add(self, node):
		self.tree.add(node)
		self.tree = self.tree.rebalance()

	def search_knn(self, node, k, dist = None):
		return self.tree.search_knn(node, k = k, dist = dist)

	def visualize(self):
		kdtree.visualize(self.tree)



# if __name__ == '__main__':
# 	pass