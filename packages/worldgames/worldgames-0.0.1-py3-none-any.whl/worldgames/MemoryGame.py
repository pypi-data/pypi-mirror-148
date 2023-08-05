import random
from GeneralGame import Game

class Memory(Game):
    def __init__(self):
        super().__init__()

    #this fuction is geterating a random number from 1 to the 101
    def generate_sequence(self):
        randomlist = []
        for i in range(0, self.difficulty()):
            n = random.randint(1, 102)
            randomlist.append(n)
        return randomlist


    #this fuction is geterating a list from the user
    def get_list_from_user(self, get):
        getting = get
        return getting

    #this function compare between the random list that was generated to the list that the user entered
    def is_list_equal(self):
        random_list = self.generate_sequence()
        print(random_list)
        eq = (input("what you remember ?  : "))
        eq = eq.split(" ") # transform str to list of all items
        map_object = map(int, eq)
        list_of_integers = list(map_object)
        print(f"you entered the following list{list_of_integers}")
        if random_list == list_of_integers:
            print("Success")
            return True
        else:
            print("Fail")
            return False

    def play(self):
        self.is_list_equal()



