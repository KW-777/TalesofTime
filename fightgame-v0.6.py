from random import randint
import os.path
from ast import literal_eval
class FightGame:
    VERSION = 0.5
    current_character = None
    current_opponent = None
    globalself = None
    def __init__(self):
        FightGame.globalself = self
        print("Welcome to Fight Game v%.1f!" % FightGame.VERSION)
        self.charwiz()    
    def charwiz(self): #Customize Character
        char = input("Choose your class: (Warrior,Archer,Mage,Raider): ")
        if char == "":
            char = "Invalid"
        name = input("Enter your name: ")
        if name == "":
            name = "Player"
        self.charselect(char,name)    
    def charselect(self,chartype="Warrior",name="Player"): #Assigns class
        self.character = None
        self.char = chartype
        self.name = name
        if chartype.lower() == "warrior":
            self.character = Warrior(name)
        elif chartype.lower() == "archer":
            self.character = Archer(name)
        elif chartype.lower() == "mage":
            self.character = Mage(name)
        elif chartype.lower() == "raider":
            self.character = Raider(name)
        elif chartype.lower() == "adventurer":
            self.character = Adventurer(name)
        elif chartype == "DEVELOPER": #debug class
            self.character = Dev(name)
        else:
            self.character = Warrior(name)
            print("(!)\n[ERROR] Invalid Class, assigning default\n(!)")   
        self.opponent = None
        FightGame.current_character = self.character
        self.mainmenu()
