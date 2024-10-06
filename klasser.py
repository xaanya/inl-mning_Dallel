import random

# Klass som representerar en kortlek med kort från 1 till 13
class Kortlek:
    def __init__(self) -> None:
        # Skapa en kortlek med kort från 1 till 13
        self.kortlek = list(range(1, 14))

    # Dra ett slumpmässigt kort från kortleken
    def dra_kort(self) -> int:
        return random.choice(self.kortlek)

# Klass som representerar en spelare, hanterar spelarens namn och poäng
class Spelare:
    def __init__(self, namn: str) -> None:
        self.namn: str = namn  
        self.poäng: int = 0  # Spelarens poäng börjar på 0

    # Dra ett kort från kortleken, uppdatera poängen och hantera ess
    def spela_kort(self, kortlek: Kortlek) -> int:

        # Dra ett kort från kortleken
        draget_kort: int = kortlek.dra_kort()

        # if-sats för hantering av ess (1/14)
        if draget_kort == 1:
            
            if self.poäng + 14 <= 21:
                draget_kort = 14 
            else:
                draget_kort = 1 

        # Lägg till det dragna kortets värde till spelarens poäng
        self.poäng += draget_kort

        # Skriv ut spelarens nuvarande kort och poäng
        print(f'{self.namn} drar ett kort med värdet: {draget_kort}')
        print(f'{self.namn} har nu {self.poäng} poäng.\n')

        # Returnera spelarens uppdaterade poäng så att det kan användas
        # för att avgöra spelets fortsatta gång t.ex om spelaren vunnit/förlorat
        return self.poäng

