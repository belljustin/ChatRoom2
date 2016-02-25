from Tkinter import *

import message

class Chatbox(Frame):

    def __init__(self, parent, sock):
        Frame.__init__(self, parent)

        self.sock = sock
        self.username = "Anonymous"
        self.parent = parent
        self.initUI()

    def initUI(self):

        self.parent.title("Buttons")

        frame = Frame(self, relief=RAISED, borderwidth=1)
        frame.pack(fill=BOTH, expand=True)

        self.message_box = Message(frame)
        self.message_box.pack()

        self.text_box = Text(self.message_box)
        self.text_box.pack()

        self.pack(fill=BOTH, expand=True)

        self.okButton = Button(self, text="Send", command=self.sendmsg)
        self.okButton.pack(side=LEFT)

        self.entry = Entry(self)
        self.entry.pack(side=LEFT)

    def sendmsg(self):
        msg = self.entry.get()
        message.send_msg(self.sock, self.username, msg)

    def write(self, username, msg):
        self.text_box.insert(END, username + ": " + msg + "\n")
