import random as r
from tamagotchi import Tamagotchi
from utils import clear_screen, config_pets, validate_option, inform_player

def main():

    clear_screen()
    
    owner_name, pet_name = config_pets()
    pet = Tamagotchi(owner_name, pet_name)
    run_game(pet)

def run_game(pet):
    
    is_done = inform_player(pet)
    
    while not is_done:

        option = validate_option(pet.name)
        clear_screen()

        if option == "1":

            pet.stats()
            input("Press Enter to continue...")

        elif option == "2":

            pet.eat()
            input("Press Enter to continue...")     

        elif option == "3":
            
            pet.play()
            input("Press Enter to continue...")

        elif option == "4":

            pet.sleep()
            input("Press Enter to continue...")

        else:

            is_done = True
            pet.db.commit()
            pet.db.close()

main()