import time

class ClientController:
    def __init__(self, view, client):
        self.view = view
        self.client = client

        self.view.btn_send.configure(command=self.on_send_click)
        # self.view.entry.bind("<Return>", self.on_send_click)

        self.running=False

        self.view.root.protocol("WM_DELETE_WINDOW", self.close)

    def start(self):
        try:
            self.client.connect()
        except:
            self.view.add_line("SYSTEM: Server offline")
            self.view.btn_send.config(state="disabled")
            # time.sleep(5)
            # self.start()
            self.view.root.after(5000, self.start)
            return

        self.client.socket.setblocking(False)
        self.running = True
        self.view.add_line("SYSTEM: Server online")
        self.view.btn_send.config(state="normal")
        self.poll_receive()

    def on_send_click(self):
        text = self.view.entry.get()
        if text == "":
            return

        self.view.add_line("Client: " + text)
        self.view.entry.delete(0, "end")

        self.client.send(text)

    def poll_receive(self):
        try:
            msg=self.client.receive()
            if msg == "_offline_":
                self.view.add_line("SYSTEM: Server disconnected")
                self.running = False
                self.view.btn_send.config(state="disabled")
                self.client.disconnect()
                self.view.root.after(1000, self.start)
                return
            if msg:
                self.view.add_line("Server: " + msg)
        except:
            pass

        self.view.root.after(50, self.poll_receive)

    def close(self):
        try:
            if self.client.socket:
                self.client.send("_offline_")
        except:
            pass
        try:
            self.client.disconnect()
        except:
            pass
        self.running = False
        self.view.root.destroy()