#!/usr/bin/env python3
"""Script for Tkinter GUI chat client."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
import tkinter.messagebox as messagebox
import sys

user= False

def receive():
    """Handles receiving of messages."""
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            msg_list.insert(tkinter.END, msg)
        except OSError:  # Possibly client has left the chat.
            break


def send(event=None):  # event is passed by binders.
    """Handles sending of messages."""
    
    msg = my_msg.get()
    my_msg.set("")  # Clears input field.
    client_socket.send(bytes(msg, "utf8"))
    send_button['text'] = "Envoyer le message"
    if msg == "/quit":
        client_socket.close()
        top.destroy()
        sys.exit()
        sys.exit()
        print('ERROR: Impossible de fermer l\'application. Merci d\'uttiliser kill ou ^C')

def on_closing(event=None):
    """This function is to be called when the window is closed."""
    my_msg.set("/quit")
    send()

def get_port():
    connection_window = tkinter.Tk()
    connection_window.title('Connection au serveur')
    
    Label1 = tkinter.Label(connection_window, text='Adresse:')
    Label1.pack(side=tkinter.LEFT, padx=5, pady=5)
    
    host = tkinter.StringVar()
    port = tkinter.StringVar()
    user = tkinter.StringVar()
    host.set('localhost')
    port.set('31000')
    
    adr_input = tkinter.Entry(connection_window, textvariable=host)
    adr_input.pack(side = tkinter.LEFT, padx = 5, pady = 5)

    Label2 = tkinter.Label(connection_window, text="Port:")
    Label2.pack(side=tkinter.LEFT, padx=5, pady=5)

    port_input = tkinter.Entry(connection_window, textvariable=port)
    port_input.pack(side=tkinter.LEFT, padx=5, pady=5)

    Label3 = tkinter.Label(connection_window, text="| Pseudo: ")
    Label3.pack(side=tkinter.LEFT, padx=5, pady=5)

    user_input = tkinter.Entry(connection_window, textvariable=user)
    user_input.pack(side=tkinter.LEFT, padx=5, pady=5)
    
    Bouton = tkinter.Button(connection_window, text='Valider', command=connection_window.destroy)
    Bouton.pack(side=tkinter.LEFT, padx=5, pady=5)

    connection_window.mainloop()
    return [port.get(), host.get(), user.get()]

connection = get_port()

top = tkinter.Tk()
top.title("ZoChat")
top.tk.call('wm', 'iconphoto', top._w, tkinter.PhotoImage(file='./images/Zochatfavicon.png'))
zochat_icon = tkinter.PhotoImage('./images/ZOCHAT.png')
image = tkinter.Canvas(top, width="1000", height="300")
image.create_text(300, 200, text="ZOCHAT", fill="red", font=("ubuntu", 50))
image.create_text(600, 200, text="By Zonovum", fill="red", font=("ubuntu", 20))
image.pack()

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()  # For the messages to be sent.
my_msg.set(connection[-1])
scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.
# Following will contain the messages.
msg_list = tkinter.Listbox(messages_frame, height=20, width=200, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_msg, width="200")
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="Envoyer mon pseudo", command=send)
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)

#----Now comes the sockets part----
HOST = connection[1]
PORT = connection[0]
print(connection)
if not PORT:
    PORT = 33000
else:
    PORT = int(PORT)

BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()
top.mainloop()  # Starts GUI execution.
