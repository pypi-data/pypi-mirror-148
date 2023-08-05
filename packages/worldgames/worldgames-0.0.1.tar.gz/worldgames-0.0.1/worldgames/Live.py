from GeneralGame import games_mapping
from MemoryGame import Memory
from GuessGame import Guess
from CurrencyRouletteGame import Currency
### this is sample of the load game function you shuld have



def load_game():
    mem_game = Memory()
    guess_game = Guess()
    currency = Currency()
    game_selection = input(f"The are Games are {games_mapping}: ")
    if game_selection.isdigit():
        game_selection = int(game_selection)

        if game_selection in games_mapping.keys():
            print(f"You have selected the game {games_mapping.get(game_selection)}")
            if game_selection == 1:
                mem_game.welcome("danny")
                mem_game.play()
            elif game_selection == 2:
                guess_game.welcome("danny")
                guess_game.play()
            elif game_selection == 3:
                currency.welcome("danny")
                currency.play()

        else:
            print("You entered wrong game")

    else:
        print("You entered something that is not digit")

load_game()

