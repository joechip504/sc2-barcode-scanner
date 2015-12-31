import kdtree
import dill as pickle

class Node(object):
	'''
	{
	'player_name' : 'HuK', 
	'player_race' : '', 
	'player_url'  : '', 
	'hotkey_data' : [1, 12, 14, 2, ... 6], 
	'winner'  : 'HuK', 
	'time_elapsed' : 123, 
	}
	'''
	pass

class ReplayKDTree(object):
	
	def __init__(self):
		self.tree = None
		self.replay_ids = set()

if __name__ == '__main__':
	pass