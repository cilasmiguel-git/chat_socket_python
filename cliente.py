import socket
import threading

# Configurações do cliente
HOST = 'localhost'
PORT = 8888

# Criação do socket do cliente
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

# Função para enviar mensagens ao servidor
def send_message():
    while True:
        try:
            message = input()
            client.send(message.encode())
        except Exception as e:
            print(f"Error sending message: {e}")
            break

# Inicia uma thread para enviar mensagens
send_thread = threading.Thread(target=send_message)
send_thread.start()

# Recebe e exibe mensagens do servidor
while True:
    try:
        message = client.recv(1024).decode()
        if not message:
            break
        print(message)
    except Exception as e:
        print(f"Error receiving message: {e}")
        break
