
from nintendo.pia import streams
from Crypto.Cipher import AES
import random
import struct
import time

import logging
logger = logging.getLogger(__name__)


def pad(data):
	return data + b"\xFF" * ((16 - len(data) % 16) % 16)


class Packet:
	def __init__(self):
		self.encrypted = False
		self.connection_id = 0
		self.destination_id = 0
		self.source_id = 0
		self.sequence_id = 0
		self.session_timer = 0
		self.rtt_timer = 0
		self.nonce = 0
		self.payload = b""
		self.footer = b""


class PacketEncoderV1:
	def __init__(self, network, settings):
		self.settings = settings
	
	def decode(self, data, addr):
		stream = streams.StreamIn(data, self.settings)
		if stream.u32() != 0x32AB9864:
			raise ValueError("Packet has wrong magic number")
		
		encryption = stream.u8()
		if encryption not in [1, 2]:
			raise ValueError("Packet has unexpected encryption mode")
		
		packet = Packet()
		packet.encrypted = encryption == 2
		packet.connection_id = stream.u8()
		packet.sequence_id = stream.u16()
		packet.session_timer = stream.u16()
		packet.rtt_timer = stream.u16()
		packet.payload = stream.read(stream.available() - 16)
		
		signature = stream.read(16)
		if hmac.digest(self.settings["crypto.session_key"], data[:-16], "md5") != signature:
			raise ValueError("Signature is invalid")
		
		if packet.encrypted:
			aes = AES.new(self.settings["crypto.session_key"], AES.MODE_ECB)
			packet.payload = aes.decrypt(packet.payload)
		
		return packet
	
	def encode(self, packet, addr):
		stream = streams.StreamOut(self.settings)
		
		payload = packet.payload
		if packet.encrypted:
			aes = AES.new(self.settings["crypto.session_key"], AES.MODE_ECB)
			payload = aes.encrypt(pad(packet.payload))
		
		stream.u32(0x32AB9864)
		stream.u8(2 if packet.encrypted else 1)
		stream.u8(packet.connection_id)
		stream.u16(packet.sequence_id)
		stream.u16(packet.session_timer)
		stream.u16(packet.rtt_timer)
		stream.write(payload)
		stream.write(hmac.digest(self.settings["crypto.session_key"], stream.get(), "md5"))
		return stream.get()


class PacketEncoderV2:
	def __init__(self, network, settings):
		self.network = network
		self.settings = settings
	
	def decode(self, data, addr):
		stream = streams.StreamIn(data, self.settings)
		if stream.u32() != 0x32AB9864:
			raise ValueError("Packet has wrong magic number")
		
		encryption = stream.u8()
		if encryption not in [1, 2]:
			raise ValueError("Packet has unexpected encryption mode")
		
		packet = Packet()
		packet.encrypted = encryption == 2
		packet.connection_id = stream.u8()
		packet.sequence_id = stream.u16()
		packet.session_timer = stream.u16()
		packet.rtt_timer = stream.u16()
		packet.nonce = stream.u64()
		signature = stream.read(16)
		packet.payload = stream.readall()
		
		if packet.encrypted:
			nonce = self.network.generate_nonce(packet, addr)
			aes = AES.new(self.settings["crypto.session_key"], AES.MODE_GCM, nonce=nonce)
			packet.payload = aes.decrypt_and_verify(packet.payload, signature)
		
		return packet
	
	def encode(self, packet, addr):
		signature = bytes(16)
		payload = packet.payload
		if packet.encrypted:
			nonce = self.network.generate_nonce(packet, addr)
			aes = AES.new(self.settings["crypto.session_key"], AES.MODE_GCM, nonce=nonce)
			payload, signature = aes.encrypt_and_digest(packet.payload)
		
		stream = streams.StreamOut(self.settings)
		stream.u32(0x32AB9864)
		stream.u8(2 if packet.encrypted else 1)
		stream.u8(packet.connection_id)
		stream.u16(packet.sequence_id)
		stream.u16(packet.session_timer)
		stream.u16(packet.rtt_timer)
		stream.u64(packet.nonce)
		stream.write(signature)
		stream.write(payload)
		return stream.get()


