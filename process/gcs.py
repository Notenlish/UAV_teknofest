from typing import TYPE_CHECKING

from server.async_server import TCPServer

if TYPE_CHECKING:
    from app import App

# this code is the most unorganized mess I've ever written
# I hate this. So much. Please help.


class GCSComm:
    def __init__(self, app: "App", config, memory) -> None:
        self.app = app
        self.config = config
        self.memory = memory
        
        print("ĞĞĞĞ GCS COMM")
    
    def start(self):
        self.server = TCPServer(self)
        self.server.run()
    
    

