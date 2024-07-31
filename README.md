# Projeto da Disciplina Infraestrutura de Comunicações - 2024.1

## Visão Geral
Este projeto é dividido em três partes e faz parte da disciplina Infraestrutura de Comunicações, 2024.1. O objetivo é desenvolver um sistema de comunicação cliente-servidor utilizando UDP, implementar um protocolo básico de transferência confiável e, finalmente, criar um sistema de reserva de acomodações.

## Estrutura do Projeto

1. **Primeira Etapa: Transmissão de Arquivos com UDP**
    - Implementação de comunicação UDP usando a biblioteca `socket` em Python.
    - Envio e devolução de arquivos (pelo menos dois tipos diferentes, como `.txt` e imagem) em pacotes de até 1024 bytes.
    - Alteração do nome do arquivo antes da devolução ao cliente.
    - Requisitos: modularização em arquivos `.py` separados para cliente e servidor.

2. **Segunda Etapa: Implementando uma Transferência Confiável com RDT 3.0**
    - Implementação de transferência confiável usando o RDT3.0 conforme o livro "Redes de Computadores e a Internet" de Kurose.
    - Printar na linha de comando os passos executados do algoritmo.
    - Implementar um gerador de perdas de pacotes aleatórios para teste.

3. **Terceira Etapa: Sistema de Reserva de Acomodações**
    - Desenvolvimento de um sistema de reserva de acomodações exibido por linha de comando.
    - Suporte para múltiplos clientes simultâneos.
    - Manter o uso do RDT3.0.

## Instruções de Execução

#### Primeira Etapa

1. Execute o servidor UDP:
    ```bash
    python3 server.py 127.0.0.1
    ```
2. Execute o cliente UDP:
    ```bash
    python3 client.py 127.0.0.1 "../arquivo.mp3"
    ```
3. O cliente deve enviar um arquivo ao servidor, que será armazenado e devolvido ao cliente com um nome alterado. Será criada uma pasta "received_files" no diretório do cliente e do servidor. Essas pastas terão os arquivos recebidos por cada um deles, nomeados com o timestamp do momento em que foram recebidos.


#### Segunda Etapa

1. Execute o servidor UDP:
    ```bash
    python3 server.py 127.0.0.1
    ```
2. Execute o cliente UDP:
    ```bash
    python3 client.py 127.0.0.1 "../arquivo.mp3"
    ```
3. O cliente deve enviar um arquivo ao servidor, que será armazenado e devolvido ao cliente com um nome alterado. Será criada uma pasta "received_files" no diretório do cliente e do servidor. Essas pastas terão os arquivos recebidos por cada um deles, nomeados com o timestamp do momento em que foram recebidos.
4. Verifique a transmissão confiável com pacotes perdidos simulados.

#### Terceira Etapa
1. Para cada cliente, execute:
    ```bash
    python client.py <porta>
    ```
3. Para o servidor, execute:
    ```bash
    python server.py
    ```
4. Use os comandos listados abaixo para interagir com o sistema.

### Comandos Disponíveis

- **Conectar ao Sistema**
  ```bash
  login <nome_do_usuario>
  ```
- **Sair do Sistema**
  ```bash
  logout
  ```
- **Exibir Minhas Acomodações**
  ```bash
  list:myacmd
  ```
- **Exibir Acomodações Disponíveis**
  ```bash
  list:acmd
  ```
- **Exibir Minhas Reservas**
  ```bash
  list:myrsv
  ```
- **Criar Acomodação**
  ```bash
  create <nome_da_acomodação> <localização> <id>
  ```
- **Reservar Oferta**
  ```bash
  book <nome_ofertante> <id_oferta> <dia>
  ```
- **Cancelar Reserva**
  ```bash
  cancel <nome_reserva> <id> <dia>
  ```

## Estrutura de Arquivos

- `udp.py`: Implementação da classe UDP para comunicação.
- `server.py`: Implementação do servidor utilizando UDP.
- `client.py`: Implementação do cliente utilizando UDP.
- `commands.py`: Definição de comandos do sistema.
- `entities.py`: Definição das entidades do sistema (acomodações, reservas, etc.).

## Conclusão
Este projeto oferece uma experiência prática na implementação de protocolos de comunicação, enfatizando a confiabilidade e a aplicação de sistemas distribuídos. Siga as instruções cuidadosamente e respeite os prazos de entrega para obter a melhor nota possível.

---

## Nome dos Integrantes
- Ianne Vitoria Cruz Fernandes (ivcf)
- Juliana Silva (js3)
- Rafaela Albert de Carvalho (rac4)
- Lucas Morais de Araújo (lma6)
- Camila Barbosa Vieira (cbv2)
- José Vinicius de Santana Souza (jvss2)