class PacketEncoderV3:
	def __init__(self, network, settings):
		self.network = network
		self.settings = settings
	
	def decode(self, data, addr):
		stream = streams.StreamIn(data, self.settings)
		if stream.u32() != 0x32AB9864:
			raise ValueError("Packet has wrong magic number")
		
		encryption = stream.u8()
		if encryption & 0x7F != 3:
			raise ValueError("Packet has unexpected version number")
		
		packet = Packet()
		packet.encrypted = bool(encryption & 0x80)
		packet.connection_id = stream.u8()
		packet.sequence_id = stream.u16()
		packet.nonce = stream.u64()
		signature = stream.read(16)
		packet.payload = stream.readall()
		
		if packet.encrypted:
			nonce = self.network.generate_nonce(packet, addr)
			aes = AES.new(self.settings["crypto.session_key"], AES.MODE_GCM, nonce=nonce)
			packet.payload = aes.decrypt_and_verify(packet.payload, signature)
		
		return packet
	
	def encode(self, packet, addr):
		signature = bytes(16)
		payload = packet.payload
		if packet.encrypted:
			nonce = self.network.generate_nonce(packet, addr)
			aes = AES.new(self.settings["crypto.session_key"], AES.MODE_GCM, nonce=nonce)
			payload, signature = aes.encrypt_and_digest(packet.payload)
		
		stream = streams.StreamOut(self.settings)
		stream.u32(0x32AB9864)
		stream.u8((packet.encrypted << 7) | 3)
		stream.u8(packet.connection_id)
		stream.u16(packet.sequence_id)
		stream.u64(packet.nonce)
		stream.write(signature)
		stream.write(payload)
		return stream.get()


class PacketEncoderV4:
	def __init__(self, network, settings):
		self.network = network
		self.settings = settings
	
	def decode(self, data, addr):
		stream = streams.StreamIn(data, self.settings)
		if stream.u32() != 0x32AB9864:
			raise ValueError("Packet has wrong magic number")
		
		encryption = stream.u8()
		if encryption & 0x7F != 4:
			raise ValueError("Packet has unexpected version number")
		
		packet = Packet()
		packet.encrypted = bool(encryption & 0x80)
		packet.connection_id = stream.u8()
		packet.sequence_id = stream.u16()
		packet.nonce = stream.u64()
		signature = stream.read(16)
		packet.payload = stream.readall()
		
		if packet.encrypted:
			nonce = self.network.generate_nonce(packet, addr)
			aes = AES.new(self.settings["crypto.session_key"], AES.MODE_GCM, nonce=nonce)
			packet.payload = aes.decrypt_and_verify(packet.payload, signature)
		
		return packet
	
	def encode(self, packet, addr):
		signature = bytes(16)
		payload = packet.payload
		if packet.encrypted:
			nonce = self.network.generate_nonce(packet, addr)
			aes = AES.new(self.settings["crypto.session_key"], AES.MODE_GCM, nonce=nonce)
			payload, signature = aes.encrypt_and_digest(packet.payload)
		
		stream = streams.StreamOut(self.settings)
		stream.u32(0x32AB9864)
		stream.u8((packet.encrypted << 7) | 4)
		stream.u8(packet.connection_id)
		stream.u16(packet.sequence_id)
		stream.u64(packet.nonce)
		stream.write(signature)
		stream.write(payload)
		return stream.get()


class PacketEncoderV5:
	def __init__(self, network, settings):
		self.network = network
		self.settings = settings
	
	def decode(self, data, addr):
		stream = streams.StreamIn(data, self.settings)
		if stream.u32() != 0x32AB9864:
			raise ValueError("Packet has wrong magic number")
		
		encryption = stream.u8()
		if encryption & 0x7F != 5:
			raise ValueError("Packet has unexpected version number")
		
		packet = Packet()
		packet.encrypted = bool(encryption & 0x80)
		packet.connection_id = stream.u8()
		packet.sequence_id = stream.u16()
		packet.nonce = stream.u64()
		signature = stream.read(8)
		packet.payload = stream.readall()
		
		if packet.encrypted:
			nonce = self.network.generate_nonce(packet, addr)
			aes = AES.new(self.settings["crypto.session_key"], AES.MODE_GCM, nonce=nonce)
			packet.payload = aes.decrypt_and_verify(packet.payload, signature)
		
		return packet
	
	def encode(self, packet, addr):
		signature = bytes(16)
		payload = packet.payload
		if packet.encrypted:
			nonce = self.network.generate_nonce(packet, addr)
			aes = AES.new(self.settings["crypto.session_key"], AES.MODE_GCM, nonce=nonce)
			payload, signature = aes.encrypt_and_digest(packet.payload)
		
		stream = streams.StreamOut(self.settings)
		stream.u32(0x32AB9864)
		stream.u8((packet.encrypted << 7) | 5)
		stream.u8(packet.connection_id)
		stream.u16(packet.sequence_id)
		stream.u64(packet.nonce)
		stream.write(signature)
		stream.write(payload)
		return stream.get()


