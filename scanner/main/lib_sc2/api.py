import sc2reader
from replayparser import ReplayParser
from tree import Node, ReplayKDTree

class SC2BarcodeScannerAPI(object):

	def __init__(self):
		'''
		will deserialize everything here
		'''
		self.parser = ReplayParser()

	def guess_from_ladder_replay(self, replay_file_path):
		pass

	def add_tournament_replay(self, replay_file_path):
		'''
		can assert not ladder type
		'''
		replay = self.parser.load_replay(replay_file_path)
		for player in replay.players:
			hotkey_info = self.parser.extract_hotkey_info(replay, player)


if __name__ == '__main__':
	SC2BarcodeScannerAPI().add_tournament_replay('test.SC2Replay')