import requests
import random
from GeneralGame import Game

url = 'https://v6.exchangerate-api.com/v6/8454f0610167ea1dac0488f8/latest/USD'

response = requests.get(url)
data = response.json()
ILS = data['conversion_rates']['ILS']
USD = data['conversion_rates']['USD']
rate_of_ils_to_usd = ILS / USD
rand = (random.randint(1, 101))
class Currency(Game):
    
    def __init__(self):
        super().__init__()

    def get_money_interval(self):
        diff = self.difficulty()
        print(f" the random number is {rand} ")
        Min = rate_of_ils_to_usd * (rand - (5 - diff))
        Max = rate_of_ils_to_usd * (rand + (5 - diff))
        return Min, Max


    def get_user_input(self):
        guess_in = (input(f"what do you think is the convert of {rand} from ILS to USD?"))
        return guess_in

    def compare_results(self):
        Min, Max = self.get_money_interval()
        user_guess = self.get_user_input()

        if float(user_guess) >= Min and float(user_guess) <= Max:
            print(True)
        else:
             print(False)

    def play(self):
        self.compare_results()
  