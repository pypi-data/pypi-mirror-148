
from nintendo.pia import packet, streams
import copy


FLAG_MULTICAST = 1


class Message:
	def __init__(self):
		self.flags = 0
		self.station_index = 0xFD
		self.destination = 0
		self.source = 0
		self.protocol_id = 0
		self.protocol_port = 0
		self.payload = b""


class MessageEncoderV1:
	def __init__(self, settings):
		self.settings = settings
	
	def decode(self, data):
		stream = streams.StreamIn(data, self.settings)
		
		messages = []
		while not stream.eof():
			message = Message()
			message.flags = stream.u8()
			message.station_index = stream.u8()
			size = stream.u16()
			message.destination = stream.u32()
			message.source = stream.u32()
			message.protocol_id = stream.u16()
			message.protocol_port = stream.u16()
			stream.pad(4)
			message.payload = stream.read(size)
			stream.align(4)
			messages.append(message)
		return messages
	
	def encode(self, messages):
		stream = streams.StreamOut(self.settings)
		for message in messages:
			stream.u8(message.flags)
			stream.u8(message.station_index)
			stream.u16(len(message.payload))
			stream.u32(message.destination)
			stream.u32(message.source)
			stream.u16(message.protocol_id)
			stream.u16(message.protocol_port)
			stream.pad(4)
			stream.write(message.payload)
			stream.align(4)
		return stream.get()


class MessageEncoderV2:
	def __init__(self, settings):
		self.settings = settings
	
	def decode(self, data):
		stream = streams.StreamIn(data, self.settings)
		
		messages = []
		while not stream.eof():
			message = Message()
			message.flags = stream.u8()
			size = stream.u16()
			message.destination = stream.u64()
			message.source = stream.u64()
			message.protocol_id = stream.u8()
			message.protocol_port = stream.u8()
			stream.pad(3)
			message.payload = stream.read(size)
			stream.align(4)
			messages.append(message)
		return messages
	
	def encode(self, messages):
		stream = streams.StreamOut(self.settings)
		for message in messages:
			stream.u8(message.flags)
			stream.u16(len(message.payload))
			stream.u64(message.destination)
			stream.u64(message.source)
			stream.u8(message.protocol_id)
			stream.u8(message.protocol_port)
			stream.pad(3)
			stream.write(message.payload)
			stream.align(4)
		return stream.get()


class MessageEncoderV3:
	def __init__(self, settings):
		self.settings = settings
	
	def decode(self, data):
		stream = streams.StreamIn(data, self.settings)
		
		messages = []
		while not stream.eof():
			message = Message()
			message.flags = stream.u8()
			if stream.u8() != 1:
				raise ValueError("Message has wrong version number")
			size = stream.u16()
			message.protocol_id = stream.u8()
			message.protocol_port = stream.u8()
			message.destination = stream.u64()
			message.source = stream.u64()
			message.payload = stream.read(size)
			stream.align(4)
			messages.append(message)
		return messages
	
	def encode(self, messages):
		stream = streams.StreamOut(self.settings)
		for message in messages:
			stream.u8(message.flags)
			stream.u8(1)
			stream.u16(len(message.payload))
			stream.u8(message.protocol_id)
			stream.u8(message.protocol_port)
			stream.u64(message.destination)
			stream.u64(message.source)
			stream.write(message.payload)
			stream.align(4)
		return stream.get()


class MessageEncoderV4:
	def __init__(self, settings):
		self.settings = settings
	
	def decode(self, data):
		stream = streams.StreamIn(data, self.settings)
		
		messages = []
		while not stream.eof():
			message = Message()
			message.flags = stream.u8()
			if stream.u8() != 2:
				raise ValueError("Message has wrong version number")
			size = stream.u16()
			message.protocol_id = stream.u8()
			message.protocol_port = stream.u24()
			message.destination = stream.u64()
			message.source = stream.u64()
			message.payload = stream.read(size)
			stream.align(4)
			messages.append(message)
		return messages
	
	def encode(self, messages):
		stream = streams.StreamOut(self.settings)
		for message in messages:
			stream.u8(message.flags)
			stream.u8(2)
			stream.u16(len(message.payload))
			stream.u8(message.protocol_id)
			stream.u24(message.protocol_port)
			stream.u64(message.destination)
			stream.u64(message.source)
			stream.write(message.payload)
			stream.align(4)
		return stream.get()


