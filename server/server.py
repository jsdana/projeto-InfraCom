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
        self.received_file_path = ""  # Inicializa o caminho do arquivo recebido como vazio
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    #Receber o arquivo
    def handle_messages(self):
        print("Servidor está escutando...")

        total_fragments_received = 0
        file_extension = ""

        # Receber o tipo do arquivo enviado pelo cliente retirando da mensagem TYPE recebida antes do arquivo
        for data, origin in self.listen():
            if data.startswith(b"TYPE_"):
                file_extension = data[5:].decode()
                print("Tipo de arquivo recebido:", file_extension)
                break

        # Atualizar o endereço do cliente
        self.client_address = origin

        # Definir o caminho do arquivo recebido usando um timestamp
        self.received_file_path = os.path.join(self.output_dir, f"received_file_{int(time.time())}.{file_extension}")

        # Receber e armazenar o arquivo fragmentado enviado pelo cliente
        with open(self.received_file_path, 'wb') as f:
            for data, origin in self.listen():
                if data.startswith(b"END"):
                    print("Fim de loop")
                    break
                
                f.write(data)
                total_fragments_received += 1

        print("Arquivo recebido com sucesso:", self.received_file_path)
        print("Total de fragmentos recebidos:", total_fragments_received)
        self.send_file(self.client_address, self.received_file_path)


    #Enviar o arquivo
    def send_file(self, server_addr: tuple[str, int], file_path: str):
        if not os.path.isfile(file_path):
            print("Arquivo não encontrado!")
            return
        
        # Identificar o tipo de arquivo com base na extensão
        file_extension = self.get_file_type(file_path)
        
        print(f"Enviando arquivo {file_path} ({file_extension}) para o Cliente.")

        # Enviar o tipo de arquivo para o cliente
        self.send(server_addr, f"TYPE_{file_extension}".encode())

        # Enviar o arquivo fragmentado para o cliente
        with open(file_path, 'rb') as f:
            while True:
                fragment = f.read(self.MAX_BUFF)
                if not fragment:
                    break #Sai do loop quando não há mais dados a serem lidos

                self.send(server_addr, fragment)

        # Fim do envio
        self.send(server_addr, b"END")
        print("Arquivo enviado")

    # Obter a extensão do arquivo pelo path dele
    def get_file_type(self, file_path: str) -> str:
        _, file_extension = os.path.splitext(file_path)
        return file_extension[1:]  # Remover o ponto da extensão


# Exemplo de uso:
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Exemplo de uso: python3 server.py 127.0.0.1")
        sys.exit(1)

    server_ip = sys.argv[1]
    
    server = UDPServer(skt.AF_INET, skt.SOCK_DGRAM, (server_ip, 8007))
    server.handle_messages()