class PacketEncoderV9:
	def __init__(self, network, settings):
		self.network = network
		self.settings = settings
	
	def decode(self, data, addr):
		stream = streams.StreamIn(data, self.settings)
		if stream.u32() != 0x32AB9864:
			raise ValueError("Packet has wrong magic number")
		
		encryption = stream.u8()
		if encryption & 0x7F != 9:
			raise ValueError("Packet has unexpected version number")
		
		packet = Packet()
		packet.encrypted = bool(encryption & 0x80)
		packet.destination_id = stream.u32()
		packet.source_id = stream.u32()
		packet.sequence_id = stream.u16()
		footer_size = stream.u8()
		packet.nonce = stream.u64()
		signature = stream.read(8)
		packet.payload = stream.read(stream.available() - footer_size)
		packet.footer = stream.read(footer_size)
		
		if packet.encrypted:
			nonce = self.network.generate_nonce(packet, addr)
			aes = AES.new(self.settings["crypto.session_key"], AES.MODE_GCM, nonce=nonce)
			packet.payload = aes.decrypt_and_verify(packet.payload, signature)
		
		return packet
	
	def encode(self, packet, addr):
		signature = bytes(16)
		payload = packet.payload
		if packet.encrypted:
			nonce = self.network.generate_nonce(packet, addr)
			aes = AES.new(self.settings["crypto.session_key"], AES.MODE_GCM, nonce=nonce)
			payload, signature = aes.encrypt_and_digest(packet.payload)
		
		stream = streams.StreamOut(self.settings)
		stream.u32(0x32AB9864)
		stream.u8((packet.encrypted << 7) | 9)
		stream.u32(packet.destination_id)
		stream.u32(packet.source_id)
		stream.u16(packet.sequence_id)
		stream.u8(len(packet.footer))
		stream.u64(packet.nonce)
		stream.write(signature)
		stream.write(payload)
		stream.write(packet.footer)
		return stream.get()


class PacketEncoderV11:
	def __init__(self, network, settings):
		self.network = network
		self.settings = settings
	
	def decode(self, data, addr):
		stream = streams.StreamIn(data, self.settings)
		if stream.u32() != 0x32AB9864:
			raise ValueError("Packet has wrong magic number")
		
		encryption = stream.u8()
		if encryption & 0x7F != 11:
			raise ValueError("Packet has unexpected version number")
		
		packet = Packet()
		packet.encrypted = bool(encryption & 0x80)
		packet.destination_id = stream.u16()
		packet.source_id = stream.u16()
		packet.sequence_id = stream.u16()
		footer_size = stream.u8()
		packet.nonce = stream.u64()
		signature = stream.read(8)
		packet.payload = stream.read(stream.available() - footer_size)
		packet.footer = stream.read(footer_size)
		
		if packet.encrypted:
			nonce = self.network.generate_nonce(packet, addr)
			aes = AES.new(self.settings["crypto.session_key"], AES.MODE_GCM, nonce=nonce)
			packet.payload = aes.decrypt_and_verify(packet.payload, signature)
		
		return packet
	
	def encode(self, packet, addr):
		signature = bytes(16)
		payload = packet.payload
		if packet.encrypted:
			nonce = self.network.generate_nonce(packet, addr)
			aes = AES.new(self.settings["crypto.session_key"], AES.MODE_GCM, nonce=nonce)
			payload, signature = aes.encrypt_and_digest(packet.payload)
		
		stream = streams.StreamOut(self.settings)
		stream.u32(0x32AB9864)
		stream.u8((packet.encrypted << 7) | 11)
		stream.u16(packet.destination_id & 0xFFFF)
		stream.u16(packet.source_id & 0xFFFF)
		stream.u16(packet.sequence_id)
		stream.u8(len(packet.footer))
		stream.u64(packet.nonce)
		stream.write(signature)
		stream.write(payload)
		stream.write(packet.footer)
		return stream.get()


