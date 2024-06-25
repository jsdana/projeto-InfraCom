import os
import socket as skt
import sys
import time

MAX_BUFF = 1024

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from udp import UDP

class UDPServer(UDP):
    def __init__(self, skct_family, skct_type, skct_biding, max_buff=1024, output_dir='received_files'):
        super().__init__(skct_family, skct_type, skct_biding, max_buff)
        self.output_dir = output_dir
        self.received_file_path = ""
        self.received_packets = set()
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def handle_messages(self):
        print("Servidor está escutando...")

        total_fragments_received = 0
        file_extension = ""
        origin = ''

        while True:
            for data, origin in self.listen():
                if data and data.startswith(b"TYPE_"):
                    file_extension = data[5:].decode()
                    print("Tipo de arquivo recebido:", file_extension)
                    break
            if origin != "":
                break
            print("Nenhum dado recebido")

        
        self.client_address = origin
        self.received_file_path = os.path.join(self.output_dir, f"received_file_{int(time.time())}.{file_extension}")

        with open(self.received_file_path, 'wb') as f:
            while True:
                for data, origin in self.listen():
                    if data and data.startswith(b"END"):
                        print("Fim de loop")
                        break
                    
                    if data:
                        seq_num = int.from_bytes(data[:4], byteorder='big') 
                        if seq_num not in self.received_packets:  
                            print(f"Recebendo fragmento: {seq_num}")                
                            self.send_ack(origin)
                            f.write(data[4:])
                            self.received_packets.add(seq_num)
                            total_fragments_received += 1
                        else:
                            print(f"FRAGMENTO DUPLICADO: {seq_num}")   
                            self.send_ack(origin)
                if data and data.startswith(b"END"):
                    break

        print("Arquivo recebido com sucesso:", self.received_file_path)
        print("Total de fragmentos recebidos:", total_fragments_received)
        self.send_file(self.client_address, self.received_file_path)

    def send_file(self, server_addr: tuple[str, int], file_path: str):
        if not os.path.isfile(file_path):
            print("Arquivo não encontrado!")
            return
        
        file_extension = self.get_file_type(file_path)
        
        print(f"Enviando arquivo {file_path} ({file_extension}) para o cliente.")

        self.send(server_addr, f"TYPE_{file_extension}".encode(), expect_ack=False)

        with open(file_path, 'rb') as f:
            while True:
                fragment = f.read(self.MAX_BUFF-4)
                if not fragment:
                    break
                
                seq_bytes = self.seq_num.to_bytes(4, byteorder='big')  
                print(f"Enviando fragmento: {self.seq_num}")
                self.send(server_addr, seq_bytes + fragment)
                self.seq_num += 1

        self.send(server_addr, b"END", expect_ack=False)
        print("Arquivo enviado")

    def get_file_type(self, file_path: str) -> str:
        _, file_extension = os.path.splitext(file_path)
        return file_extension[1:]

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Exemplo de uso: python3 server.py 127.0.0.1")
        sys.exit(1)

    server_ip = sys.argv[1]
    
    server = UDPServer(skt.AF_INET, skt.SOCK_DGRAM, (server_ip, 8007))
    server.handle_messages()
