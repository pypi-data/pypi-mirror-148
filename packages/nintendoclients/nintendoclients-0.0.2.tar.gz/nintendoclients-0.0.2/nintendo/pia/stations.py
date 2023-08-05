
class Station:
	def __init__(self):
		self.address = None
		
		self.index = 0xFD
		self.connection_id_out = 0
		self.connection_id_in = 0
		self.variable_id = 0
		self.constant_id = 0
		
		self.sequence_id_out = 0
		self.sequence_id_in = 0
	
	def next_sequence_id(self):
		if self.index != 0xFD:
			self.sequence_id_out = max((self.sequence_id_out + 1) & 0xFFFF, 1)
			return self.sequence_id_out
		return 0
	
	def check_sequence_id(self, sequence_id):
		if sequence_id == 0: return True
		
		diff = (sequence_id - self.sequence_id_in) & 0xFFFF
		if diff != 0 and diff < 0x8000:
			self.sequence_id_in = sequence_id
			return True
		return False


class StationTable:
	def __init__(self):
		self.stations = []
		self.create(None)
	
	def create(self, address):
		station = Station()
		station.address = address
		self.stations.append(station)
		return station
	
	def local_station(self):
		return self.find_by_address(None)
	
	def find_by_address(self, address):
		for station in self.stations:
			if station.address == address:
				return station
	
	def find_by_index(self, index):
		for station in self.stations:
			if station.index == index:
				return station
