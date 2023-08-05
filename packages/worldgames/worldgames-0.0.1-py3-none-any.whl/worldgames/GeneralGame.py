from abc import ABC, abstractmethod

games_mapping = {1: "Memory Game", 2: "Guess Game", 3: "Currency Roulette"}
diff = [1, 2, 3, 4, 5]

class Game(ABC):

    @abstractmethod
    def play(self):
        pass

    def welcome(self, name):
        print(f"Hello {name} and welcome to the World of Games (WoG)")
        print("Here you can find many cool games to play")

    def difficulty(self):
            user_selection = input(" The range of difficulty is between Level 1-5 \n please select difficulty level : ")
            if user_selection.isdigit():
                user_selection = int(user_selection)
                return user_selection # if you put return, any code under it will never run.
                if user_selection in diff: # this code will never run
                    print(f"You have selected difficultly of {user_selection}")
                else:
                    print("You entered diffuculty out of range")
            else:
                print("You entered something that is not digit")

