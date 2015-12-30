import sc2reader
import logging

class ReplayParser(object):

	WARNING_SC2READER_LOAD 	= '''
	Unable to load replay - {}
	Error - {}
	'''

	WARNING_REPLAY_VALIDATE = '''
	Error validating replay - {} 
	Must be 2 player LOTV replay
	'''
	
	def __init__(self):
		self.logger = logging.getLogger('ReplayParser')
		self.logger.setLevel(logging.DEBUG)
		self.sha1_id = None

	def validate_replay(self, replay):
		'''
		Must be LOTV replay with 2 players
		'''
		return all((
			len(replay.players) == 2, 
			))

	def extract_hotkey_info(self, replay, player_id):
		pass

	def extract_player_info(self, replay, player_id):
		pass

	def get_replay(self, replay_file_path):
		"""
		"""
		try:
			replay = sc2reader.load_replay(replay_file_path)
		except Exception as e:
			self.logger.warning(self.WARNING_SC2READER_LOAD.format(replay_file_path, str(e)))
			return None

		if not self.validate_replay(replay):
			self.logger.warning(self.WARNING_REPLAY_VALIDATE.format(replay_file_path))
			return None

		self.logger.info('Parsing - {}'.format(replay.filename))
		

if __name__ == '__main__':
	parser = ReplayParser()
	parser.parse_replay('test.SC2Replay')