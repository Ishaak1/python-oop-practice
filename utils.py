import os
import time as t
import sqlite3
import random as r

def clear_screen():

    os.system("cls")

def connect_db():

    db = sqlite3.connect("tamagotchi.db")
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    return cursor, db

def config_pets():

    owner_name = input("\nEnter your name: ").strip().lower()

    while len(owner_name) == 0:
        
        clear_screen()
        owner_name = input("\nEnter a valid name: ").strip().lower()
    
    clear_screen()
    cursor, db = connect_db()
    cursor.execute("SELECT * FROM owners")
    all_owners = {dict(owner)["name"].lower() : dict(owner)["id"] for owner in cursor.fetchall()}

    if owner_name.lower() not in all_owners.keys():

        cursor.execute("INSERT INTO owners (name) VALUES (?)", [owner_name])
        db.commit()
        cursor.execute("SELECT id FROM owners WHERE name = (?)", [owner_name])
        owner_id = dict(cursor.fetchone())["id"]

        pet_name = set_pet(cursor, db, owner_id)
        clear_screen()

    else:

        owner_id = all_owners[owner_name.lower()]

        cursor.execute("SELECT * FROM tamagotchi WHERE owner_id = (?)", [owner_id])
        pets = [dict(pet)["name"] for pet in cursor.fetchall()]
        
        if len(pets) > 0:
        
            print("\n1. Create a new pet")
            print("2. Load an existing pet")
            option = input("\nSelect an option: ")

            while option != "1" and option != "2":
                
                clear_screen()
                print("\n1. Create a new pet")
                print("2. Load an existing pet")
                option = input("\nSelect an option: ")

            if option == "1":
                
                clear_screen()
                pet_name = set_pet(cursor, db, owner_id)

            else:

                if len(pets) == 1:
                    
                    pet_name = pets[0]

                else:

                    clear_screen()
                    available_pets = []
                    print()

                    for i in range(len(pets)):

                        print(f"{i + 1}. {pets[i]}")
                        available_pets.append(str(i + 1))

                    option = input("\nSelect an option: ")

                    while option not in available_pets:
        
                        clear_screen()
                        print()

                        for i in range(len(pets)):

                            print(f"{i + 1}. {pets[i]}")

                        option = input("\nSelect a valid option: ")
                    
                    pet_index = int(option) - 1
                    pet_name = pets[pet_index]
    
        else: 

            pet_name = set_pet(cursor, db, owner_id)

    return owner_name, pet_name

def set_pet(cursor, db, owner_id):

    cursor.execute("SELECT * FROM tamagotchi WHERE owner_id = (?)", [owner_id])
    available_pets = [dict(pet)["name"].lower() for pet in cursor.fetchall()]

    pet_name = input("\nGive your pet a name: ").strip()

    while len(pet_name) == 0 or pet_name.lower() in available_pets: 
        
        clear_screen()
        pet_name = input("\nGive your pet a valid name: ").strip()
    
    clear_screen()
    gender = input("\nIs it a boy or girl (m/f): ").lower()

    while gender != "m" and gender != "f":

        clear_screen()
        gender = input("\nInput a valid gender (m/f): ").lower()

    cursor.execute("INSERT INTO tamagotchi (name, gender, energy, hunger, happiness, time, owner_id) VALUES (?, ?, ?, ?, ?, ?, ?)", [pet_name, gender, 5, 5, 5, t.time(), owner_id])
    db.commit()

    clear_screen()
    return pet_name

def validate_option(name):

    available_options = ["1", "2", "3", "4", "5"]

    clear_screen()
    display_menu(name)
    option = input("Select an option: ")
    
    while option not in available_options:

        clear_screen()    
        display_menu(name)
        option = input("Select a valid option: ")

    return option

def display_menu(name):

    print(f"\n1. View {name}'s stats")
    print(f"2. Feed {name}")
    print(f"3. Play with {name}")
    print(f"4. Let {name} go to sleep")
    print(f"5. Leave {name} in peace\n")

def inform_player(pet):
    
    clear_screen()
    is_done = False

    if pet.gender == "m":

        first_pronoun = "him"
        second_pronoun = "his"
        third_pronoun = "he"

    else:

        first_pronoun = "her"
        second_pronoun = "her"
        third_pronoun = "she"

    if pet.hunger >= 9 and pet.energy <= 1:

        is_done = True
        print(f"{pet.moods["dead"]}\n{pet.name} has passed away. You didn't take very good care of {first_pronoun}")

        pet.cursor.execute("DELETE FROM tamagotchi WHERE id = (?)", [pet.id])
        pet.db.commit()

        input("\nPress Enter to continue...")

        return is_done

    if pet.energy < 3:

        print(f"{pet.name} is feeling tired. Put {first_pronoun} to bed to help {first_pronoun} recharge!")

    if pet.hunger >= 7:

        print(f"{pet.name} is starving. Feed {first_pronoun} soon to keep {first_pronoun} healthy!")

    if pet.happiness <= 3:

        print(f"{pet.name} is unhappy. Play with {first_pronoun} or feed {first_pronoun} to boost {second_pronoun} mood.")

    if pet.energy < 3 or pet.hunger >= 7 or pet.happiness <= 3:

        input("\nPress Enter to continue...")

    return is_done

def display_actions(action, moods, name):
    
    random_time = r.randint(4, 10) / 3
    print(random_time)
    clear_screen()    
    print(f"\n{moods[action]}\n{name} is {action}.")
    t.sleep(random_time)
    clear_screen()
    print(f"\n{moods[action]}\n{name} is {action}..")
    t.sleep(random_time)
    clear_screen()
    print(f"\n{moods[action]}\n{name} is {action}...")
    t.sleep(random_time)
    clear_screen()    