from klasser import Kortlek, Spelare

# Spelarens tur, där spelaren drar kort och väljer att fortsätta eller stanna
def spelarens_tur(spelare: Spelare, kortlek: Kortlek) -> bool:
    while True:
        poäng: int = spelare.spela_kort(kortlek)  # Spelaren drar ett kort från kortleken

        # Om spelarens poäng går över 21, har spelaren förlorat
        if poäng > 21:
            print(f'{spelare.namn} har {spelare.poäng} poäng. Du har förlorat! \U0001F622 \n')
            return False  # Avsluta spelarens runda

        # Fråga spelaren om hen vill dra ett till kort
        val: str = input('Vill du dra ett kort till? (ja/nej): ').lower()
        if val != 'ja':
            print(f'{spelare.namn} har valt att stanna med {spelare.poäng} poäng.')
            return True  # Spelaren stannar och rundan avslutas

# Datorns tur - datorn fortsätter dra kort tills den når minst 17 poäng
def datorns_tur(dator: Spelare, kortlek: Kortlek) -> bool:
    while dator.poäng < 17: 
        dator.spela_kort(kortlek)

    # Om datorns poäng går över 21, har datorn förlorat
    if dator.poäng > 21:
        
        print(f'Motståndaren har {dator.poäng} poäng och har förlorat!')
        print(f'GRATTIS, DU VANN!!! \U0001F601')
        return False
    
    else:
        # Om datorn har stannat under eller på 21 poäng
        print(f'Motståndaren har stannat med {dator.poäng} poäng.\n')
        return True

# Skapa en kortlek och två spelare (en spelare och en motståndare som är datorn)
kortlek: Kortlek = Kortlek()
spelare: Spelare = Spelare("Du") 
dator: Spelare = Spelare("Motståndaren") 


# Spela spelet
if spelarens_tur(spelare, kortlek):  # Spelarens tur
    print()  # tom rad här för att få tydligare utskrift
    if datorns_tur(dator, kortlek):  # Datorns tur
        # Jämför poäng mellan spelaren och datorn för att utse vinnaren
        if spelare.poäng > dator.poäng:
            print(f'{spelare.namn} vinner med {spelare.poäng} poäng mot motståndaren {dator.poäng} poäng \U0001F601.')
        elif spelare.poäng < dator.poäng:
            print(f'Motståndaren vinner med {dator.poäng} poäng mot dina {spelare.poäng}')
            print(f'Du har förlorat \U0001F622 ')
        else:
            print(f'Oavgjort! Både {spelare.namn} och motståndaren har {spelare.poäng} poäng. Motståndaren vinner!\U0001F622')
