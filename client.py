import sys
import random
from time import sleep
from sys import stdin, exit

from PodSixNet.Connection import connection, ConnectionListener

# This example uses Python threads to manage async input from sys.stdin.
# This is so that I can receive input from the console whilst running the server.
# Don't ever do this - it's slow and ugly. (I'm doing it for simplicity's sake)
from thread import *

class Client(ConnectionListener):
	def __init__(self, host, port):
		self.Connect((host, port))
		nickname = random.randint(1000, 10000)
		connection.Send({"action": "login", "nickname": nickname})
		#connection.Send({"action": "login", "nickname": stdin.readline().rstrip("\n")})
		t = start_new_thread(self.InputLoop, ())
	
	def Loop(self):
		connection.Pump()
		self.Pump()
	
	def InputLoop(self):
		connection.Send({"action": "list"})
		while 1:
			connection.Send({"action": "playermove", "message": stdin.readline().rstrip("\n")})
	
	#######################################
	### Network event/message callbacks ###
	#######################################

	def Network_message(self, data):
		print data['message']

	def Network_playermove(self, data):
		print data['message']

#	def Network_responselogin(self, data):
#		if(data["status"] == 1):
#			print "Selamat Datang, Selamat Bermain"

	def Network_connected(self, data):
		print "Selamat Datang, Selamat Bermain"
	
	def Network_error(self, data):
		print 'error:', data['error'][1]
		connection.Close()
	
	def Network_disconnected(self, data):
		print 'Server disconnected'
		exit()

c = Client("localhost", 55555)
while 1:
	c.Loop()
	#sleep(0.001)
