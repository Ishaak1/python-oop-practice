import time as t
import math
import random as r
import sqlite3
from utils import clear_screen, display_actions

def setup_database():

    db = sqlite3.connect("tamagotchi.db")
    db.row_factory = sqlite3.Row
    cursor = db.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS owners (
    
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT
    
    )""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS tamagotchi (

        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        gender TEXT,
        energy INTEGER,
        hunger INTEGER,
        happiness INTEGER,
        time REAL,
        owner_id INTEGER,

        FOREIGN KEY (owner_id) REFERENCES owners (id)

    )""")

    return db, cursor

class Tamagotchi:
    
    moods = { 
        
        "hungry": "🤤", 
        "neutral": "🙂", 
        "sleeping": "💤", 
        "happy": "😄", 
        "playing": "🐕", 
        "eating": "🍗", 
        "dead": "🩻", 
        "unhappy": "😣", 
        "tired": "🥱", 
        "sad": "🥺", 
        "energy": "💪"

    }

    db, cursor = setup_database()

    def __init__(self, owner, name, gender = "m"):
        
        self.owner = owner
        self.name = name
        self.gender = gender

        self._prepare_data()
        self.cursor.execute("SELECT * FROM tamagotchi t JOIN owners u ON u.id = t.owner_id WHERE u.name = (?) AND t.name = (?)", [owner, name])
        pet_info = self.cursor.fetchone()

        self.hunger = pet_info["hunger"]
        self.happiness = pet_info["happiness"]
        self.energy = pet_info["energy"]
        self.gender = pet_info["gender"]
        self.id = pet_info["id"]

        self._neglect_damage(pet_info)

    def stats(self):

        if self.hunger % 1 < 0.5:
            
            hunger_bar = math.floor(self.hunger)

            if self.hunger > 10:

                hunger_bar = 10
        
        else: 

            hunger_bar = math.ceil(self.hunger)

        if self.energy % 1 < 0.5:

            energy_bar = math.floor(self.energy)

            if self.energy > 10:

                energy_bar = 10
        
        else:

            energy_bar = math.ceil(self.energy)

        if self.happiness % 1 < 0.5:

            happiness_bar = math.floor(self.happiness)

            if self.happiness > 10:

                happiness_bar = 10

        else:

            happiness_bar = math.ceil(self.happiness)

        hunger_meter = "█" * hunger_bar + "░" * (10 - hunger_bar)
        energy_meter = "█" * energy_bar +  "░" * (10 - energy_bar)
        happiness_meter = "█" * happiness_bar +  "░" * (10 - happiness_bar)
        
        if self.hunger == 5:

            hunger_emoji = self.moods["neutral"]
        
        elif self.hunger > 5:

            hunger_emoji = self.moods["hungry"]
        
        else:

            hunger_emoji = self.moods["happy"]

        if self.energy == 5:

            energy_emoji = self.moods["neutral"]
        
        elif self.energy < 5:

            energy_emoji = self.moods["tired"]
        
        else:

            energy_emoji = self.moods["energy"]

        if self.happiness == 5:

            happiness_emoji = self.moods["neutral"]

        elif self.happiness < 5:

            happiness_emoji = self.moods["sad"]

        else:

            happiness_emoji = self.moods["happy"]

        clear_screen()
        print()
        print(self.name.upper())
        print()
        print(f"Hunger        {hunger_meter} {hunger_emoji}")
        print(f"Energy        {energy_meter} {energy_emoji}")
        print(f"Happiness     {happiness_meter} {happiness_emoji}\n")
    
    def eat(self):

        if self.hunger >= 4:

            if self.gender == "m":
        
                boy_or_girl = "he"

            else:

                boy_or_girl = "she"

            decrease_hunger = r.randint(1, 3)
            increase_energy = r.randint(1, 3)
            increase_happiness = r.randint(1, 3)
            random_time = r.randint(4,10) / 3
            
            display_actions("eating", self.moods, self.name)
            
            if (self.hunger - decrease_hunger) <= 0:

                self.hunger = 0
            
            else: 

                self.hunger -= decrease_hunger
            
            if (self.energy + increase_energy) >= 10:

                self.energy = 10

            else: 

                self.energy += increase_energy
            
            if (self.happiness + increase_happiness) >= 10:

                self.happiness = 10
            
            else:

                self.happiness += increase_happiness

            self.cursor.execute("UPDATE tamagotchi SET energy = (?), hunger = (?), happiness = (?), time = (?) WHERE id = (?)", [self.energy, self.hunger, self.happiness, t.time(), self.id])
            self.db.commit()

            print(f"\n{self.name} is {decrease_hunger * 10}% less hungry after eating.")
            print(f"{self.name} is {increase_energy * 10}% more energetic after eating.")
            print(f"{self.name} is {increase_happiness * 10}% happier after eating.\n")

        else:

            clear_screen()
            print(f"\n{self.name} is not hungry\n")

    def play(self):

        if self.energy >= 4:

            display_actions("playing", self.moods, self.name)
            
            increase_hunger = r.randint(1, 3)
            decrease_energy = r.randint(1, 3)
            increase_happiness = r.randint(1, 3)

            if (self.hunger + increase_hunger) >= 10:

                self.hunger = 10
                
            else:

                self.hunger += increase_hunger

            if (self.energy - decrease_energy) <= 0:

                self.energy = 0

            else:

                self.energy -= decrease_energy
            
            if (self.happiness + increase_happiness) >= 10:

                self.happiness = 10
            
            else:

                self.happiness += increase_happiness

            self.cursor.execute("UPDATE tamagotchi SET energy = (?), hunger = (?), happiness = (?), time = (?) WHERE id = (?)", [self.energy, self.hunger, self.happiness, t.time(), self.id])
            self.db.commit()

            print(f"\n{self.name} has {decrease_energy * 10}% less energy after playing")
            print(f"{self.name} is {increase_hunger * 10}% hungrier after playing")
            print(f"{self.name} is {increase_happiness * 10}% happier after playing\n")

        else:

            clear_screen()
            print(f"\n{self.name} doesn't have enough energy to play.\n")
        
    def sleep(self):

        if self.energy <= 4:

            display_actions("sleeping", self.moods, self.name)

            increase_hunger = r.randint(1, 3)
            increase_energy = r.randint(1, 3)
            decrease_happiness = r.randint(1, 3)

            if (self.hunger + increase_hunger) >= 10:

                self.hunger = 10
                
            else:

                self.hunger += increase_hunger

            if (self.energy + increase_energy) >= 10:

                self.energy = 10

            else: 

                self.energy += increase_energy

            if (self.happiness - decrease_happiness) <= 0:

                self.happiness = 0
            
            else:

                self.happiness -= decrease_happiness

            if self.gender == "m":

                boy_or_girl = "he's" 

            else:

                boy_or_girl = "she's"

            clear_screen()

            self.cursor.execute("UPDATE tamagotchi SET energy = (?), hunger = (?), happiness = (?), time = (?) WHERE id = (?)", [self.energy, self.hunger, self.happiness, t.time(), self.id])
            self.db.commit()

            print(f"\n{self.name} has {increase_energy * 10}% more now that {boy_or_girl} awake.")
            print(f"{self.name} is {increase_hunger * 10}% hungrier now that {boy_or_girl} awake.")
            print(f"{self.name} is {decrease_happiness * 10}% happier now that {boy_or_girl} awake.\n")

        else:

            clear_screen()
            print(f"\n{self.name} has too much energy to go sleep.\n")
        
    def _neglect_damage(self, pet_info):

        self.cursor.execute("SELECT * FROM tamagotchi WHERE id = (?)", [self.id])
        info = dict(self.cursor.fetchone())
        passed_time = t.time() - pet_info["time"]
        hours = int(passed_time // 3600)

        if hours >= 2:

            damage = hours * 0.4
            self.cursor.execute("UPDATE tamagotchi SET time = (?) WHERE id = (?)", [t.time(), self.id])
            self.db.commit()

            if (self.hunger + damage) >= 10:

                self.hunger = 10
                
            else:

                self.hunger += damage

            if (self.energy - damage) <= 0:

                self.energy = 0

            else: 

                self.energy -= damage

            if (self.happiness - damage) <= 0:

                self.happiness = 0
            
            else:

                self.happiness -= damage   

            self.cursor.execute("UPDATE tamagotchi SET energy = (?), hunger = (?), happiness = (?), time = (?) WHERE id = (?)", [self.energy, self.hunger, self.happiness, t.time(), self.id])
            self.db.commit()

    def _prepare_data(self):

        self.cursor.execute("SELECT * FROM tamagotchi t JOIN owners u ON u.id = t.owner_id WHERE u.name = (?) AND t.name = (?)", [self.owner, self.name])
        owner_pet_info = self.cursor.fetchall()
        
        if len(owner_pet_info) == 0:

            self.cursor.execute("SELECT * FROM owners WHERE name = (?)", [self.owner])
            owner_info = self.cursor.fetchall()
            
            if len(owner_info) == 0:

                self.cursor.execute("INSERT INTO owners (name) VALUES (?)", [self.owner])
                self.db.commit()

            self.cursor.execute("SELECT id FROM owners WHERE name = (?)", [self.owner])
            owner_id = dict(self.cursor.fetchone())["id"]

            self.cursor.execute("INSERT INTO tamagotchi (name, hunger, happiness, energy, gender, time, owner_id) VALUES (?, ?, ?, ?, ?, ?, ?)", [self.name, 5, 5, 5, self.gender, t.time(), owner_id])
            self.db.commit()