import socket
import threading

# Configurações do servidor
HOST = 'localhost'
PORT = 8888

# Dicionário para armazenar os clientes conectados
clients = {}

# Dicionário para armazenar os usuários registrados (usuário: senha)
registered_users = {
    "joao": "senha123",
    "maria": "123456"
}


# Função para lidar com as mensagens recebidas de um cliente
def handle_client(client_socket, client_address):
    # Autenticação do cliente
    authenticated = False
    username = None

    try:
        while not authenticated:
            client_socket.send("login ou registro: ".encode())
            auth_type = client_socket.recv(1024).decode()

            if auth_type == "login":
                client_socket.send("Username: ".encode())
                username = client_socket.recv(1024).decode()
                client_socket.send("Password: ".encode())
                password = client_socket.recv(1024).decode()

                if registered_users.get(username) == password:
                    authenticated = True
                    client_socket.send("Autenticação bem-sucedida.".encode())
                else:
                    client_socket.send("Credenciais incorretas. Tente novamente.".encode())
            elif auth_type == "registro":
                client_socket.send("Novo Username: ".encode())
                new_username = client_socket.recv(1024).decode()
                client_socket.send("Nova Password: ".encode())
                new_password = client_socket.recv(1024).decode()

                if new_username not in registered_users:
                    registered_users[new_username] = new_password
                    authenticated = True
                    client_socket.send("Registro bem-sucedido.".encode())
                else:
                    client_socket.send("Usuário já registrado. Tente novamente.".encode())

        # Agora o cliente está autenticado
        clients[client_socket] = (username, client_address)

        # Recebe e exibe as mensagens do cliente
        while True:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            print(f"Received from {username}: {message}")

            # Encaminha a mensagem para todos os outros clientes
            for client, (other_username, _) in clients.items():
                if client != client_socket:
                    try:
                        client.send(f"{username}: {message}".encode())
                    except Exception as e:
                        print(f"Error sending message to {other_username}: {e}")

    except Exception as e:
        print(f"Error with {username}: {e}")

    # Remove o cliente da lista de clientes
    del clients[client_socket]
    print(f"Connection with {username} ({client_address}) closed")


# Configuração do servidor
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)
print(f"Server listening on {HOST}:{PORT}")

# Aguarda conexões de clientes
while True:
    client_socket, client_address = server.accept()
    print(f"Accepted connection from {client_address}")

    # Inicia uma nova thread para lidar com o cliente
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()
