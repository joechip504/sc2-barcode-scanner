class Player(object):
	def __init__(self, percent_match, sample_size, url, name):
		self.name = name
		self.confidence = percent_match
		self.url = url
		self.sample_size = sample_size

	def likely_candidate(self):
		return (self.confidence > 95 and self.sample_size > 10) or self.confidence > 99

	def __lt__(self, other):
		# return self.confidence < other.confidence
		if (self.likely_candidate() and other.likely_candidate()):
			return self.confidence < other.confidence

		elif other.likely_candidate():
			return True

		return self.confidence < other.confidence

	def __repr__(self):
		return self.url