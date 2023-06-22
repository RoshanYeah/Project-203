import socket
from threading import Thread
from tkinter import *

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IP = '127.0.0.1'
PORT = 8000

client.connect((IP, PORT))

print('Server has started...')

class GUI:
    def __init__(self):
        self.Window = Tk()
        self.Window.withdraw()

        self.login = Toplevel()
        self.login.title("Login")

        self.login.resizable(width=False, height=False)
        self.login.configure(width=400,height=300)

        self.pls = Label(self.login,
                         text = "Please login to continue",
					     justify = CENTER,
					     font = "Helvetica 14 bold")
        self.pls.place( relheight = 0.15,
                        relx = 0.2,
                        rely = 0.07)
        self.nameLabel = Label(self.login,
                               text = "Name: ",
                               font = "Helvetica 12")
        self.nameLabel.place(relheight= 0.2,
                             relx = 0.1,
                             rely = 0.2)
        self.nameEntry = Entry(self.login,
                               font = "Helvetica 14")
        self.nameEntry.place(relwidth=0.4,
                             relheight=0.12,
                             relx=0.35,
                             rely=0.2)
        self.nameEntry.focus()
        self.button = Button(self.login,
                             text="CONTINUE",
                             font="Helvetica 14 bold",
                             command= lambda: self.goAhead(self.nameEntry.get()))
        self.button.place(relx=0.4,rely=0.5)
        self.Window.mainloop()
    def goAhead(self,name):
        self.login.destroy()
        # self.name = name
        self.layout(name)
        rcv = Thread(target=self.receive)
        rcv.start()
    
    def layout(self,name):
        self.name = name
        self.Window.deiconify()
        self.Window.title("CHATROOM")
        self.Window.resizable(width = False,
                              height = False)
        self.Window.configure(width = 470,
                              height = 550,
                              bg = "#FFAEBC")
        self.titleLabel = Label(self.Window,
                                bg="#FFAEBC",
                                fg="#ffffff",
                                text=self.name,
                                font="Helvetica 13 bold",
                                pady=5)
        self.titleLabel.place(relwidth=1)        
        self.line = Label(self.Window,
                          width=450,
                          bg="#FBE7C6")
        self.line.place(relwidth=1,
                        rely=0.07,
                        relheight=0.012)
        self.textArea = Text(self.Window,
                             width=20,
                             height=2,
                             bg="#FFAEBC",
                             fg="#ffffff",
                             font="Helvetica 14",
                             padx=5,
                             pady=5)
        self.textArea.place(relheight=0.745,
                            relwidth=1,
                            rely=0.08)
        self.textBottomLabel = Label(self.Window,
                                     bg="#FBE7C6",
                                     height=80)
        self.textBottomLabel.place(relwidth=1,
                                   rely=0.825)
        self.textInput = Entry(self.textBottomLabel,
                               bg="#A0E7E5",
                               fg="#ffffff",
                               font="Helvetica 13")
        self.textInput.place(relwidth=0.74,
                             relheight=0.06,
                             rely=0.008,
                             relx=0.011)
        self.textInput.focus()
        self.button = Button(self.textBottomLabel,
                             text="Send",
                             font="Helvetica 10 bold",
                             width=20,
                             bg="#B4F8C8",
                             command=lambda:self.sendButton(self.textInput.get()))
        self.button.place(relx=0.77,
                          rely=0.008,
                          relheight=0.06,
                          relwidth=0.22)
        self.textArea.config(cursor="arrow")
        scrollbar = Scrollbar(self.textArea)
        scrollbar.place(relheight=1,
                        relx=0.974)
        scrollbar.config(command=self.textArea.yview)
        self.textArea.config(state=DISABLED)
    
    def sendButton(self,msg):
        self.textArea.config(state=DISABLED)
        self.msg = msg
        self.textInput.delete(0,END)
        sendMsg = Thread(target=self.write)
        sendMsg.start()

    def showMessage(self,message):
        self.textArea.config(state=NORMAL)
        self.textArea.insert(END,message+"\n\n")
        self.textArea.config(state=DISABLED)
        self.textArea.see(END)

    def write(self):
        self.textArea.config(state=DISABLED)
        while True:
            message = (f'{self.name}:{self.msg}')
            client.send(message.encode('utf-8'))
            self.showMessage(message)
            break

    def receive(self):
        while True:
            try:
                message = client.recv(2048).decode('utf-8')
                if message == 'NICKNAME':
                    client.send(self.name.encode('utf-8'))
                else:
                    self.showMessage(message)
            except:
                print("An error occured!")
                client.close()
                break


g = GUI()

# def write(client_socket):
#     while True:
#         message = input()
#         client_socket.send(message.encode('utf-8'))

# receive_thread = Thread(target=receive, args=(client_socket,))
# receive_thread.start()

# write_thread = Thread(target=write, args=(client_socket,))
# write_thread.start()
