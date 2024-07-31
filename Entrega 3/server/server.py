import socket as skt
from commands import *
from entities import *
from udp import UDP

MAX_BUFF = 1024

connections = {}
acomodacoes = []

def get_login_by_client_address(client_address):
    for key in list(connections.keys()):
        if connections[key] == client_address:
            return key
    
    return None

class UDPServer(UDP):
    def _init_(self, skct_family, skct_type, skct_biding, max_buff=1024):
        super()._init_(skct_family, skct_type, skct_biding, max_buff)
        self.switch = {
            Commands.LOGIN.value: self.handle_login,
            Commands.LOGOUT.value: self.handle_logout,
            Commands.CREATE.value: self.handle_create,
            Commands.LIST_MY_ACMD.value: self.handle_list_my_acmd,
            Commands.LIST_ACMD.value: self.handle_list_acmd,
            Commands.LIST_MY_RSV.value: self.handle_list_my_rsv,
            Commands.BOOK.value: self.handle_book,
            Commands.CANCEL.value: self.handle_cancel
        }

    def handle_messages(self):
        print("Servidor está escutando...")
        while True:
            for data, origin in self.listen():
                if data:
                    self.send_ack(origin)
                    args = data.decode().split(" ")
                    func = self.switch.get(args[0])
                    if func:
                        func(args, origin)
                    else:
                        ack_message = "Comando invalido."
                        self.send(origin, ack_message.encode())

    def handle_login(self, args, client_address):
        if len(args) == 2:
            if args[1] not in list(connections.keys()):
                connections[args[1]] = client_address
                message = "Você está online!"
            else: message = "Usuário já logado. Hacker c4n4lh4!" 
        else:
            message = "Argumento invalido."

        self.send(client_address, message.encode())

    def handle_logout(self, args, client_address):
        find = False
        for key in list(connections.keys()):
            if connections[key] == client_address:
                del connections[key]
                message = "Você foi deslogado."
                find = True
        
        if not find:
            message = "Você não tem acesso a esse recurso."

        self.send(client_address, message.encode())

    def handle_create(self, args, client_address):
        if len(args) == 3:
            login_dono = get_login_by_client_address(client_address)
            nome_acomodacao = args[1]
            localizacao = args[2]

            if login_dono == None:
                message = "Você não tem acesso a esse recurso."

            else:
                found = False
                for acmd in acomodacoes:
                    if acmd.nome == nome_acomodacao and acmd.localizacao == localizacao:
                        message = "Uma acomodação de mesmo nome e localização já foi registrada."
                        found = True
                    
                if not found:
                    acomodacoes.append(Acomodacao(nome_acomodacao, localizacao, login_dono, client_address))
                    message = f"Acomodação de nome {nome_acomodacao} na localizacao '{localizacao}' criada com sucesso!"

                    for login in list(connections.keys()):
                        if login != login_dono:
                            broadcast_message = f"[{login_dono}/{client_address}:{self.get_skct()}] Criou a acomodação '{args[1]}' na localização '{args[2]}'."
                            self.send(connections[login], broadcast_message.encode())

        else:
            message = "Argumentos invalidos."
        
        self.send(client_address, message.encode())

    def handle_list_my_acmd(self, args, client_address):
        login_dono = get_login_by_client_address(client_address)

        if login_dono == None:
            message = "Você não tem acesso a esse recurso."

        else:
            foundAcmdForClient = False
            for acmd in acomodacoes:
                if acmd.login_dono == login_dono:
                    dias_disponiveis = []
                    dias_indisponiveis = []

                    for reserva in acmd.reservas:
                        if reserva.booker is None:
                            dias_disponiveis.append(reserva.data)
                        else:
                            dias_indisponiveis.append(f"{reserva.data} -> Reservado por '{reserva.booker.nome}/{reserva.booker.ip}:{reserva.booker.socket}'")

                    message = f"""Acomodação: '{acmd.nome}'
Localização: '{acmd.localizacao}'
Dias disponiveis: '{dias_disponiveis}'
Dias indisponiveis: '{dias_indisponiveis}'
                """

                    self.send(client_address, message.encode())
                    foundAcmdForClient = True

            if not foundAcmdForClient:
                self.send(client_address, "Você não possui acomodações registradas.".encode())

    def handle_list_acmd(self, args, client_address):
        login_dono = get_login_by_client_address(client_address)

        if login_dono == None:
            message = "Você não tem acesso a esse recurso."

        else:
            for acmd in acomodacoes:
                dias_disponiveis = []

                for reserva in acmd.reservas:
                    if reserva.booker is None:
                        dias_disponiveis.append(reserva.data)

                message = f"""Id: '{acmd.id}'
Acomodação: '{acmd.nome}'
Localização: '{acmd.localizacao}'
Descrição: '{acmd.descricao}'
Dias disponiveis: '{dias_disponiveis}'
Nome do ofertante: '{acmd.login_dono}'
            """
                self.send(client_address, message.encode())


    def handle_list_my_rsv(self, args, client_address):
        login_cliente = get_login_by_client_address(client_address)

        if login_cliente == None:
            message = "Você não tem acesso a esse recurso."

        else:
            foundReservartionForClient = False
            for acmd in acomodacoes:
                for reserva in acmd.reservas:
                    if reserva.booker is not None:
                        if reserva.booker.nome == login_cliente:
                            message = f"[{acmd.login_dono}/{acmd.ip_dono}:{self.get_skct()}]: Reserva em '{acmd.nome}' localizada em '{acmd.localizacao}' no dia '{reserva.data}'"
                            self.send(client_address, message.encode())
                            foundReservartionForClient = True

            if not foundReservartionForClient:
                message = "Não foi possível achar reservas."
                self.send(client_address, message.encode())

    def handle_book(self, args, client_address):
        if len(args) == 4:
            login_cliente = get_login_by_client_address(client_address)
            if login_cliente == None:
                message = "Você não tem acesso a esse recurso."

            else:
                nome_ofertante = args[1]
                id_oferta = args[2]
                dia_requerido = args[3]

                fail = True
                for acmd in acomodacoes:
                    if acmd.id == int(id_oferta):
                        if acmd.login_dono == nome_ofertante:
                            if acmd.login_dono != login_cliente:
                                reserva = None
                                for rsv in acmd.reservas:
                                    if rsv.data == dia_requerido:
                                        if rsv.booker == None:
                                            reserva = rsv
                                            break
                                if reserva is not None:
                                    reserva.book(Booker(login_cliente, client_address, self.get_skct()))
                                    message = f"[{login_cliente}/{client_address}:{self.get_skct()}]: Reserva em '{acmd.nome}' localizada em '{acmd.localizacao}' no dia '{reserva.data}' realizada com sucesso."
                                    self.send(acmd.ip_dono, message.encode())
                                    message = "Reserva realizada com sucesso."
                                    self.send(client_address, message.encode())
                                    fail = False
                                    break

                if fail:
                    message = "Não foi possível realizar a reserva."
                    self.send(client_address, message.encode())

        else:
            message = "Argumentos invalidos."
            self.send(client_address, message.encode())

    def handle_cancel(self, args, client_address):
        if len(args) == 4:
            login_cliente = get_login_by_client_address(client_address)
            nome_ofertante = args[1]
            id_oferta = args[2]
            dia_requerido = args[3]

            if login_cliente == None:
                message = "Você não tem acesso a esse recurso."

            else:
                fail = True
                for acmd in acomodacoes:
                    if acmd.id == int(id_oferta):
                        if acmd.login_dono == nome_ofertante:
                            for rsv in acmd.reservas:
                                if rsv.data == dia_requerido:
                                    if rsv.unbook(Booker(login_cliente, client_address, self.get_skct())):  
                                        message = f"[{login_cliente}/{client_address}:{self.get_skct()}]: Reserva em '{acmd.nome}' localizada em '{acmd.localizacao}' no dia '{rsv.data}' foi cancelada."
                                        self.send(acmd.ip_dono, message.encode())
                                        message = "Reserva cancelada com sucesso."
                                        self.send(client_address, message.encode())
                                        fail = False

                                        for login in list(connections.keys()):
                                            if login != acmd.login_dono:
                                                broadcast_message = f"[{acmd.login_dono}/{acmd.ip_dono}:{self.get_skct()}] Novas disponibilidades para a acomodação '{acmd.nome}' localizada em '{acmd.localizacao}' com id '{acmd.id}'."
                                                self.send(connections[login], broadcast_message.encode())
                                        break

                if fail:
                    message = "Não foi possível realizar o cancelamento da reserva."
                    self.send(client_address, message.encode())

        else:
            message = "Argumentos invalidos."
            self.send(client_address, message.encode())

if _name_ == "_main_":

    server_ip = "127.0.0.1" 
    
    server = UDPServer(skt.AF_INET, skt.SOCK_DGRAM, (server_ip, 8007))
    server.handle_messages()
