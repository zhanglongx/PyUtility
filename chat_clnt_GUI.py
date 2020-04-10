#!/usr/bin/env python3
"""Script for Tkinter GUI chat client."""
from ipymessenger.IpmsgServer import IpmsgServer
import tkinter

USER  = 'zhlx-conf-only'
GROUP = 'conf-only'
PORT  = 24250  # listening port
LIST  = ['192.165.53.35', '192.165.54.32']

class pyipmsg_tk():
    def __init__(self):
        self.top = tkinter.Tk()
        self.top.title("Call Conference")
        self.top.wm_attributes("-topmost", 1)

        # get screen width and height
        ws = self.top.winfo_screenwidth()  # width of the screen
        hs = self.top.winfo_screenheight() # height of the screen

        # calculate x and y coordinates for the Tk root window
        x = (ws * 2 / 3)
        y = (hs * 1 / 4)

        self.top.geometry('%dx%d+%d+%d' % (350, 300, x, y))

        self.__start_ipmsg_server()

        messages_frame = tkinter.Frame(self.top)
        self.my_msg = tkinter.StringVar()  # For the messages to be sent.
        self.my_msg.set("")
        scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.
        # Following will contain the messages.
        self.msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
        self.msg_list.pack()
        messages_frame.pack()

        entry_field = tkinter.Entry(self.top, textvariable=self.my_msg)
        entry_field.bind("<Return>", self.on_send)
        entry_field.pack(side=tkinter.LEFT)
        send_button = tkinter.Button(self.top, text="Send", command=self.on_send)
        send_button.pack(side=tkinter.LEFT)

        mail_button = tkinter.Button(self.top, text="Mail", command=self.on_mail)
        mail_button.pack(side=tkinter.RIGHT)

        self.top.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.on_receive()

        tkinter.mainloop()  # Starts GUI execution.

    def __host_ip(self):
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()
        s.close()
        # FIXME: nics
        return ip 

    def __start_ipmsg_server(self):
        self.DEST_IP = [x for x in LIST if x not in self.__host_ip()]
        # self.DEST_IP = ['192.165.53.35']    # tempz

        try:
            self.server = IpmsgServer(USER, GROUP, PORT)
            self.server.start()
        except Exception as e:
            raise e

    def __close_ipmsg_server(self):
        self.server.stop()
        self.server.join()

    def __update_list(self, user, message):
        self.msg_list.insert(tkinter.END, user + ': ')
        self.msg_list.insert(tkinter.END, '    ' + message)

    def on_receive(self):
        """Handles receiving of messages."""
        try:
            for dest_host in self.DEST_IP:
                ipmsg = self.server.get_message(dest_host, remove=True)
                if len(ipmsg):
                    msg = ipmsg[0].get_full_unicode_message().split(':')
                    self.__update_list(msg[2], msg[5])

        except OSError:  # Possibly client has left the chat.
            pass

        self.top.after(100, self.on_receive)

    def on_send(self, event=None):  # event is passed by binders.
        """Handles sending of messages."""
        msg = self.my_msg.get()
        if msg == '':
            msg = 'GGG'
        for ip in self.DEST_IP:
            self.server.send_message(ip, msg)

        self.my_msg.set("")  # Clears input field.

        self.__update_list('my', msg)

    def on_mail(self, event=None):
        pass

    def on_closing(self, event=None):
        """This function is to be called when the window is closed."""
        self.__close_ipmsg_server()

        self.top.quit()

if __name__ == '__main__':
    p = pyipmsg_tk()
    p.on_receive()
