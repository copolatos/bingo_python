import sys
from time import sleep, localtime
from weakref import WeakKeyDictionary
from thread import *
from PodSixNet.Server import Server
from PodSixNet.Channel import Channel

room = {}#room_name:username
rooms = []#list room

class ClientChannel(Channel):
	def __init__(self, *args, **kwargs):
		self.nickname = ""
		#self.room = ""
		Channel.__init__(self, *args, **kwargs)
		
	def Close(self):
	 	self._server.DelPlayer(self)

	def Network_login(self, data):
		self.nickname = data['nickname']
		self._server.kirimroom()
		#self.Send({"action": "responselogin", "status": 1})

	def Network_list(self, data):
		self._server.ListPlayers()
	
	def Network_listlobby(self, data):
		print "list lobby = "
		#print rooms
		print "list room = "
		#print room

	# def Network_joinroom(self):
	# 	self.Send({"action": "user", "username": })

	def Network_createlobby(self, data):
		room[data["room"]]=[data["user"]]
		rooms.append(data["room"])
		self._server.kirimroom()
		self._server.SendToAll({"action": "users", "users": len(room[data["room"]])})
		#print rooms
		print room
		#room.append
	
	def Network_joinlobby(self, data):
		room[data["room"]].append(data["user"])
		#print "orang di room"
		self._server.SendToAll({"action": "users", "users": len(room[data["room"]])})
		print room

	def Network_delroom(self, data):
		room.pop(data["roomname"], None)
		self._server.kirimroom()

	def Network_deluserroom(self, data):
		index_user = (room[data['room']]).index(data["user"])
		(room[data['room']]).pop(index_user)
                #room.pop(data["roomname"], None)
                #self._server.kirimroom()
		self._server.SendToAll({"action": "users", "users": len(room[data["room"]])})

	def Network_playermove(self,data):
		print data['move']
		print data['nickname']
		playertotal = len(room[data['room']])
		if (room[data['room']]).index(data['nickname']) + 1 >= playertotal:
			print room[data['room']][0]
			nextturn = room[data['room']][0]
			self._server.SendToAll({"action": "playermove", "move": data["move"], "room": data['room'], "nickname": nextturn})
		else:
			print room[data['room']][((room[data['room']]).index(data['nickname'])) + 1]
			nextturn = room[data['room']][((room[data['room']]).index(data['nickname'])) + 1]
			self._server.SendToAll({"action": "playermove", "move": data["move"], "room": data['room'], "nickname": nextturn})

	def Network_winner(self,data):
		self._server.SendToAll({"action": "winner", "winflag": 1})

	def Network_play(self,data):
		nextturn = room[data['room']][0]
		self._server.SendToAll({"action": "firstturn", "nickname": nextturn})

class ChatServer(Server):
	channelClass = ClientChannel
	
	def __init__(self, *args, **kwargs):
		Server.__init__(self, *args, **kwargs)
		self.players = WeakKeyDictionary()
		print self.players
		print 'Server launched'
	
	def Connected(self, channel, addr):
		self.AddPlayer(channel)
		#print channel, addr
	
	def ListPlayers(self):
		print "List User : ", [p.nickname for p in self.players]

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

	def kirimroom(self):
		self.SendToAll({"action": "listroom", "rooms": room})

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
