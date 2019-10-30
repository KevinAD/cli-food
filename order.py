#!/usr/bin/python3
import sys
#print = sys.stdout.write
from pyparsing import *
import random
import time
import os

################################ ESCAPE CODES ###############################


ESC = Literal('\x1b')
integer = Word(nums)
escapeSeq = Combine(ESC + '[' + Optional(delimitedList(integer,';')) +
                oneOf(list(alphas)))

nonAnsiString = lambda s : Suppress(escapeSeq).transformString(s)

colors = {
"beige":222,
"yellow":226,
"brown":94,
"light red":196,
"red":160,
"dark red":124,
"light green":120,
"green":82,
"dark green":28,
"white":255,
"orange":208,
"light yellow":229,
}
ESCAPE = "\u001b["
COL_ESCAPE = ESCAPE+"38;5;"

def get_color_code(color):
    if(color == "reset"):
        return ESCAPE+"0m"
    return COL_ESCAPE + str(colors[color]) +"m"

def set_color(color):
    if(color == "reset"):
        reset_color()
    print(get_color_code(color))

def reset_color():
    print(ESCAPE+"0m")
################################# ASCII ART #################################

################## misc ##################
ice = (" ","□")

################# borger #################
burger_ingredients_art = {
"bun_top":("beige","""   _______________________
 /                         \\
|___________________________|    BUN"""),
"cheese":("yellow","-----------------------------    CHEESE"),
"lettuce":("green","~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    LETTUCE"),
"patty":("brown","▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓    PATTY"),
"tomato":("light red","⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗⌗    TOMATO"),
"pickles":("dark green","/\\/\\/\\/\\    /\\/\\/\\/\\   /\\/\\/\\    PICKLES"),
"bacon":("dark red","""'._.-'-._.-._.-''-..''._.-'-.    BACON"""),
"bun_bottom":("beige","""-----------------------------    BUN
\\___________________________/""")
}

################# drinks ################
drinks = {
"small":"""         //
        //
-------------
|{0}~~~~~~~~~~~{3}|
 \\{0}{1:^9}{3}/
  | {2}  {2}  |
  |_______|""",
"medium":"""         //
        //
       //
--------------
|{0}~~~~~~~~~~~~{3}|
| {0}{1:^10}{3} |
 \\    {2}     /
  |      {2} |
  | {2}      |
  |________|""",
"large":"""         //
        //
       //
--------------
|            |
|{0}~~~~~~~~~~~~{3}|
| {0}{1:^10}{3} |
|   {2}      {2} |
 \\     {2}    /
  |{2}     {2} |
  |   {2}    |
  | {2}   {2}  |
  |________|"""
}
############################### FOOD Config ################################
drink_colors = {"water":"white","coke":"brown","diet-coke":"brown","fanta":"orange","root beer":"brown","sprite":"white","dr.pepper":"brown","lemonade":"light yellow","mtn dew":"light green"}
drink_flavors = list(drink_colors.keys())
drink_sizes = list(drinks.keys())
burger_toppings = list(burger_ingredients_art.keys())
############################### MULTI_STRING ################################
def multi_string(*argv,padding=0):
    '''
    Combines multiple strings while accounting for newline characters
    '''

    rstring = ""
    #Casting to list to make it a bit easier
    strings = list(argv)
    running = [1] * len(strings) #All strings currently have data left
    strings = [text.split('\n') for text in strings] #split each string into lines
    lengths = [get_max_length(text) for text in strings] #Get maximum length for each line

    #For every line
    total_lines = (max([len(text) for text in strings]))

    for line_index in range(total_lines):


        for string_index, text in enumerate(strings):
            line = "" #Empty line
            line_offset = total_lines-len(text)
            new_line_index = line_index - line_offset

            if(len(text) > new_line_index and new_line_index >= 0):
                line += text[new_line_index] #add line from string if it exists

            #fill the rest with spaces
            line += (" " * (lengths[string_index] - len(nonAnsiString(line)))) + get_color_code("reset")

            #print line
            rstring += line + (" "*padding)
        rstring += "\n" #This is the same as print("") but I think this makes more sense

    return rstring
############################ MAX LENGTH #############################
def get_max_length(text):
    return max([len(nonAnsiString(line)) for line in text])

############################### FOOD FUNCS ################################
def burger_string(modifications = []):
    new_burger = ["bun_top","tomato","lettuce","pickles","cheese","patty","bun_bottom"]
    for order,ingredients in modifications:
        if(order.lower() == "custom"):
            new_burger = ["bun_top"] + ingredients + ["bun_bottom"]
        elif(order.lower() == "extra" or order.lower() == "add"):
            for ingredient in ingredients:
                if(ingredient in new_burger):
                    ingredient_index = new_burger.index(ingredient)
                    new_burger.insert(ingredient_index,ingredient)
                else:
                    if(new_burger[0] == "bun_top"):
                        new_burger.insert(1,ingredient)
                    else:
                        new_burger = [ingredient]+new_burger
        elif(order.lower() == "exclude" or order.lower() == "no"):
            for ingredient in ingredients:
                while(ingredient in new_burger):
                    new_burger.remove(ingredient)
    burger_string = []
    for ingredient in new_burger:
        color,ingredient_art = burger_ingredients_art[ingredient]
        burger_string += [get_color_code(color)+line+get_color_code("reset") for line in ingredient_art.split("\n")]
    return "\n".join(burger_string)