##Battle Functions##
    def newOpponent(self): #New Opponent
        if self.boss_class() == True:
            self.opponent = self.get_boss()
        else:
            ranclass = randint(0,3)
            names = ["Terry the %s", "John the %s", "Declan the %s", "Steve the %s", "Joe the %s", "Brian the %s", "Alex the %s"]
            ranName = randint(1,len(names)-1)
            if ranclass == 0:
                oppchar = "Warrior"
                self.opponent = Warrior(name=names[ranName] % oppchar)
            elif ranclass == 1:
                oppchar = "Archer"
                self.opponent = Archer(name=names[ranName] % oppchar)
            elif ranclass == 2:
                oppchar = "Mage"
                self.opponent = Mage(name=names[ranName] % oppchar)
            elif ranclass == 3:
                oppchar = "Raider"
                self.opponent = Raider(name=names[ranName] % oppchar)
            else:
                oppchar = "Adventurer"
                self.opponent = Adventurer(name=names[ranName] % oppchar)
            print("(!)New Opponent Incoming(!)")
            print("\nA wild %s has appeared!" % oppchar)
        FightGame.current_opponent = self.opponent
        self.set_dif()
        self.fightmenu()
    def attack(self): #Player Atk
        if self.opponent.health > 0:
            randomnum = self.character.critrate
            atkhit = 1 != randint(1,self.character.ranatk)
            if atkhit:
                dmg = (self.character.damage * (1 - (self.opponent.defense / 100)))
                #Crit Attack
                if randomnum == 1:
                    dmg *= self.character.critpercent
                    print("\n%s landed a critical strike on %s dealing %.1f dmg" % (self.character.name, self.opponent.name, dmg))
                else: 
                    ranmsg = randint(0,len(self.character.atkmsg)-1)
                    print(self.character.atkmsg[ranmsg] % (self.character.name, self.opponent.name, dmg))                    
                self.opponent.health -= dmg
                if self.opponent.health <= 0:
                    if self.opponent.isBoss == True:
                        self.opponent.fightWin()
                    self.fightWin()
                else:
                    print(f"\n{self.opponent.name}'s remaining health: {self.opponent.health:.1f}")
            else:
                print("Your attack missed :(")
    def oppatk(self): #Opponent Atk
        if self.character.health > 0:
            randomnum = self.character.critrate
            atkhit = 1 != randint(1,self.opponent.ranatk)
            if atkhit:
                dmg = (self.opponent.damage * (1-(self.character.defense/100)))
                if randomnum == 1:
                    dmg = dmg * self.opponent.critpercent
                    print("\n%s landed a critical strike on %s dealing %.1f dmg" % (self.opponent.name, self.character.name, dmg))
                else:
                    randommsg = randint(0,len(self.opponent.atkmsg)-1)
                    print(self.opponent.atkmsg[randommsg] % (self.opponent.name, self.character.name, dmg))
                self.character.health -= dmg
                if self.character.health <= 0:
                    self.fightLoss()
                else:
                    print("\n%s's remaining health: %.1f" % (self.character.name,self.character.health))
            else:
                print("\n%s's attacked missed" % (self.opponent.name))   
    def atkround(self): #Atk turns
        if self.opponent == None:
            self.newOpponent()
        if self.character.speed > self.opponent.speed: #Player is faster, Player hits first
            print("You are faster than %s, you managed to hit first\n" % (self.opponent.name))
            self.attack()
            self.oppatk()
        elif self.character.speed == self.opponent.speed: #Equal Speeds, 50% chance
            randnum = randint(1,2)
            if randnum == 1:
                print("You are faster than %s, you managed to hit first\n" % (self.opponent.name))
                self.attack()
                self.oppatk()
            if randnum == 2: 
                print("%s was faster than you, they hit you first\n" % (self.opponent.name))
                self.oppatk()
                self.attack()
        elif self.character.speed < self.opponent.speed: #Opponent is faster, hits first
            print("%s is faster than you, they hit you first\n" % (self.opponent.name))
            self.oppatk()
            self.attack()
        self.character.health += self.character.regen
        self.opponent.health += self.opponent.regen
        if self.character.regen > 0:
            print(f"{self.character.name} regenerated {self.character.regen}hp") 
        if self.opponent.regen > 0:
            print(f"{self.opponent.name} regenerated {self.opponent.regen}hp") 
        if self.opponent.health and self.character.health > 0:
            self.fightmenu()
    def run(self): #Run from fight
        if self.opponent.isBoss:
            print("You can't run from a boss!!")
            self.oppatk()
            self.fightmenu()
        elif self.character.speed > self.opponent.speed:
            self.opponent = None
            print("You ran from the fight")
            y = input("Would you like to fight another opponent? (y/n): ")
            if y == "y":
                self.newOpponent()
            else:
                self.mainmenu()
        else:
            randnum = randint(1,4)
            if randnum == 1:
                print("Flee Attempt Failed.")
                self.oppatk()
                self.fightmenu()
            else:
                self.opponent = None
                print("You ran from the fight")
                y = input("Would you like to fight another opponent? (y/n): ")
                if y == "y":
                    self.newOpponent()
                else:
                    self.mainmenu()
    def itemdrop(self,name="Opponent"): #Consumable drops
        chance = randint(1,5)
        if chance == 1:
            self.character.items[0] += 1
            print("%s dropped a medpack!" % name)
        if chance == 2:
            self.character.items[1] += 1
            print("%s dropped 1x Go-Juice!" % name)
        if chance == 3:
            self.character.items[2] += 1
            print("%s dropped 1x Adrenaline Booster" % name)            
    def fightWin(self): #Victory
        self.itemdrop(self.opponent.name)
        self.opponent = None
        randcoins = self.character.coinrate
        self.character.damage += 5
        self.character.speed += 5
        self.character.kc += 1
        self.character.health += 75
        if self.character.health > self.character.maxhealth:
            self.character.health = self.character.maxhealth
        self.character.coins += randcoins
        self.check_gj()
        self.check_adr()
        print("\nYou have defeated your opponent! [+75 Health, +5 Max Damage, +5 Max Speed, +%d coins]" % randcoins)
        y = input("\nWould you like to fight another opponent? (y/n): ")
        if y == "y":
            self.newOpponent()
        else:
            self.mainmenu()
    def fightLoss(self): #Failure
        self.character.health = 0
        print("\n%s has reached 0 health and died." % self.character.name)
        print("Game Over:(")
        self.info()
        newgame = input("\nWould you like to create a new character? (y/n)")
        if newgame == "y":
            self.character = None
            self.charwiz()
        else:
            print("\nThank you for playing!")
            self.character = None
            return
