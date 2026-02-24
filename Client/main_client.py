from Client.Model.model_client import Client
from Client.View.view_client import ClientView
from Client.Controller.controller_client import ClientController

HOST = '127.0.0.1'
PORT = 4000

view = ClientView()
client = Client(HOST, PORT)

controller = ClientController(view, client)
controller.start()

view.start()