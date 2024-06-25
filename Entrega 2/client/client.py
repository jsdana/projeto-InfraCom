import os
import socket as skt
import sys
import time

MAX_BUFF = 1024

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from udp import UDP

class UDPClient(UDP):
    def __init__(self, skct_family, skct_type, skct_biding, max_buff=MAX_BUFF, output_dir='received_files'):
        super().__init__(skct_family, skct_type, skct_biding, max_buff)
        self.output_dir = output_dir
        self.received_packets = set()
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    #Enviar o arquivo
    def send_file(self, server_addr: tuple[str, int], file_path: str):
        if not os.path.isfile(file_path):
            print("Arquivo não encontrado!")
            return
        
        # Identificar o tipo de arquivo com base na extensão
        file_extension = self.get_file_type(file_path)
        
        print(f"Enviando arquivo {file_path} ({file_extension}) para o servidor.")

        # Enviar o tipo de arquivo para o servidor
        self.send(server_addr, f"TYPE_{file_extension}".encode(), expect_ack=False)

        # Enviar o arquivo fragmentado para o servidor
        with open(file_path, 'rb') as f:
            while True:
                fragment = f.read(self.MAX_BUFF-4)
                if not fragment:
                    break

                seq_bytes = self.seq_num.to_bytes(4, byteorder='big')  
                print(f"Enviando fragmento: {self.seq_num}")
                self.send(server_addr, seq_bytes + fragment)
                self.seq_num += 1

        # Fim do envio
        self.send(server_addr, b"END", expect_ack=False)
        print("Fim do envio")
        client.handle_messages()

    #Receber o arquivo
    def handle_messages(self):
        print("Cliente está escutando...")

        total_fragments_received = 0
        file_extension = ""

        # Recebe o tipo do arquivo enviado pelo cliente
        for data, origin in self.listen():
            if data.startswith(b"TYPE_"):
                file_extension = data[5:].decode()
                print("Tipo de arquivo recebido:", file_extension)
                break

        # Definir o caminho do arquivo recebido dentro da função handle_messages
        self.received_file_path = os.path.join(self.output_dir, f"received_file_{int(time.time())}.{file_extension}")

        # Receber e armazenar o arquivo fragmentado enviado pelo cliente
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

    # Obter a extensão do arquivo pelo path dele
    def get_file_type(self, file_path: str) -> str:
        _, file_extension = os.path.splitext(file_path)
        return file_extension[1:]  # Remover o ponto da extensão

# Exemplo de uso:
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python clientepy 127.0.0.1 <arquivopng>")
        sys.exit(1)
        
    server_ip = sys.argv[1]
    file_path = sys.argv[2]
    
    client = UDPClient(skt.AF_INET, skt.SOCK_DGRAM, ("localhost", 8005))
    client.send_file((server_ip, 8007), file_path)
