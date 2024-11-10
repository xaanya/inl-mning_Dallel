import socket
import threading

HOST = '127.0.0.1'
PORT = 12345

# Funktion för att lyssna på inkommande meddelanden från servern
def listen_for_messages(client_socket):
    while True:
        try:
            # Ta emot och skriv ut meddelanden från servern
            message = client_socket.recv(512).decode('utf-8')
            print(f'\n{message}')
        except:
            # Om något går fel, koppla från
            print("Connection closed by server.")
            break

# Starta klienten och anslut till servern
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))
    
    # Ta emot uppmaning om att ange namn och skriv in namnet
    prompt = client_socket.recv(512).decode('utf-8')
    print(prompt, end='')
    name = input()
    client_socket.sendall(name.encode('utf-8'))
    
    print("Connected to server. Type 'exit' to leave the chat.")
    
    # Starta en tråd för att lyssna på inkommande meddelanden
    listen_thread = threading.Thread(target=listen_for_messages, args=(client_socket,))
    listen_thread.start()
    
    while True:
        # Skicka meddelanden till servern
        message = input("You: ")
        if message.lower() == 'exit':
            client_socket.sendall(message.encode('utf-8'))
            break
        client_socket.sendall(message.encode('utf-8'))
