import socket  # Importera socket-biblioteket för att skapa nätverksanslutningar
import threading # Importerar threading-biblioteket för att kunna hantera flera klienter samtidigt

HOST = '127.0.0.1'  # IP-adressen till servern (127.0.0.1 är lokala datorn, "localhost")
PORT = 12345  # Porten servern lyssnar på

# Funktion för att lyssna på inkommande meddelanden från servern
def listen_for_messages(client_socket):
    while True:
        try:
            # Ta emot och skriv ut meddelanden från servern
            message = client_socket.recv(512).decode('utf-8')  # Tar emot upp till 512 byte och dekodar det
            print(f'\n{message}')  # Skriver ut meddelandet på skärmen
        except:
            # Om något går fel, till exempel att servern stänger anslutningen, koppla från
            print("Connection closed by server.")
            break  # Avslutar loopen och därmed tråden

# Starta klienten och anslut till servern
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:  # Skapar en TCP/IP-socket
    client_socket.connect((HOST, PORT))  # Anslut till servern på den adressen och porten som gäller
    
    # Ta emot meddelande om att ange namn från servern och skriv in namnet
    request_message = client_socket.recv(512).decode('utf-8')  # Väntar på meddelande från servern om att ange namn
    print(request_message, end='')  # Skriv ut meddelandet för att ange namn (utan radbrytning)
    name = input() 
    client_socket.sendall(name.encode('utf-8'))  # Skicka användarens namn till servern

    
    print("Connected to server. Type 'exit' to leave the chat.")  # Meddelande om att anslutningen är etablerad
    
    # Starta en tråd för att lyssna på inkommande meddelanden från servern
    listen_thread = threading.Thread(target=listen_for_messages, args=(client_socket,))
    listen_thread.start()  # Starta tråden för att lyssna på meddelanden parallellt
    
    while True:
        # Skicka meddelanden till servern
        message = input("You: ")  # Ta emot användarens meddelande
        if message.lower() == 'exit':  # Om användaren skriver "exit", skicka det och avsluta
            client_socket.sendall(message.encode('utf-8'))  # Skicka exit-meddelandet till servern
            break  # Avsluta loopen och därmed klientens program
        client_socket.sendall(message.encode('utf-8'))  # Skicka det inmatade meddelandet till servern
