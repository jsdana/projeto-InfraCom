import socket as skt 
import random
import time

MAX_BUFF = 1024
PACKET_LOSS_PROBABILITY = 0.01

class UDP:
    def __init__(self, skct_family, skct_type, skct_biding, max_buff=MAX_BUFF):
        self.skct = skt.socket(skct_family, skct_type)
        self.skct.bind(skct_biding)
        self.skct.settimeout(2)
        self.client_address = None
        self.MAX_BUFF = max_buff
        self.seq_num = 0

    def listen(self):
        while True:
            try:
                data, origin = self.skct.recvfrom(self.MAX_BUFF)
                yield data, origin
            except skt.timeout:
                return None, None

    def send(self, server_addr: tuple[str, int], msg: bytes, expect_ack=True):
        while True:
            if random.random() < PACKET_LOSS_PROBABILITY:
               print(f"Simulando perda de pacote do endereço {server_addr}")
            else:
                print(f"Enviando pacote para {server_addr}")
                self.skct.sendto(msg, server_addr)
                if not expect_ack:
                    break

            try:
                if random.random() < PACKET_LOSS_PROBABILITY:
                    print(f"Simulando timeout prematuro {server_addr}")
                    continue
                else:
                    ack, _ = self.skct.recvfrom(self.MAX_BUFF)
                    if ack == b"ACK":
                        print("ACK recebido")
                        break
            except skt.timeout:
                print("Timeout. Reenviando pacote...")
                continue

    def send_ack(self, addr):
        if random.random() < PACKET_LOSS_PROBABILITY:
            print(f"Simulando perda de ACK para {addr}")
        else:
            print(f"Enviando ACK para {addr}")
            self.skct.sendto(b"ACK", addr)