import tkinter as tk

class ClientView:
    def __init__(self, title="Client"):
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry("700x700")

        self.history = tk.Text(self.root, wrap="word", state="disabled")
        self.history.pack(fill="both", expand=True, padx=10, pady=10)

        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(fill="x", padx=10, pady=(0, 10))

        self.entry = tk.Entry(bottom_frame)
        self.entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.btn_send = tk.Button(bottom_frame, text="Відправити")
        self.btn_send.pack(side="right")

        self.history.tag_config("client", foreground="blue")
        self.history.tag_config("server", foreground="green")
        self.history.tag_config("system", foreground="gray")

    def add_line(self, text):
        self.history.configure(state="normal")

        tag=None
        if text.startswith("Client: "):
            tag="client"
        elif text.startswith("Server: "):
            tag="server"
        elif text.startswith("SYSTEM: "):
            tag="system"

        if tag:
            self.history.insert("end", text + "\n", tag)
        else:
            self.history.insert("end", text + "\n")

        self.history.configure(state="disabled")
        self.history.see("end")

    def start(self):
        self.root.mainloop()