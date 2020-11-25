import socket
import time
import re
import sys 
from datetime import datetime
from tkinter import *
import tkinter.scrolledtext as tkst
import threading


class Application():
    def __init__(self,master):
        print("3333")
        
    def send():
        nickname = 'kai11xe14'
        token = 'oauth:c1qmr7kavg5l2exrnyj1z740belyyv'
        channel = '#' + channelID
        s.send(f"PASS {token}\r\n".encode("utf-8"))
        s.send(f"NICK {nickname}\r\n".encode("utf-8"))
        s.send(f"JOIN {channel}\r\n".encode("utf-8"))

        
def read_twichChatRoom(ChannelID):

     
     
    connected = False
    run = True
     
     
    while run:
        response = s.recv(2048).decode("utf-8")
        if response.startswith('PING'):     #確認是否還在連線中
            s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
           # print('Pong')
        else:
            username = re.search(r"\w+", response, re.U).group(0)
            CHAT_MSG = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :") #把這行regular expression做成一個pattern,可重複使用
            
            message = CHAT_MSG.sub("", response).rstrip('\n')
     
            if 'End of /NAMES list' in message:
                connected = True
                print('Listening to ', channel)
     
     
            if connected == True:  
                if 'End of /NAMES list' in message:
                    pass
                else:      
                    print(datetime.now().strftime("%Y-%b-%d %H:%M:%S > ") + username.title() + ':', message)
     
     
            #so we don't send messages too fast
            time.sleep(1 / 10)


    
window = Tk()

#frame0 , for Entry and Button
frame0 = Frame(
    master = window
)
frame0.pack(fill=BOTH)

#frame1 , for ScrolledText
frame1 = Frame(
    master = window
)
frame1.pack(side=BOTTOM, expand='yes')

#create an Entry
global channelID
channelID = ''
str_v = StringVar(window,value='default text')
textfield = Entry(frame0,textvariable=str_v,bd=1, bg='white',fg='black')
def on_change(event):
    channelID = event.widget.get()
    print(channelID)

    
textfield.bind("<Return>",on_change)
textfield.pack(padx=10, pady=10, side=LEFT)

#create a Button
btn=Button(frame0, text="Enter", fg='blue')
def callback(event):
    channelID = textfield.get()
    print(channelID)

    
btn.bind("<ButtonPress>",callback)
btn.pack(padx=5, pady=10, side=LEFT)

#create a ScrolledText
scrltext = tkst.ScrolledText(
    master = frame1,
    wrap = WORD,
    width = 60,
    height = 40
)
scrltext.pack(padx=10,pady=10,side=BOTTOM,expand=True)
scrltext.insert(INSERT,
"""\
Integer posuere erat a ante venenatis dapibus.
Posuere velit aliquet.
Aenean eu leo quam. Pellentesque ornare sem.
Lacinia quam venenatis vestibulum.
Nulla vitae elit libero, a pharetra augue.
Cum sociis natoque penatibus et magnis dis.
Parturient montes, nascetur ridiculus mus.
""")
scrltext.see(END)

#create a socket and connect to twitch
server = 'irc.chat.twitch.tv'
port = 6667



global s
s = socket.socket()
s.connect((server, port))



window.title('Hello Python')
window.mainloop()



##server = 'irc.chat.twitch.tv'
##port = 6667
##nickname = 'kai11xe14'
##token = 'oauth:c1qmr7kavg5l2exrnyj1z740belyyv'
##channel = '#serjunplaygame' 
##
## 
## 
##s = socket.socket()
##s.connect((server, port))
##s.send(f"PASS {token}\r\n".encode("utf-8"))
##s.send(f"NICK {nickname}\r\n".encode("utf-8"))
##s.send(f"JOIN {channel}\r\n".encode("utf-8"))
## 
## 
##connected = False
##run = True
## 
## 
##while run:
##    response = s.recv(2048).decode("utf-8")
##    if response.startswith('PING'):     #確認是否還在連線中
##        s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
##       # print('Pong')
##    else:
##        username = re.search(r"\w+", response, re.U).group(0)
##        CHAT_MSG = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :") #把這行regular expression做成一個pattern,可重複使用
##        
##        message = CHAT_MSG.sub("", response).rstrip('\n')
## 
##        if 'End of /NAMES list' in message:
##            connected = True
##            print('Listening to ', channel)
## 
## 
##        if connected == True:  
##            if 'End of /NAMES list' in message:
##                pass
##            else:      
##                print(datetime.now().strftime("%Y-%b-%d %H:%M:%S > ") + username.title() + ':', message)
## 
## 
##        #so we don't send messages too fast
##        time.sleep(1 / 10)