##Consumables##
    def inv(self): #Inventory
        try:
            for index in range(len(self.character.items)):
                if index == 0:
                    itemname = "(M) Medpacks"
                    bio = "Restores 150 Health"
                if index == 1:
                    itemname = "(G) Go-Juice"
                    bio = "Boosts Speed, Accuracy & Crit chance"
                if index == 2:
                    itemname = "(A) Adr Boosters"
                    bio = "Boosts Damage, Crits & Defense Moderately "
                print("\n%dx %s\n=>%s" % (self.character.items[index],itemname,bio))
            y = input("\nWould you like to use an item?(y/n)")
            if y == "y":
                x = input("What item would you like to use (M,G,A):").upper()
                if x == "M":
                    self.apply_hp()
                    self.inv()
                if x == "G":
                    self.apply_gj()
                    self.inv()
                if x == "A":
                    self.apply_adr()
                    self.inv()
            else:
                if self.prevmenu == "fm":
                    self.fightmenu()
                else:
                    self.mainmenu()
        except Exception as e:
            print(f"An unexpected error occurred while getting menu: {e}")
    def apply_hp(self): #Apply Medpack
        if self.character.items[0] == 0:
            print("(!)\nYou don't have enough Medpacks!\n(!)")
        else:
            if self.character.health <= self.character.maxhealth:
                self.character.items[0] -= 1
                self.character.health += 150
                if self.character.health > self.character.maxhealth:
                    self.character.health = self.character.maxhealth
            print("Administered Medpack. User Health: %.1f/%d" %(self.character.health,self.character.maxhealth))
    def apply_gj(self): #Apply Go-Juice
        if self.character.items[1] == 0:
            print("(!)\nYou don't have enough Go-Juice!/n(!)")
        elif self.character.gjr > 0:
            print("Duration of Go-Juice Extended.")
            self.character.gjr += 3
            self.character.items[1] -= 1
        else:
            self.character.gjr += 3
            self.character.items[1] -= 1
            self.oldspeed = self.character.speed
            self.oldranatk = self.character.ranatk
            self.oldcritrate = self.character.critrate
            print("Administered Go-Juice. Stats buffed for 3 rounds.")
            self.character.speed += 30
            self.character.ranatk = 200
            self.character.critrate = randint(1,3)
            self.character.gj = True
            self.inv()     
    def check_gj(self): #Check Go-Juice
        if self.character.gjr > 1:
            self.character.gjr -= 1
        elif self.character.gjr <= 1 and self.character.gj == True:
            self.character.speed = self.oldspeed
            self.character.ranatk = self.oldranatk
            self.character.critrate = self.oldcritrate
            print("(!)\nYour Go-Juice has Expired.\n(!)")
            self.gjr = 0
            self.character.gj = False
    def apply_adr(self): #Apply Adrenaline Shot
        if self.character.items[2] == 0:
            print("(!)\nYou don't have enough Adrenaline Shots!/n(!)")
        elif self.character.asr > 0:
            print("Duration of Adrenaline Extended.")
            self.character.asr += 3
            self.character.items[2] -= 1
        else:
            self.character.asr += 3
            self.character.items[2] -= 1
            self.olddmg = self.character.damage
            self.oldcrit = self.character.critpercent
            self.olddef = self.character.defense
            print("Administered Adrenaline. Stats buffed for 3 rounds.")
            self.character.damage += 20
            self.character.critpercent += 0.15
            self.character.defense += 15
            self.character.adr = True
            self.inv()     
    def check_adr(self): #Check Adrenaline Shot
        if self.character.asr > 0:
            self.character.asr -= 1
        elif self.character.asr <= 1 and self.character.adr == True:
            self.character.damage = self.character.olddmg
            self.character.critpercent = self.character.oldcrit
            self.character.defense = self.character.olddef
            print("Your Adrenaline Shot has Expired.")
            self.character.adr = False                
