class Player(object):
	def __init__(self, percent_match, sample_size, url, name):
		self.name = name
		self.confidence = percent_match
		self.url = url
		self.sample_size = sample_size

	def __lt__(self, other):
		# return self.confidence < other.confidence
		return self.sample_size < other.sample_size

	def __repr__(self):
		return self.url