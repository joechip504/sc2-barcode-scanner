import sc2reader
from replayparser import ReplayParser
from tree import Node, ReplayKDTree

class SC2BarcodeScannerAPI(object):

	def __init__(self):
		'''
		will deserialize everything here
		'''
		pass

	def guess_from_ladder_replay(self, replay_file_path):
		pass

	def add_tournament_replay(self, replay_file_path):
		'''
		can assert not ladder type
		'''
		pass


if __name__ == '__main__':
	SC2BarcodeScannerAPI().add_tournament_replay('test.SC2Replay')