##Menus##
    def mainmenu(self): #Main Menu
        try:
            self.prevmenu = "mm"
            print("Tales of Time Main Menu")
            print('Enter "help" for available commands')
            opt = input("What would you like to do?").lower()
            if opt == "help" or opt == "h":
                print("Usage - Keyword\nView Current Character - info\nCreate New Character - newchar" \
                      "\nChange Difficulty - dif\nNew Encounter - fight \nInventory - inv\nShop - n/a")
                self.mainmenu()
            elif opt == "stats" or opt == "s":
                self.info()
                self.mainmenu()
            elif opt == "newchar":
                y = input("This will clear existing character stats. Are you sure you would like to continue?(y/n): ")
                if y == "y":
                    self.charwiz()
                else:
                    print("Request Cancelled.")
                    self.mainmenu()
            elif opt == "save":
                self.save()
                self.mainmenu()
            elif opt == "load":
                self.load()
                self.mainmenu()
            elif opt == "dif":
                self.opponent = None
                self.modify_difficulty()
                self.mainmenu()
            elif opt == "fight" or opt == "f":
                self.newOpponent()
            elif opt == "inv" or opt == "i":
                self.inv()
                self.mainmenu()
            elif opt == "boss":
                self.summon_boss()
                FightGame.current_opponent = self.opponent
                self.fightmenu()
            elif opt == "exit":
                return
            else:
                print("Invalid Option")
                print("Usage - Keyword\nView Current Character - info\nCreate New Character - newchar" \
                      "\nChange Difficulty - dif\nNew Encounter - fight \nInventory - inv\nShop - n/a")
                self.mainmenu()
        except Exception as e:
            print(f"An unexpected error occurred while setting difficulty: {e}")
    def fightmenu(self): #Fight Menu
        self.prevmenu = "fm"
        opt = input("What would you like to do next? (type help for commands):")
        #Player Commands
        if opt == "help":
            print("Command List: \n1) Fight - f\n2)) Run - r\nInventory - i\nStats - s")
            self.fightmenu()
        elif opt == "f" or opt == "fight":
            print("\nAttempting to attack...")
            self.atkround()
        elif opt == "r" or opt == "run":
            print("\nAttempting to flee...")
            self.run()
        elif opt == "i" or opt == "inv":
            self.inv()
            self.fightmenu()
        elif opt == "s":
            self.info()
            self.fightmenu()
        #Debug/Hidden Commands
        elif opt == "exit":
            return
        elif opt == "oppstats":
            self.get_opp_stats()
            self.fightmenu()
        elif opt == "moddif":
            self.modify_difficulty()
            self.set_dif()
            self.fightmenu()
        else:
            print("\nInvalid Input.\nCommands:")
            print("Command List: \n1) Fight - f\n2)) Run - r\nInventory - i\nStats - s")
            self.fightmenu()
##Settings##
    def modify_difficulty(self,lv="x"): #Modifies opponent stats
        if lv == "x":
            print("Difficulty Rates: \n-3 - Reduces Opponent Stats by 50%\n-2 - Reduces Opponent Stats by 25%\n-1 - Reduces Opponent Stats by 10%" \
              "\n 1 - Increases Opponent Stats by 10%\n2 - Increases Opponent Stats by 25%\n3 - Increases Opponent Stats by 50%\nEnter '0' to reset to default")
            lv = int(input('Enter a difficulty value: '))
        if lv == -1:
            mult = 0.90
            print("Difficulty decreased by 10%")
        elif lv == -2:
            mult = 0.75
            print("Difficulty decreased by 25%")
        elif lv == -3:
            mult = 0.50
            print("Difficulty decreased by 50%")
        elif lv == 1:
            mult = 1.10
            print("Difficulty increased by 15%")
        elif lv == 2:
            mult = 1.25
            print("Difficulty increased by 25%")
        elif lv == 3:
            mult = 1.50
            print("Difficulty increased by 50%")
        else:
            mult = 1
        self.character.mult = mult
    def set_dif(self): #Sets opponent stats according to difficulty
        try:
            self.opponent.health *= self.character.mult
            self.opponent.defense *= self.character.mult
            self.opponent.speed *= self.character.mult
            self.opponent.damage *= self.character.mult
        except Exception as e:
            print(f"An unexpected error occurred while setting difficulty: {e}")

    def get_boss(self):
        if self.character.char == "Archer":
            if self.character.kc == 5:
                return Boss_Archer()
        elif self.character.char == "Warrior":
            if self.character.kc == 5:
                return Boss_Warrior()
        elif self.character.char == "Mage":
            if self.character.kc == 5:
                return Boss_Mage()
        else:
            rand = randint(1,3)
            print(rand)
            if rand == 1:
                return Boss_Archer()
            if rand == 2:
                return Boss_Warrior()
            if rand == 3:
                return Boss_Mage()
    def boss_class(self):
        if self.character.kc == 5:
            return True
        else:
            return False
    def info(self): #Displays user stats
        print("The tale of %s:" % self.character.name, 
              "\n\nStats: \nHealth: %.1f/%d\nDefense: %.1f\nSpeed: %.1f\nDamage: %.1f\nCoins: %d\nWins: %d\nRegen (per rd): %d" % (
                  self.character.health,self.character.maxhealth, self.character.defense, self.character.speed,
                  self.character.damage, self.character.coins,self.character.kc,self.character.regen))
