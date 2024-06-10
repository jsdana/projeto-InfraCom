import time
import socket as skt 

MAX_BUFF = 1024

class UDP:
    def __init__(self, skct_family, skct_type, skct_biding, max_buff=MAX_BUFF):
        self.skct = skt.socket(skct_family, skct_type)
        self.skct.bind(skct_biding)
        self.skct.settimeout(20)
        self.client_address = None
        self.MAX_BUFF = max_buff

    def listen(self):
        while True:
            data, origin = self.skct.recvfrom(self.MAX_BUFF)
            yield data, origin

    def send(self, server_addr: tuple[str, int], msg: bytes):
        self.skct.sendto(msg, server_addr)
        time.sleep(0.0001)
