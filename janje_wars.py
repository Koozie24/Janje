import random
import os
import json

PATH = r'c:\Users\13173\ProgrammingProjects\Janje\save_data.json'

player_inventory = {
    "sirnica": 0,
    "burek": 0,
    "cevapi" : 0,
    "janje" : 0,
    "rakija" : 0
}


store_items = {
    "sirnica": random.randint(10, 100),
    "burek": random.randint(10, 100),
    "cevapi" : random.randint(10, 100),
    "janje" : random.randint(10, 100),
    "rakija" : random.randint(10, 100)
}

#variable to store player cash, starts with 200
player_cash = 200

#day count tracks which iteration of days in game
day_count = 1

#get input from user on length of game
print("Please input number of days the game should last: ")
game_length = int(input())

#gets a save name fromm user and appends ending player cash to save_data.json
def save_game(player_cash):

    print("Please input your name to save your score!")
    save_name = input()

    #check if json file exists and contains data
    if os.path.exists(PATH) and os.path.getsize(PATH) > 0:
        #open and load data to dict
        with open(os.path.join(PATH), 'r') as infile:
           data = json.load(infile)
        
    else:
        data = {}

    data[save_name] = player_cash

    with open(os.path.join(PATH), 'w') as outfile:
        json.dump(data, outfile, indent=4)

#loop through save_data.json to find the highest score and print
def score_check(player_cash):
    with open(os.path.join(PATH), 'r') as openfile:
        
        json_object = json.load(openfile)

        high_score = player_cash

        for i in json_object:
            if (json_object[i] > high_score):
                high_score = json_object[i]

        if (high_score == player_cash):
            print(f'Congratulations! You have the high score of {high_score}')
        else:
            print(f'Good attempt! You got {player_cash} marks! The high score is {high_score} marks!')

#function to current clear screen 
def clear_screen():
    os.system('cls' if os.name == 'nt' else ' clear')

#function parses user inputs and returns inputs
def take_inputs(user_input):
     
    if(user_input == 'quit'):
        return False
    elif(user_input[:3] == 'buy'):
        purchase = user_input.split()
        buy_item(purchase)
    elif(user_input[:4] == 'sell'):
        sale = user_input.split()
        sell_item(sale)
    elif(user_input[:5] == 'drink'):
        drink = user_input.split()
        drink_rakija(drink)
    elif(user_input[:4] == 'next'):
        global day_count
        global game_length
        day_count += 1
        change_day()
        if(day_count == game_length):
            print("Today is the final day!")
        if(day_count > game_length):
            save_game(player_cash)
            score_check(player_cash)
            print(f'Your ending number of marks is: {player_cash}!')
            if (player_cash < 200):
                print("OOOF! Looks like you lost pare!")
            else:
                profit = player_cash - 200
                print(f'Congrats! You made {profit} in profit!')
            exit(1)

#function to handle purchasing logic
def buy_item(buy_input):

    if(len(buy_input) == 3):
        global player_cash
        buy_name = buy_input[1]

        #try to convert argument to int
        try:
            buy_amount = int(buy_input[2])
        except ValueError:
            print("Sorry, doesnt look like you input that correct [buy] [item_name] [quantity]")
            return
        
        
        #check if input purchase is in store_items dict
        if buy_name in store_items:
            #calculate cost of purchase
            buy_cost = buy_amount * store_items[buy_name]
            ##check if total cost < amount player has
            if(buy_cost <= player_cash):
                #clear current screen
                clear_screen()
                #update inventory and cash
                player_inventory[buy_name] += buy_amount
                player_cash -= buy_cost
               
                printer()
                print(f'Ti imas {buy_amount} vise {buy_name}')
                
            else:
                print("Izvini. Ne imas dovonjo marks. ")
                print("")
    else:
        print("Not a valid buy input, try again. [buy][item][quantity]")
        print("")


#function to handle sale logic
def sell_item(sale_input):

    if(len(sale_input) == 3):
        global player_cash
        sell_name = sale_input[1]
        
        #try to convert input to int
        try:
            sell_amount = int(sale_input[2])
        except ValueError:
            print("Sorry doesnt look like you input that correctly [sell] [item_name] [quantity]")
            return
        
        if sell_name in store_items:
            #calculate cost
            if(player_inventory[sell_name] >= sell_amount):
                clear_screen()
                sell_cost = store_items[sell_name] * sell_amount
                #update inventory and cash
                player_cash += sell_cost
                player_inventory[sell_name] -= sell_amount

                printer()
                print(f'Ti imas {sell_amount} manje {sell_name}')
              
            else:
                print(f'Izvini. Ne imas dovonjo {sell_name}.')


    else:
        print("Not a valid sale input, try again.")
        print("")

#function to change update day and items for sale 
def change_day():
    global day_count
    global store_items

    for item in store_items:
        store_items[item] = random.randint(10, 100)
    clear_screen()
    printer()

#function to display screen 
def printer():
    global day_count
    print("Commands: buy, sell, next, quit. [commnand] [item_name] [quantity] or drink [drink] [quantity]")
    print(f'Items for Sale (Day {day_count}): ')
    print("------------------")
    for key, value in store_items.items():
        print(f'{key} : ${value}')
    print("")
    print("Player Inventory: ")
    print("------------------")
    for key, value in player_inventory.items():
        print(f'{key} : {value}')
    print("")
    print(f'You currently have ${player_cash} marks')
    print("")


#gambling function for drink [number] command
#takes a bet of count input of rakija. picks a random number 0 - 99 if even, player wins. player will win a random num of janje from 2 to drink bet * 2
#reverse if player loses. subtract janje count from 1 to drinks * 2
def drink_rakija(drink):

    if (len(drink) == 2):
        how_drunk = int(drink[1])
        janje_count = player_inventory['janje']
        if (how_drunk <= player_inventory["rakija"] and (janje_count >= 1)):
            player_inventory["rakija"] -= how_drunk

            chance = random.randint(0, 99)
            if(chance % 2 == 0):
                janje_winnings = random.randint(2, how_drunk*2)
                player_inventory["janje"] += janje_winnings
                janje_count += janje_winnings
                clear_screen()
                printer()
                print("Ti pies pivo sa jaranje! You win janje!")
                print(f'You won {janje_winnings} janje!')
                print(f'You now have {janje_count} janje')
            else:
                janje_loss = random.randint(1, janje_count)
                player_inventory["janje"] -= janje_loss
                janje_count -= janje_loss
                clear_screen()
                printer()
                print("Ti si pian, you lost your bet.")
                print(f'You lost: {janje_loss} janje')
                print(f'You now have {janje_count} janje')
    else:
        print("Not a valid input. To drink rakija: [drink][quantity]")


printer()

#create a loop
while True:
    #get user input
    user_input = input()

    #call function to parse inputs
    store_input = take_inputs(user_input)
    #check if quit input
    if(store_input == False):
        break
    
    