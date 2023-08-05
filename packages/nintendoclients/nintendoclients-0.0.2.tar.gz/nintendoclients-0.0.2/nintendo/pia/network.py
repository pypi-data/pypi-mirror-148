
class NetworkInterface:
	def generate_nonce(self, packet, addr):
		raise NotImplementedError("%s.generate_nonce" %self.__class__.__name__)
