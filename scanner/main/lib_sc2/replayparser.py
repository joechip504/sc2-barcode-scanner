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

	CONTROL_GROUP_EVENTS = (
		'SetControlGroupEvent', 
		'GetControlGroupEvent', 
		'AddToControlGroupEvent'
		)
	
	def __init__(self):
		self.logger = logging.getLogger('ReplayParser')
		self.logger.setLevel(logging.DEBUG)

	def validate_replay(self, replay):
		'''
		Must be LOTV replay with 2 players
		'''
		return all((
			len(replay.players) == 2, 
			))

	def extract_hotkey_info(self, replay, player):
		hotkey_data = [0] * 10

		control_group_events = [
			event for event in replay.events if (
			event.name in self.CONTROL_GROUP_EVENTS and
			player.uid == event.pid
			)]

		for event in control_group_events:
			hotkey_data[event.control_group] += 1

		for i in range(len(hotkey_data)):
			hotkey_data[i] /= replay.length.mins
			hotkey_data[i] = int(hotkey_data[i])

		return hotkey_data

	def load_replay(self, replay_file_path):
		try:
			replay = sc2reader.load_replay(replay_file_path, load_level = 4)
		except Exception as e:
			self.logger.warning(self.WARNING_SC2READER_LOAD.format(replay_file_path, str(e)))
			return None

		if not self.validate_replay(replay):
			self.logger.warning(self.WARNING_REPLAY_VALIDATE.format(replay_file_path))
			return None

		self.logger.info('Parsing - {}'.format(replay.filename))
		return replay
		

if __name__ == '__main__':
	parser = ReplayParser()
	parser.parse_replay('test.SC2Replay')