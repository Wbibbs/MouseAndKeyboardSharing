import os
from socket import *
import pyautogui as pag
host = ""
port = 13000
buf = 1024
addr = (host, port)
UDPSock = socket(AF_INET, SOCK_DGRAM)
UDPSock.bind(addr)
print("Waiting to receive messages...")
while True:
	(data, addr) = UDPSock.recvfrom(buf)
	#print("Received message")
	#data = data.decode(()
	coords = data.decode()
	print(coords)
	coords = coords.replace("[", "")
	coords = coords.replace("]", "")
	coords = coords.replace(" ", "")
	x, y = coords.split(",")
	#(data, addr) = UDPSock.recvfrom(buf)
	#y = data.decode()
	print("X Coord: " + x)
	print("Y Coord: " + y)
	pag.moveTo(int(x), int(y), .25, pag.easeInOutQuad)
	
UDPSock.close()
os._exit(0)