##Save/Load##
    def getSaves(self):
        try:
            self.character.savenum = str(input("What save file would you like to overwrite?: "))
            self.fileload = ("character%s.txt" % self.character.savenum)
            fileread = open(self.fileload, "r")
            fileread.close()
        except FileNotFoundError:
            print("Save not found, creating new character file")
            failnum = 0
            fileread = open(self.fileload, "w")
            fileread.close()
        except ValueError:
            self.savenum = 0
    def save(self):
        self.getSaves()
        print("Saving " + self.fileload + "\n")
        file = open(self.fileload, "w")
        try:
            file.write("New Character " + str(int(self.character.savenum)) + ":\n")
        except (NameError, ValueError):
            print("Save id corrupted, new id set to 0")
            self.savenum = 0
            file.write("New Character " + str(int(self.character.savenum)) + ":\n")
        for i in self.character.attr:
            file.write(i + ":" + str(getattr(FightGame.current_character, i)) + "\n")
        print("Saving complete.")
        file.close()
    def load(self):
        try:
            loadnum = input("What load file would you like to access: ")
            self.fileload = ("character%s.txt" % loadnum)
            filein = open(self.fileload, "r")
            header = filein.readline().strip()
            if header.startswith("New Character"):
                num = header.split(":")[0].split()[-1]
            else:
                print("Invalid save file.")
                return
            for line in filein:
                if ":" not in line:
                    continue
                key, value = line.strip().split(":", 1)
                try:
                    parsed_value = literal_eval(value.strip())
                    print("set",key,"to",parsed_value)
                except (ValueError, SyntaxError):
                    parsed_value = value.strip()
                    print("**set",key,"to",parsed_value)
                setattr(FightGame.current_character, key, parsed_value)
            print("**Warning: attribute passed as string. May cause issues if attribute is a literal.**")
            print("Loaded character",num)
        except (ValueError, FileNotFoundError):
            print("Invalid save file.")
            return
##DEBUG##
    def get_opp_stats(self):
        try:
            print("The tale of %s" % self.opponent.name, 
                  "\n\nStats: \nHealth: %.1f\nDefense: %.1f\nSpeed: %.1f\nDamage: %.1f" % (
                      self.opponent.health, self.opponent.defense, self.opponent.speed,
                      self.opponent.damage))
        except Exception as e:        
            print(f"An unexpected error occurred while summoning boss: {e}")
    def summon_boss(self,n=0):
        try:
            if n == 0:
                n = input("What Boss would you like to fight:")
            elif n == "1":
                self.opponent = Boss_Archer()
            elif n == "2":
                self.opponent = Boss_Warrior()
            elif n == "3":
                self.opponent = Boss_Mage()
            else:
                n = input("Invalid Option, try again.")
        except Exception as e:
            print(f"An unexpected error occurred while summoning boss: {e}")
######################Classes#############################
class Character: #Name,Type,HP,Def,Spd,Dmg
    def __init__(self, name="Nomad", chartype="Adventurer", health=100, defense=40, speed=40, damage=40, ranatk=10):
#Type Attributes
        self.name = name
        self.char = chartype
#Stat Attributes
        self.health = health
        self.defense = defense
        self.speed = speed
        self.damage = damage
        self.kc = 0  # Kill count
        self.ranatk = ranatk #Higher Values = Easier hits
        self.critpercent = 1.35 #crit dmg multiplier
        self.maxhealth = 200
        self.critrate = randint(1,10) #crit chance
        self.regen = 0
