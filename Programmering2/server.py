import socket
import threading

HOST = '127.0.0.1'
PORT = 12345

# Lista för att hålla reda på alla anslutna klienters sockets och namn
clients = []

# Funktion för att hantera varje klientanslutning
def handle_client(client_socket, addr):
    print(f"New connection: {addr}")
    
    # Ta emot och spara användarnamn
    client_socket.sendall("Enter your name: ".encode('utf-8'))
    name = client_socket.recv(512).decode('utf-8')
    clients.append((client_socket, name))  # Lägg till klient och namn i listan

    print(f"{name} has joined the chat!")
    broadcast(f"{name} has joined the chat!", client_socket)
    
    try:
        while True:
            # Ta emot data från klienten
            data = client_socket.recv(512)
            if not data:
                break

            # Dekoda meddelandet från klienten
            message = data.decode('utf-8')
            print(f'{name}: {message}')
            
            # Om klienten skickar "exit", avsluta anslutningen
            if message.lower() == "exit":
                print(f"{name} has left the chat.")
                broadcast(f"{name} has left the chat.", client_socket)
                break
            
            # Sprid meddelandet till alla andra anslutna klienter
            broadcast(f"{name}: {message}", client_socket)
    finally:
        # När klienten kopplar från, ta bort klienten från listan
        clients.remove((client_socket, name))
        client_socket.close()
        print(f"Connection closed: {addr}")

# Funktion för att skicka ett meddelande till alla anslutna klienter
def broadcast(message, sender_socket):
    for client_socket, _ in clients:
        if client_socket != sender_socket:  # Skicka inte tillbaka till avsändaren
            try:
                client_socket.sendall(message.encode('utf-8'))
            except:
                # Om det uppstår ett fel, ta bort klienten från listan
                clients.remove((client_socket, _))

# Starta servern och lyssna på inkommande anslutningar
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f'Server is listening on {HOST}:{PORT}')
    
    while True:
        # Acceptera ny klientanslutning
        client_socket, addr = server_socket.accept()
        
        # Starta en ny tråd för att hantera klientens kommunikation
        client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_thread.start()
