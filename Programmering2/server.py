
import socket  # Importerar socket-biblioteket för att skapa nätverksanslutningar
import threading  # Importerar threading-biblioteket för att kunna hantera flera klienter samtidigt

HOST = '127.0.0.1'  # Definierar serverns IP-adress (127.0.0.1 är min dator, "localhost")
PORT = 12345  # Definierar porten som servern kommer att lyssna på

# En lista för alla anslutna klienter. Varje klient representeras som en tuple
# där första elementet är (socket/anslutningen) och andra elementet är klientens namn
clients = []

# Funktion som hanterar varje klientanslutning
def handle_client(client_socket, addr):
    print(f"New connection: {addr}")  # Skriver ut när en ny klient ansluter
    
    # Ber om klientens namn 
    client_socket.sendall("Enter your name: ".encode('utf-8'))
    
    # Ta emot och dekoda klientens namn
    name = client_socket.recv(512).decode('utf-8')
    
    # Lägg till klienten och dess namn i listan "clients"
    clients.append((client_socket, name))

    print(f"{name} has joined the chat!")  # Skriver ut när en ny klient har anslutit
    broadcast(f"{name} has joined the chat!", client_socket)  # Meddelar också alla andra klienter om den nya anslutningen
    
    try:
        while True:
            # Ta emot data (meddelanden) från klienten
            data = client_socket.recv(512) 
            if not data:  # Om ingen data tas emot (dvs klienten kopplade bort sig), bryt loopen
                break

            # Dekoda det mottagna meddelandet så det blir till en läsbar string
            message = data.decode('utf-8')
            print(f'{name}: {message}')  # Skriver ut klientens mededlande på servern
            
            # Om klienten skriver "exit", stäng av anslutningen
            if message.lower() == "exit":
                print(f"{name} has left the chat.") # Meddelar att klienten har lämnat chatten
                broadcast(f"{name} has left the chat.", client_socket) # Informera alla andra om att klienten har lämnat
                break  
            
            # Om klienten inte skulle zskriva "exit", sänd meddelandet till alla andra anslutna klienter
            broadcast(f"{name}: {message}", client_socket)
    finally:
        # Här körs alltid detta block när klienten kopplar från eller om det blir något fel
        clients.remove((client_socket, name))  # Ta bort klienten från listan
        client_socket.close()  # Stäng anslutningen
        print(f"Connection closed: {addr}")  # Meddelar att anslutningen är stängd

# Funktion för att skicka ett meddelande till alla anslutna klienter
def broadcast(message, sender_socket):
    # Loopa genom alla klienter i listan "clients"
    for client_socket, _ in clients:
        if client_socket != sender_socket:  # Skicka inte meddelandet tillbaka till den klient som skickade det
            try:
                client_socket.sendall(message.encode('utf-8'))  # Skicka meddelandet till klienten
            except:
                # Om något går fel (t.ex. om en klient inte längre är ansluten), ta bort klienten från listan
                clients.remove((client_socket, _))

# Starta servern och lyssna på inkommande anslutningar
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:  # Skapa en TCP/IP-server-socket
    server_socket.bind((HOST, PORT))  # Bind servern till den lokala adressen och potten
    server_socket.listen()  # Servern börjar lyssna på inkommande anslutningar
    print(f'Server is listening on {HOST}:{PORT}')  # Skriver ut att servern är igång och väntar på klienter
    
    while True:
        # Acceptera inkommande anslutning från en klient
        client_socket, addr = server_socket.accept()
        
        # Starta en ny tråd för att hantera kommunikationen med denna klient
        client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_thread.start()  # Starta tråden för att hantera klientens meddelanden