#Old/Default Values
        self.olddmg = self.damage
        self.oldcrit = self.critpercent
        self.olddef = self.defense
        self.oldcritrate = self.critrate
        self.oldspeed = self.speed
        self.oldranatk = self.ranatk
#Drop Attributes
        self.coins = 0
        self.coinrate = randint(5,25)
        self.items = [0]*3# Medpacks, Go-Juice, Adrenaline Boosters
#Function Attributes
        self.mult = 1
        self.gjr = 0
        self.asr = 0
        self.adr = False
        self.gj = False
        self.isBoss = False
        self.savenum = 0
        self.attr = ["name","char","health","defense","speed","damage" \
            ,"kc","ranatk","critpercent","maxhealth","critrate" \
            ,"regen","coins","coinrate","items","mult","asr","gjr","adr","gj","savenum"]
class Warrior(Character): #Warrior Class => High Health, Low Defense, Moderately Slow, Medium Damage
    def __init__(self, name="Warrior"):
        super().__init__(name, "Warrior", 120, 30, 50, 50,99)
        self.atkmsg = ["\n%s sliced %s dealing %.1f dmg", "\n%s stabbed %s dealing %.1f dmg"]
        self.critpercent = 1.40
class Archer(Character): #Archer Class => Medium Health, Medium Defense, Moderately Fast, Very Low defense 
    def __init__(self, name="Archer"):
        super().__init__(name, "Archer", 120, 50, 70, 30,5) #Archer Class => Medium Health, Medium Defense, High speed, Low damage
        self.atkmsg = ["%s shot an arrow at %s dealing %.1f dmg", "%s pierced %s with an arrow dealing %.1f dmg"]
        self.critpercent = 1.50
        self.maxhealth = 240   
class Mage(Character): #Mage Class => Low Health, High Defense, Very Fast, Medium Damage
    def __init__(self, name="Mage"):
        super().__init__(name, "Mage", 60, 60, 80, 50,7)
        self.atkmsg = ["%s blasted %s with a fireball dealing %.1f dmg", "%s cast a spell on %s dealing %.1f dmg"]
        self.critpercent = 1.40
        self.maxhealth = 120
class Raider(Character): #Raider Class => Low health, low defense, Very fast, High damage, deadly critical strike.
    def __init__(self, name="Raider"):
        super().__init__(name, "Raider", 30,10,90,70,50)
        self.atkmsg = ["%s stealthily stabbed %s dealing %.1f dmg", "%s attacked %s dealing %.1f dmg"]
        self.maxhealth = 100
        self.critpercent = 2.10
        self.critrate = randint(1,15)
        self.coinrate = randint(1,50)
        self.items[1] += 1
        self.items[2] += 1
class Adventurer(Character): #Challenging Class. Medium health, Medium defense, Medium Speed, Medium Damage.
    def __init__(self, name="Adventurer"):
        super().__init__()
        self.atkmsg = ["%s attacked %s dealing %.1f","%s punched %s dealing %.1f dmg"]


##Boss Classes
class Boss_Archer(Character):
    def __init__(self,name="Sharpshooter"):
        super().__init__(name, "Boss_Archer",200,50,110,45,50)
        print("\n(!) Incoming Boss (!)")
        self.atkmsg = ["%s blasted %s with a piercing shot dealing %.1f dmg"]
        self.maxhealth = 300
        self.critpercent = 1.80
        self.regen = 15
        self.isBoss = True
    def fightWin(self):
        FightGame.current_character.maxhealth += 75
        FightGame.current_character.health = FightGame.current_character.maxhealth
        FightGame.current_character.speed += 20
        FightGame.current_character.damage += 20
        FightGame.current_character.coins += 75
        FightGame.current_character.kc += 1
        print("\nYou have defeated the %s!" % self.name)
        print("[+75 Max Health, +20 Max Speed, +20 Max Damage, +75 Coins]")
        for i in range(1,randint(1,5)):
            FightGame.globalself.itemdrop(self.name)
        print("\nYou notice the %s's quiver shimmering..." % self.name)
        y = input("Do you take the quiver for yourself (1) or sell it? (2)")
        if y == "1":
            print("You take the quiver. It seems to pulse in your hand. [Higher Atk Rate, +3 Regen]")
            FightGame.current_character.ranatk = 99
            FightGame.current_character.regen += 3
        else:
            print("You sell the quiver for 250 coins.")
            FightGame.current_character.coins += 250
        FightGame.current_character.opponent = None
        n = input("\nWould you like to fight another opponent? (y/n): ")
        if n == "y":
            FightGame.globalself.newOpponent()
        else:
            FightGame.globalself.mainmenu()
