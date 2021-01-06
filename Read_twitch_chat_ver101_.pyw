import socket
import time
import re
import sys 
from datetime import datetime
from tkinter import *
import tkinter.scrolledtext as tkst
import threading


class Application(Frame):
    def __init__(self,master):
        Frame.__init__(self,master)
##        self.pack(side=BOTTOM, expand=True)
        self.pack(side=BOTTOM,fill=BOTH,expand=True)
        self.createScrollText()

        
    def createScrollText(self):
        self.scrltext = tkst.ScrolledText(
            master = self,
            wrap = WORD,
            width = 60,
            height = 40
        )
        self.scrltext.pack(padx=10,pady=10,fill=BOTH,side=BOTTOM,expand=True)
        self.scrltext.tag_config('listening',foreground='red')
        self.scrltext.tag_config('talking',foreground='black')
        self.scrltext.see(END)

        

        
    def send(self,chID):
        global first
        global s
        server = 'irc.chat.twitch.tv'
        port = 6667
        nickname = 'kai11xe14'
        token = 'oauth:c1qmr7kavg5l2exrnyj1z740belyyv'
        if first == True:
            first = False
        else:
            #if not first time to send, close socket and reconnect to twitch.
            s.close()
            s = socket.socket()
            connected = False
            while not connected:
                try:
                    s.connect((server, port))
                    connected = True
                    print("Connection successful.")
                    self.scrltext.insert(END,'Connection successful.\n','connecting')
                except:
                    print("Reconnecting...")
                    self.scrltext.insert(END,'Reconnecting...\n','connecting')
                    time.sleep(5)
                    

            
        self.nickname = 'kai11xe14'
        self.token = 'oauth:c1qmr7kavg5l2exrnyj1z740belyyv'
        self.channel = '#' + chID
        s.send(f"PASS {self.token}\r\n".encode("utf-8"))
        s.send(f"NICK {self.nickname}\r\n".encode("utf-8"))
        s.send(f"JOIN {self.channel}\r\n".encode("utf-8"))
        print('creating a new thread...\n')
        self.t=threading.Thread(target = self.getInfo,args=(chID,))
        self.t.start()

        #print('Here are',threading.active_count(),"threads.\n")



    def getInfo(self,chID):
        print('Here are',threading.active_count(),"threads.\n")
        
        print('Hello '+chID+'\n')
        
        connected = False
        while True:
            try:
                response = s.recv(2048).decode("utf-8")
            except:
                #When socket closed, this thread is ready to die.
                print("socket closed, I'm ready to die.\n")
                break
            print(response)
            if response.startswith('PING'):     #確認是否還在連線中
                s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
                print('Pong\n')
            else:
                try:
                    username = re.search(r"\w+", response, re.U).group(0)
                except:
                    break
                print(username)
                CHAT_MSG = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :") #把這行regular expression做成一個pattern,可重複使用
                
                message = CHAT_MSG.sub("", response).rstrip('\n')
         
                if 'End of /NAMES list' in message:
                    connected = True
                    print('Listening to ', self.channel)
                    self.scrltext.insert(END,'=======Listening to ' + self.channel + '=======\n','listening')

                    self.scrltext.see(END)
         
         
                if connected == True:  
                    if 'End of /NAMES list' in message:
                        pass
                    else:      
                        print(datetime.now().strftime("%Y-%b-%d %H:%M:%S > ") + username.title() + ':', message)
                        self.scrltext.insert(END,datetime.now().strftime("%Y-%b-%d %H:%M:%S > ") + username.title() + ':' + message + "\n",'talking')

                        self.scrltext.see(END)
                #so we don't send messages too fast
                time.sleep(1 / 10)
        print("a thread is dead.\n")
        print("###################")
        self.send(chID)

        
        



global first #check if the first time to connect
first = True
##global thread_isDead
##thread_isDead = True

window = Tk()
#create a socket and connect to twitch
server = 'irc.chat.twitch.tv'
port = 6667
nickname = 'kai11xe14'
token = 'oauth:c1qmr7kavg5l2exrnyj1z740belyyv'
#channel = '#serjunplaygame' 


global s
s = socket.socket()
s.connect((server, port))
##s.send(f"PASS {token}\r\n".encode("utf-8"))
##s.send(f"NICK {nickname}\r\n".encode("utf-8"))
##s.send(f"JOIN {channel}\r\n".encode("utf-8"))

app = Application(master=window)

#frame0 , for Entry and Button
frame0 = Frame(
    master = window
)
frame0.pack(side=TOP,fill=BOTH)

#frame1 , for ScrolledText
##frame1 = Frame(
##    master = window
##)
##frame1.pack(side=BOTTOM, expand='yes')

#create an Entry
str_v = StringVar(window,value='default text')
textfield = Entry(frame0,textvariable=str_v,bd=1, bg='white',fg='black')
def on_change(event):
    channelID = event.widget.get()
    print(channelID)
    app.send(chID=channelID)
    
textfield.bind("<Return>",on_change)
textfield.pack(padx=10, pady=10, side=LEFT)

#create a Button
btn=Button(frame0, text="Enter", fg='blue')
def callback(event):
    channelID = textfield.get()
    print(channelID)
    app.send(chID=channelID)


    
btn.bind("<ButtonPress>",callback)
btn.pack(padx=5, pady=10, side=LEFT)

#create a ScrolledText
##scrltext = tkst.ScrolledText(
##    master = frame1,
##    wrap = WORD,
##    width = 60,
##    height = 40
##)
##scrltext.pack(padx=10,pady=10,side=BOTTOM,expand=True)
##scrltext.insert(INSERT,
##"""\
##Integer posuere erat a ante venenatis dapibus.
##Posuere velit aliquet.
##Aenean eu leo quam. Pellentesque ornare sem.
##Lacinia quam venenatis vestibulum.
##Nulla vitae elit libero, a pharetra augue.
##Cum sociis natoque penatibus et magnis dis.
##Parturient montes, nascetur ridiculus mus.
##""")
##scrltext.see(END)


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
