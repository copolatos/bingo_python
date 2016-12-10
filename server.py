import sys
from time import sleep, localtime
from weakref import WeakKeyDictionary

from PodSixNet.Server import Server
from PodSixNet.Channel import Channel

class ClientChannel(Channel):
	def __init__(self, *args, **kwargs):
		self.nickname = "anonymous"
		Channel.__init__(self, *args, **kwargs)
		
	def Close(self):
		self._server.DelPlayer(self)

	def Network_login(self, data):
		self.nickname = data['nickname']

	def Network_list(self, data):
		self._server.ListPlayers()
	
class ChatServer(Server):
	channelClass = ClientChannel
	
	def __init__(self, *args, **kwargs):
		Server.__init__(self, *args, **kwargs)
		self.players = WeakKeyDictionary()
		print 'Server launched'
	
	def Connected(self, channel, addr):
		self.AddPlayer(channel)
	
	def ListPlayers(self):
		print "List User : " , [p.nickname for p in self.players]

	def AddPlayer(self, player):
		#print "New Player Connected" + str(player.addr)
		#print "New Player Connected" + p.nickname
		self.players[player] = True
		self.SendPlayers()
		#print "players", [p for p in self.players]
	
	def DelPlayer(self, player):
		print "Deleting Player" + str(player.addr)
		del self.players[player]
		self.SendPlayers()
	
	def SendPlayers(self):
		self.SendToAll({"action": "players", "players": [p.nickname for p in self.players]})

	def SendToAll(self, data):
		[p.Send(data) for p in self.players]
	
	def Launch(self):
		while True:
			self.Pump()
			sleep(0.0001)

s = ChatServer(localaddr=("localhost", 55555))
s.Launch()
