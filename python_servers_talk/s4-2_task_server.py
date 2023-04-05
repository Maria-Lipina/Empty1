#!/bin/python3

import socket
import threading
# Работать в многопоточном режиме - это запускать одновременно более одного бесконечного цикла

# Connection Data
# На семинаре 109.107.176.64 и порт 55555 
host = '192.168.0.151'
port = 888

# Starting Server. Пространство IpV4, протокол TCP - это значения по умолчанию
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port)) 
""" элемент массива из кортежей, сказали на семинаре - это что, в теории можно связать несколько IP и несколько портов? С портами так действительно возможно, судя по линуксу """
server.listen()

# Lists For Clients and Their Nicknames
# под клиентом имеется в виду сокет, который получется в результате TCP-хендшейка и установления TCP-сессии с клиентом
clients = [] 
nicknames = [] #ники, которые присылают после подключения "с той стороны"


# Sending Messages To All Connected Clients
def broadcast(message):
    for client in clients:
        client.send(message)

# Handling Messages From Clients
def handle(client):
    while True:
        try:
            # Broadcasting Messages

            message = client.recv(1024)
            
            if message == 'EXIT':
                broadcast('{} left!'.format(nickname).encode('ascii'))
                print('{} left!'.format(nickname).encode('ascii'))
                clients.remove(client)
                nicknames.remove(nickname)
                if len(clients) == 0:
                    break
            
            broadcast(message)
            print(message)
        except:
            # Removing And Closing Clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} left!'.format(nickname).encode('ascii'))
            nicknames.remove(nickname)
            break


# Receiving / Listening Function
def receive():
    while True:
        # Accept Connection. Если подключается клиент по TCP, шлет SYN пакет, то я его принимаю и посылаю в ответ сокет с адресом
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # Request And Store Nickname
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        # Print And Broadcast Nickname
        print("Nickname is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode('ascii')) #см. функцию, описанную выше
        client.send('Connected to server!'.encode('ascii'))

        # Start Handling Thread For Client
        # если кто-то из уже подключенных клиентов рассылает сообщение. Какое-нибудь, например "Привет! Как дела?"
        thread = threading.Thread(target=handle, args=(client,)) # здесь принимается список ВСЕХ клиентов
        thread.start()

print("Server if listening...")
receive()
#Receive -- broadcast -- handle