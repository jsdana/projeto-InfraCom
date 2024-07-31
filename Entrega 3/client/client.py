import socket as skt
import threading
import sys

from udp import UDP

MAX_BUFF = 1024

class UDPClient(UDP):
    def __init__(self, skct_family, skct_type, skct_biding, max_buff=MAX_BUFF):
        super().__init__(skct_family, skct_type, skct_biding, max_buff)
        threading.Thread(target=self.receive_messages).start()

    def receive_messages(self):
        while True:
            for data, origin in self.listen():
                if data:
                    self.send_ack(origin)   
                    print(f"{data.decode()}")

    def handle_messages(self, server_addr):
        while True:
            message = input("")
            if message.lower() == 'exit':
                break

            self.send(server_addr, message.encode())

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python clientepy <porta>")
        sys.exit(1)
        
    server_ip = "127.0.0.1" # sys.argv[1]
    
    client = UDPClient(skt.AF_INET, skt.SOCK_DGRAM, ("localhost", int(sys.argv[1])))
    client.handle_messages((server_ip, 8007))