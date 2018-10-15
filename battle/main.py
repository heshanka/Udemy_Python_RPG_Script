import random

from game import Person, bcolors
from magic import Spell
from inventory import Item


print("\n\n")
#black magic █
fire = Spell("Fire", 25, 600, "black")
thunder = Spell("Thunder", 25, 600, "black")
blizzard = Spell("Blizzard", 25, 600, "black")
meteor = Spell("Meteor", 40, 1200, "black")
quake = Spell("Quake", 14, 140, "black")

#white magic
cure = Spell("Cure", 25, 620, "white")
cura = Spell("Cura", 32, 1500, "white")

potion = Item("Potion", "potion", "Heals 50 HP", 50)
hipotion = Item("Hi-Potion", "potion", "Heals 100 HP", 100)
superpotion = Item("Super Potion", "potion", "Heals 500HP", 500)
elixer = Item("Elixer", "elixer", "Fully restores HP/MP of one party member", 9999)
hielixer = Item("MegaElixer", "elixer", "Fully restores HP/MP of one party member", 9999)

grenade = Item("Grenade", "attack", "Deals 500 damage", 500)

player_spells = [fire, thunder, blizzard, meteor, quake, cure, cura]
player_items = [{"item": potion, "quantity":15}, {"item":hipotion, "quantity":5}, {"item":superpotion, "quantity":5},{"item":elixer, "quantity":5}, {"item":hielixer, "quantity":2}, {"item":grenade, "quantity":5}]

#Instantiate People
player1 = Person("Valos:", 3260, 132, 300, 34, player_spells, player_items)
player2 = Person("Nick: ", 4160, 180, 311, 34, player_spells, player_items)
player3 = Person("Robot:", 3889, 174, 288, 34, player_spells, player_items)
enemy = Person("Magus", 1200, 701, 525, 25, [], [])

players = [player1, player2, player3]



running = True
i=0

print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKS!" + bcolors.ENDC)

while running:
    print("=========================")

    print("\n")
    print("NAME                HP                                                   MP")
    for player in players:
        player.get_stats()

    print("\n")


    for player in players:
        enemy.get_enemy_stats()

        player.choose_action()
        choice = input("    Choose action:")
        index = int(choice) - 1

        if index == 0:
            dmg = player.generate_damage()
            enemy.take_damage(dmg)
            print("You attacked for", dmg, "points of damage. Enemy HP:", enemy.get_hp())
        elif index == 1:
            player.choose_magic()
            magic_choice = int(input("    Choose magic:"))-1

            if magic_choice == -1:
                continue


            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()

            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(bcolors.FAIL + "\nNot enough MP" + bcolors.ENDC)
                continue

            player.reduce_mp(spell.cost)

            if spell.type == "white":
                player.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " heals for", str(magic_dmg), "HP" + bcolors.ENDC)
            if spell.type == "black":
                enemy.take_damage(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " deals", str(magic_dmg), "points of damage" + bcolors.ENDC)


            enemy.take_damage(magic_dmg)
            print(bcolors.OKBLUE + "\n" + spell.name + " deals", str(magic_dmg) + "points of damage" + bcolors.ENDC)

        elif index == 2:
            player.choose_item()
            item_choice = int(input("    Choose item: ")) - 1

            if item_choice == -1:
                continue

            item = player.items[item_choice]["item"]

            if  player.items[item_choice]["quantity"] == 0:
                print(bcolors.FAIL + "\n" + "None left..." + bcolors.ENDC)
                continue
            player.items[item_choice]["quantity"] -= 1


            if item.type == "potion":
                player.heal(item.prop)
                print(bcolors.OKGREEN + "\n" + item.name + "heals for", str(item.prop), "HP" + bcolors.ENDC)
            elif item.type == "elixer":

                if item.name == "MegaElixer":
                    for i in players:
                        i.hp = i.maxhp
                        i.mp = i.maxmp
                print(bcolors.OKGREEN + "\n" + item.name + "fully restores HP/MP", str(item.prop), "HP" + bcolors.ENDC)
            elif item.type == "attack":
                enemy.take_damage(item.prop)
                print(bcolors.FAIL + "\n" + item.name + " deals" + str(item.prop), "points of damage", bcolors.ENDC)

    enemy_choice = 1
    target = random.randrange(0,3)
    enemy_dmg = enemy.generate_damage()

    players[target].take_damage(enemy_dmg)
    print("Enemy attacks for", enemy_dmg)

    if enemy.get_hp() == 0:
        print(bcolors.OKGREEN + "You win!" + bcolors.ENDC)
        running = False
    elif player.get_hp == 0:
        print(bcolors.FAIL + "Your enemy has defeated you!"+ bcolors.ENDC)
        running = False
