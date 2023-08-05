import random
import time
import os
from GeneralGame import Game

class Guess(Game):
    def __init__(self):
        super().__init__()

    #this fuction is geterating a random number from 1 to the length of diff list
    def generate_number(self):
        secret_number = int(random.randint(1, self.difficulty()))
        return secret_number
        time.sleep(0.7)
        os.system('cls')

    #this function get a guess from the user
    def get_guess_from_user(self):
        guess_in = int(input("Enter your guess : "))
        return guess_in

    #this function compare the user input with the number that was generated

    def compare_results(self):
        y = self.generate_number()
        # What is the purpose of this function? if it only does int casting to an str, but you arleady do the casting inside the param
        z = self.get_guess_from_user()
        # so either dont use that function at all, or call it without params and manage all the input from user inside the function
        print(y)
        if y > z:
            print("guess is low")
        elif y < z:
            print("guess is high")
        elif y == z:
            print("you guessed it!")

    #this function starting the game
    def play(self):
        self.compare_results()




