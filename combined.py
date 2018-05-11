import os
import time
from socket import *
from tkinter import *
import netifaces as ni
from queue import Queue
import pyautogui as pag
from Xlib import display
from multiprocessing import Process

network = "enp0s3" #Specifies the network/hardware to use for communicating
queue = Queue()
processes = []
sendDelay = .25 #The amount of time in seconds to delay messages sent
host = "10.255.255.0" # 255.255.0 is usual IP here - set to IP address of target computer
host2 = "10.255.255.1" #IP of the second computer to communicate with
port = 13000
addr = (host, port) #Creates an address which combines IP and port
addr2 = (host2, port)
UDPSock = socket(AF_INET, SOCK_DGRAM)
ni.ifaddresses(network)
thisIP = ni.ifaddresses(network)[ni.AF_INET][0]['addr']
x, y = 0, 0
addresses = [addr, addr2]
root = Tk()

def ping (addr):
    UDPSock.sendto("ping", addr)
    UDPSock.sendto("ping", addr2)

def gui():
    def cnct():
        cnct = Label(btmFrame, text = "Connected")
        #cnct.grid(row = 11, column = 2)
        cnct.pack()
        hostIP = str(host) + " & " + str(host2)
        ip.config(text = "Connected to: " + str(hostIP))
        root.update()
        p = Process(target=sendPosition, args=())
        processes.append(p)
        p.start()

    def dcnct():
        hostIP = "nothing"
        ip.config(text = "Connected to: " + str(hostIP))
        root.update()
        dcnct = Label(btmFrame, text = "Disconnected")
        #dcnct.grid(row = 12, column = 2)
        dcnct.pack()
        for process in processes:
            print("Terminating processes")
            process.terminate()

    hostIP = "nothing"
    
    screen_width = root.winfo_screenwidth() #Gets width of screen
    screen_height = root.winfo_screenheight() #Gets height of screen
    frame = Frame(root)
    frame.pack(side=TOP) #Creates a top frame for widgets
    btmFrame = Frame(root)
    btmFrame.pack(side = BOTTOM) #Creates a bottom frame for widgets
    ip = Label(frame, text = "Connected to: " + hostIP)
    ip.grid(row = 1, column = 2); #Creates and places ip label

    cnctBtn = Button(frame, text = "CONNECT", bg ="green", fg = "black", command = cnct) #Creates connect button
    dcBtn = Button(frame, text = "DISCONNECT", bg = "red", fg = "black", command = dcnct) #Created disconnect button
    cnctBtn.grid(row = 6, column = 2) #Places connect button
    #space = Label(frame, text="    ")
    #space.grid(row = 6, column =3 ) #Creates and places a space between the buttons
    dcBtn.grid(row = 6, column = 3) #Places disconnect button

    log = Label(frame, text = "Activity log:")
    log.grid(row = 10, column = 2) #Creates and places Activity log Label
    actionLbl = Label(btmFrame, text = "Mouse position: " + str(x) + ", " + str(y))
    actionLbl.pack()
    root.title("MoIP")
    root.geometry('640x480')
    root.update()
    root.mainloop()
    
def sendPosition():
    while True: #Sends mouse position constantly
        time.sleep(sendDelay) #Delay on sending messages
        x, y = pag.position()
        coords = [x, y]
        for address in addresses:
            UDPSock.sendto(str(coords).encode(), address)
            print("Sent x value of " + str(coords) + " to " + str(address))

def startProcesses():
    for process in processes:
        process.start()

p = Process(target=gui, args=())
p.start()
#processs.append(t)
#t2 = process(target=sendPosition, args=())
#processs.append(t2)

startProcesses()

#UDPSock.close()
#os._exit(0)