class Boss_Warrior(Character):
    def __init__(self,name="Knight"):
        super().__init__(name, "Boss_Warrior",200,70,90,65,99)
        print("\n(!) Incoming Boss (!)")
        self.atkmsg = ["%s sliced %s with a deadly blade dealing %.1f dmg"]
        self.maxhealth = 300
        self.critpercent = 1.80
        self.regen = 15
        self.isBoss = True
    def fightWin(self):
        FightGame.current_character.maxhealth += 50
        FightGame.current_character.health = FightGame.current_character.maxhealth
        FightGame.current_character.speed += 15
        FightGame.current_character.damage += 15
        FightGame.current_character.coins += 75
        FightGame.current_character.kc += 1
        print("\nYou have defeated the %s!" % self.name)
        print("[+90 Max Health, +15 Max Speed, +15 Max Damage, +75 Coins]")
        for i in range(1,randint(1,7)):
            FightGame.globalself.itemdrop(self.name)
        print("\nYou %s's blade shimmering in the moonlight.." % self.name)
        y = input("Do you take the sword for yourself (1) or sell it? (2)")
        if y == "1":
            print("You take the sword. It seems to pulse in your hand. [+50% critical damage, +3 regen]")
            FightGame.current_character.regen += 2
            FightGame.current_character.critpercent += 0.5
        elif y == "2":
            print("You sell the gem for 250 coins.")
            FightGame.current_character.coins += 250
        else: 
            print("Invalid input.")
            y = input("Do you take the gem for yourself (1) or sell it? (2)")
        FightGame.current_character.opponent = None
        y = input("\nWould you like to fight another opponent? (y/n): ")
        if y == "y":
            FightGame.globalself.newOpponent()
        else:
            FightGame.globalself.mainmenu()
class Boss_Mage(Character):
    def __init__(self,name="Wizard Apprentice"):
        super().__init__(name, "Boss_Mage",150,50,110,70,25)
        print("\n(!) Incoming Boss (!)")
        self.atkmsg = ["%s blasted %s with a magical shot dealing %.1f dmg"]
        self.maxhealth = 300
        self.critpercent = 1.80
        self.regen = 15
        self.isBoss = True
    def fightWin(self):
        FightGame.current_character.maxhealth += 80
        FightGame.current_character.health = FightGame.current_character.maxhealth
        FightGame.current_character.speed += 20
        FightGame.current_character.damage += 10
        FightGame.current_character.coins += 75
        FightGame.current_character.kc += 1
        print("\nYou have defeated the %s!" % self.name)
        print("[+80 Max Health, +20 Max Speed, +10 Max Damage, +75 Coins]")
        for i in range(1,randint(1,5)):
            FightGame.globalself.itemdrop(self.name)
        print("\nYou notice a shiny gem around the %s's neck..." % self.name)
        y = input("Do you take the gem for yourself (1) or sell it? (2)")
        if y == "1":
            print("You take the gem. It seems to pulse in your hand. [+5 regen]")
            FightGame.current_character.regen += 5
            FightGame.current_character.ranatk += 20
        else:
            print("You sell the gem for 250 coins.")
            FightGame.current_character.coins += 250
        FightGame.modify_difficulty(1)
        FightGame.current_character.opponent = None
        y = input("\nWould you like to fight another opponent? (y/n): ")
        if y == "y":
            FightGame.globalself.newOpponent()
        else:
            FightGame.globalself.mainmenu()
        
class Dev(Character):
    def __init__(self,name="Dev"):
        super().__init__(name, "Dev", 999,99,999,999,2)
        self.atkmsg = ["%s rewrote %s's code. Dealing %.1f dmg"]
        self.coinrate = randint(50,500)
try:            
    game = FightGame()
except Exception as e:
    print(f"An unexpected error occurred: {e}")

#To Do:
#Shop
