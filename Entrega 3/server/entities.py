import random

class Acomodacao:
    def __init__(self, nome, localizacao, login_dono, ip_dono):
        self.id = random.randint(0, 10000)
        self.nome = nome
        self.localizacao = localizacao
        self.descricao = ""
        self.login_dono = login_dono
        self.ip_dono = ip_dono
        self.reservas = [Reserva("17/07/2024"), Reserva("18/07/2024"), Reserva("19/07/2024"), Reserva("20/07/2024"), Reserva("21/07/2024"), Reserva("22/07/2024")]

class Booker:
    def __init__(self, nome, ip, socket):
        self.nome = nome
        self.ip = ip
        self.socket = socket

class Reserva:
    def __init__(self, data):
        self.data = data
        self.booker = None

    def book(self, booker: Booker):
        self.booker = booker
    
    def unbook(self, booker: Booker):
        if booker.nome == self.booker.nome and booker.ip == self.booker.ip:
            self.booker = None
            return True
        
        return False