class PacketEncoder:
	def __init__(self, network, settings):
		self.encoder = self.make_encoder(network, settings)
	
	def make_encoder(self, network, settings):
		version = settings["pia.version"]
		if version <= 506: return PacketEncoderV1(network, settings)
		elif 507 <= version <= 510: return PacketEncoderV2(network, settings)
		elif 511 <= version <= 517: return PacketEncoderV3(network, settings)
		elif 518 <= version <= 521: return PacketEncoderV4(network, settings)
		elif 523 <= version <= 526: return PacketEncoderV5(network, settings)
		elif 527 <= version <= 539: return PacketEncoderV9(network, settings)
		elif version == 616: return PacketEncoderV11(network, settings)
		else:
			raise ValueError("Unsupported pia version")
	
	def decode(self, data, addr): return self.encoder.decode(data, addr)
	def encode(self, packet, addr): return self.encoder.encode(packet, addr)


class PacketTransport:
	def __init__(self, network, settings, socket):
		self.encoder = PacketEncoder(network, settings)
		self.socket = socket
	
	async def send(self, packet, address):
		data = self.encoder.encode(packet, address)
		await self.socket.send(packet, address)
	
	async def receive(self):
		while True:
			data, address = await self.socket.recv()
			try:
				packet = self.encoder.decode(data, address)
				return packet, address
			except Exception:
				logger.warning("Received malformed packet")


class PacketHandler:
	def __init__(self, network, stations, settings, socket):
		self.transport = PacketTransport(network, settings, socket)
		self.stations = stations
		self.settings = settings
		
		self.nonce = random.randint(0, 0xFFFFFFFFFFFFFFFF)
		
		self.timer_base = time.monotonic()
		self.rtt = {}
	
	def next_nonce(self):
		self.nonce = (self.nonce + 1) & 0xFFFFFFFFFFFFFFFF
		return self.nonce
	
	def check_packet(self, packet, address):
		station = self.stations.find_by_address(address)
		if packet.connection_id > 2:
			if station is None or packet.connection_id != station.connection_id_in:
				logger.warning("Received packet with wrong connection id")
				return False
		
		if packet.destination_id != 0:
			local = self.stations.local_station()
			if packet.destination_id & 0xFFFF != local.variable_id & 0xFFFF:
				logger.warning("Received packet with wrong destination variable id")
				return False
		elif packet.footer:
			if len(packet.footer) % 2 != 0:
				logger.warning("Received packet with invalid footer")
				return False
			ids = struct.unpack(">%iH" %(len(packet.footer) // 2, packet.footer)
			if local.variable_id & 0xFFFF not in ids:
				logger.warning("Local variable id not found in packet footer")
				return False
		
		if packet.sequence_id != 0:
			if station is None or not station.check_sequence_id(packet.sequence_id):
				logger.warning("Received packet with wrong sequence id")
				return False
		
		current = int((time.monotonic() - self.timer_base) * 1000)
		self.rtt[address] = (current, packet.session_timer)
	
	async def send(self, packet, address):
		station = self.stations.find_by_address(address)
		if station:
			packet.connection_id = station.connection_id_out
			packet.destination_id = station.variable_id
			packet.sequence_id = station.next_sequence_id()
		
		local = self.stations.local_station()
		packet.source_id = local.variable_id
		
		current = int((time.monotonic() - self.timer_base) * 1000)
		packet.session_timer = current
		if address in self.rtt:
			local, remote = self.rtt[address]
			packet.rtt_timer = remote + (current - local)
		
		packet.nonce = self.next_nonce()
		await self.transport.send(packet, address)
	
	async def receive(self):
		while True:
			packet, address = await self.transport.receive()
			if self.check_packet(packet, address):
				return packet, address