class MessageEncoderV5:
	def __init__(self, settings):
		self.settings = settings
	
	def decode(self, data):
		stream = streams.StreamIn(data, self.settings)
		
		messages = []
		
		size = None
		message = Message()
		while not stream.eof():
			flags = stream.u8()
			
			if flags & 1: message.flags = stream.u8()
			if flags & 2: size = stream.u16()
			if flags & 4:
				message.protocol_id = stream.u8()
				message.protocol_port = stream.u24()
			if flags & 8: message.destination = stream.u64()
			if flags & 16: message.source = stream.u64()
			
			message.payload = stream.read(size)
			stream.align(4)
			
			messages.append(message)
			message = copy.copy(message)
		
		return messages
	
	def encode(self, messages):
		stream = streams.StreamOut(self.settings)
		
		prev = Message()
		for message in messages:
			flags = 0
			if message.flags != prev.flags: flags |= 1
			if len(message.payload) != len(prev.payload): flags |= 2
			if message.protocol_id != prev.protocol_id or message.protocol_port != prev.protocol_port:
				flags |= 4
			if message.destination != prev.destination: flags |= 8
			if message.source != prev.source: flags |= 16
			
			stream.u8(flags)
			if flags & 1: stream.u8(message.flags)
			if flags & 2: stream.u16(len(message.payload))
			if flags & 4:
				stream.u8(message.protocol_id)
				stream.u24(message.protocol_port)
			if flags & 8: stream.u64(message.destination)
			if flags & 16: stream.u64(message.source)
			
			stream.write(message.payload)
			stream.align(4)
			
			prev = message
		return stream.get()


class MessageEncoderV6:
	def __init__(self, settings):
		self.settings = settings
	
	def decode(self, data):
		stream = streams.StreamIn(data, self.settings)
		
		messages = []
		
		size = None
		message = Message()
		while not stream.eof():
			flags = stream.u8()
			
			if flags & 1: message.flags = stream.u8()
			if flags & 2: size = stream.u16()
			if flags & 4:
				message.protocol_id = stream.u8()
				message.protocol_port = stream.u24()
			if flags & 8: message.destination = stream.u64()
			
			message.payload = stream.read(size)
			stream.align(4)
			
			messages.append(message)
			message = copy.copy(message)
		
		return messages
	
	def encode(self, messages):
		stream = streams.StreamOut(self.settings)
		
		prev = Message()
		for message in messages:
			flags = 0
			if message.flags != prev.flags: flags |= 1
			if len(message.payload) != len(prev.payload): flags |= 2
			if message.protocol_id != prev.protocol_id or message.protocol_port != prev.protocol_port:
				flags |= 4
			if message.destination != prev.destination: flags |= 8
			
			stream.u8(flags)
			if flags & 1: stream.u8(message.flags)
			if flags & 2: stream.u16(len(message.payload))
			if flags & 4:
				stream.u8(message.protocol_id)
				stream.u24(message.protocol_port)
			if flags & 8: stream.u64(message.destination)
			
			stream.write(message.payload)
			stream.align(4)
			
			prev = message
		return stream.get()


class MessageEncoder:
	def __init__(self, settings):
		self.encoder = self.make_encoder(settings)
	
	def make_encoder(self, settings):
		version = settings["pia.version"]
		if version <= 504: return MessageEncoderV1(settings)
		elif 506 <= version <= 510: return MessageEncoderV2(settings)
		elif 511 <= version <= 512: return MessageEncoderV3(settings)
		elif 514 <= version <= 517: return MessageEncoderV4(settings)
		elif 518 <= version <= 526: return MessageEncoderV5(settings)
		elif 527 <= version <= 616: return MessageEncoderV6(settings)
		else:
			raise ValueError("Unsupported pia version")
	
	def decode(self, data): return self.encoder.decode(data)
	def encode(self, messages): return self.encoder.encode(messages)


class MessageTransport:
	def __init__(self, transport, settings):
		self.transport = transport
		self.encoder = MessageEncoder(settings)
	
	async def send(self, messages, address, encrypt=True):
		pack = packet.Packet()
		pack.payload = self.encoder.encode(messages)
		pack.encrypted = encrypt
		await self.transport.send(pack, address)
	
	async def receive(self):
		packet, address = await self.transport.receive()
		try:
			messages = self.encoder.decode(packet.payload)
			return messages, address
		except Exception:
			logger.warning("Received invalid message buffer")


class MessageHandler:
	def __init__(self, transport, stations, settings):
		self.transport = MessageTransport(transport, settings)
		self.stations = stations
	
	async def send(self, message, address, encrypt=True):
		local = self.stations.local_station()
		message.station_index = local.index
		message.source = local.constant_id
		await self.transport.send([message], address, encrypt)
	
	async def send_station(self, message, index, encrypt=True):
		station = self.stations.find_by_index(index)
		message.flags &= ~FLAG_MULTICAST
		message.destination = station.constant_id
		await self.send(message, station.address, encrypt)