def drink_string(size,flavor,has_ice = True):
    return drinks[size].format(get_color_code(drink_colors[flavor]),flavor,ice[int(has_ice)],get_color_code("reset"))

###############################  CLI ################################
if len(sys.argv)  == 1 or sys.argv[1] == "--help" or sys.argv[1] == "-h":
    print("CLI FOOD 1.1 - Kevin Dorland")
    print(f"USAGE:   {sys.argv[0]} [options] [-food item] [food options]")
    print("""

OPTIONS
\t-l\t--list [toppings,flavors,sizes] \t Lists options for given category

FOOD ITEMS
\t-b\t--burger\tAdds a burger item to food order
\t-d\t--drink \tAdds a drink item to food order

BURGER OPTIONS
\tCUSTOM=[toppings] \t Removes all toppings, replaces them with custom list

\tRANDOM=[count]    \t Removes all toppings, replaces them with specified number of random toppings

\tEXCLUDE=[toppings]\t Removes all occurrences of listed toppings
\t     NO=[toppings]

\tEXTRA=[toppings]\t Adds listed toppings to burger
\t  ADD=[toppings]

DRINK OPTIONS
\tSIZE=[size]                  \t Sets size of drink

\tFLAVOR=[flavor]              \t Sets flavor of drink

\tICE=[yes,no]                 \t Sets ice value of drink

\tRANDOM=[size,flavor,ice,all] \t Randomizes given field
    """)

    print(f"EXAMPLE: {sys.argv[0]} --burger NO=pickles,tomato --drink FLAVOR=coke")
    exit()
elif sys.argv[1] == "--list" or sys.argv[1] == "-l":
    if(len(sys.argv) <= 2):
        print("No argument supplied for list...")
        print("Options: toppings, flavors, sizes")
        exit()
    elif sys.argv[2] == "toppings":
        for topping in burger_toppings: print(topping)
        exit()
    elif sys.argv[2] == "flavors":
        for flavor in drink_flavors: print(flavor)
        exit()
    elif sys.argv[2] == "sizes":
        for size in drink_sizes: print(size)
        exit()
    else:
        print(f"list argument {sys.argv[2]} not recognized.")
        exit()
else:
    food_order = []
    current_item = None
    args = sys.argv[1:]
    #print("Args:",args)
    while len(args) > 0:
        current_arg = args.pop(0)
        #print("Current arg:",current_arg)
        if(current_arg == "-b" or current_arg == "--burger"):
            if current_item != None:
                food_order.append(current_item)
            current_item = ["burger",[]]
        elif(current_arg == "-d" or current_arg == "--drink"):
            if current_item != None:
                food_order.append(current_item)
            current_item = ["drink","medium",None,True]
        elif(current_item != None and current_item[0] == "burger"):
            if("=" in current_arg):
                var,val = current_arg.split("=")
                if(var.upper() in ("CUSTOM","EXTRA","ADD","EXCLUDE","NO","RANDOM")):
                    modification = [var,[]]
                    if(var.upper() == "RANDOM"):
                        modification[0] = "CUSTOM"
                        for _ in range(int(val)):
                            modification[1].append(random.choice([t for t in burger_toppings if "bun" not in t]))
                    else:
                        for topping in val.split(","):
                            if topping not in burger_toppings:
                                print(f"Invalid topping {topping}")
                                exit()
                            else:
                                modification[1].append(topping)
                    current_item[1].append(modification[:])
                else:
                    print(f"Invalid argument supplied {current_arg}")

            else:
                print(f"Invalid argument supplied {current_arg}")
        elif(current_item != None and current_item[0] == "drink"):
            if("=" in current_arg):
                var,val = current_arg.split("=")
                if(var.upper() == "SIZE" and val in drink_sizes):
                   current_item[1] = val
                elif(var.upper() == "FLAVOR" and val in drink_flavors):
                   current_item[2] = val
                elif(var.upper() == "ICE" and val.lower() in ("yes","no","true","false")):
                   current_item[3] = (val.lower() in ("yes","true"))
                elif(var.upper() == "RANDOM" and val.lower() in ("size","flavor","ice","all")):
                    if(val.lower() == "size" or val.lower() == "all"):
                        current_item[1] = random.choice(drink_sizes)
                    if(val.lower() == "flavor" or val.lower() == "all"):
                        current_item[2] = random.choice(drink_flavors)
                    if(val.lower() == "ice" or val.lower() == "all"):
                        current_item[3] = random.choice((True,False))
                else:
                    print(f"Invalid argument supplied {current_arg}")

            else:
                print(f"Invalid argument supplied {current_arg}")
    if current_item != None:
        food_order.append(current_item)

############################### MAIN ################################

#print(food_order)

order_strings = []

for food_item in food_order:
    if food_item[0] == "burger":
        order_strings.append(burger_string(food_item[1]))
    elif food_item[0] == "drink":
        if(food_item[2] == None):
            print("Invalid drink flavor: None")
            exit()
        order_strings.append(drink_string(*food_item[1:]))

print(multi_string(*order_strings,padding=5))
