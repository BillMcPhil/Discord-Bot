import random
import math
characters = []

# Character class, takes in player name, character name, race and class as initial parameters
# Players can add stats and proficiencies using other commands
class Character:
    def __init__(self, player, name, race, cless, level):
        self.player = player
        self.name = name
        self.race = race
        self.cless = cless
        self.stats = []
        self.proficiencies = []
        self.level = level

    # Gives the player stats @param a list of stats
    def add_stats(self, stats):
        if len(stats) == 6:
            for i in range(len(stats)):
                if stats[i] < 28:
                    self.stats.append(stats[i])
                else:
                    print("Invalid player stats, greater than 28")
            return f"Stats added to character {self.name}"
        else:
            print("Invalid player stats, more than 6")

    # Adds proficiencies to the player characters @param a list of proficiencies
    def add_proficiencies(self, proficiency):
        for profic in proficiency:
            self.proficiencies.append(profic)
        return f"Proficiencies added to character {self.name}"
    

# @param message 
# first determines if the message is a command and then @returns a response
def handle_response(message) -> str:
    #Make command all lowercase
    p_message = message.lower()

    command = ""

    #Takes the first word of any message sent in chat so it can be checked to see if it is a command
    for char in p_message:
        if char != " ":
            command = command + char
        else:
            break
    
    # Checks to see if a command has been made
    if command == "!roll":
        return roll(remove_command(p_message, 6))
    elif command == "!randchar":
        return rand_char()
    elif command == "!addchar":
        return add_char(remove_command(p_message, 9))
    elif command == "!getchar":
        return get_char(remove_command(p_message, 9))
    elif command == "!addstats":
        return add_stats(remove_command(p_message, 10))
    elif command == "!getstats":
        return get_stats(remove_command(p_message, 10))
    elif command == "!addprofic":
        return add_profic(remove_command(p_message, 11))
    elif command == "!getprofic":
        return get_profic(remove_command(p_message, 11))
    elif command == "!check":
        return make_check(remove_command(p_message, 7))
    elif command == "!delprofic":
        return remove_profic(remove_command(p_message, 11))

# Rolls dice
# @param the original message
# @return the result of the roll
def roll(message):
    number = ""
    dice = ""
    bonus = ""
    index = 1

    # Gets the number of dice requested
    for i in range(len(message)):
        if message[i] != "d":
            number = number + message[i]
            index += 1
            # Checks to see if the number of dice being requested is too much
            if index > 3:
                return "Incorrect Command: number of dice must be lower than 100"
        else:
            break

    # Gets the type of dice being rolled
    for i in range(index, len(message)):
        if message[i] != "+" and message [i] != "-":
            dice = dice + message[i]
            index += 1
        else:
            break

    # Get the bonus value
    for i in range(index, len(message)):
        bonus = bonus + message[i]
    


    # Converts both the number of dice, type of dice, and bonus into integers, 
    # or if they cannot be turned into integers the command is incorrect and returns an error
    try:
        number = int(number)
    except Exception as e:
        return "Incorrect Command: Must have an integer as the number of dice (Command format: !roll [int]d[int]+[int])"
    
    try:
        dice = int(dice)
    except Exception as e:
        return "Incorrect Command. Dice type must be an integer. (Command format: !roll [int]d[int]+[int])"

    if bonus != "":
        try:
            bonus = int(bonus)
        except Exception as e:
            return "Incorrect Command. Bonus must be an integer with no spaces before the + or -. (Command format: !roll [int]d[int]+[int])"
    else: bonus = 0
    

    # Rolls the dice and collects each die roll into a list
    roll = []
    for i in range(number):
        num = random.randint(1, dice)
        roll.append(num)

    total = sum(roll) + bonus

    # Returns the result of the roll
    return f"Rolls: {roll} + {bonus}. Total: {total}"

# Returns random stats for a character
def rand_char():
    stats = []
    # Generates stats and adds the stats to a list
    for i in range(6):
        rolls = []
        # Creates random individual stats based on the following rules:
        # Roll 4d6, re-roll 1s, drop lowest
        while len(rolls) < 4:
            roll = random.randint(1, 6)

            # Re-roll ones
            if roll == 1:
                continue
            else:
                rolls.append(roll)
        
        # Drop lowest roll, then sum all three rolls together to get stats
        rolls.remove(min(rolls))
        stats.append(sum(rolls))

    # Returns stats. Looks terrible in code but outputs are nice and formatted
    return f"STR: {stats[0]}\nDEX: {stats[1]}\nCON: {stats[2]}\nINT: {stats[3]}\nWIS: {stats[4]}\nCHA: {stats[5]}"\
    
# Adds a player and their associated character to a list, @return a confirmation message
def add_char(message):  
    try:
        words = get_word(message)
        name = words[0]
        character = words[1]
        race = words[2]
        cless= words[3]
        level = words[4]
    except Exception as e:
        return "Incorrect command"
    
    # Change the input for the level from a string to an int
    try:
        level = int(level)
        if level > 20 or level < 1:
            return "Level value must be an integer between 1 and 20"
    except Exception as e:
        return "Level value must be an integer between 1 and 20"
    
    char = Character(name, character, race, cless, level)

    characters.append(char)
    
    # Add the player character to the list and return a confirmation message
    return f"Character {character} has been added"

# Retrieves base character information @param a message containing the player name
def get_char(message):
    #Runs through the list of characters to find the one being referenced
    for i in range(len(characters)):
        if characters[i].player == message:
            character = characters[i]
            return f"Character name: {character.name}\nRace: {character.race}\nClass: {character.cless}"
    return f"Player {message} not found"
    
# Adds stats to the player
def add_stats(message):
    try:
        command = get_word(message)
        stats = []

        # Create a list containing only the stats, not the player name
        for i in range(1, len(command)):
            stats.append(int(command[i]))

        #   Make sure the there are only 6 stats in the list, no more and no less
        if len(stats) != 6:
            return "Incorrect player stats. Must be only 6 stats"
        # Make sure that each stat does not exceed 28
        if max(stats) > 28 or min(stats) < 3:
            return "Incorrect player stats. No stat may exceed 28 or be less than 3"
        
        character = find_player(command[0])

        if character != "Player not found":
            return character.add_stats(stats)
        else:
            return f"Player {command[0]} not found"
        
    except Exception as e:
        return "Incorrect command. Command format: !addstats [player name] [STR] [DEX] [CON] [INT] [WIS] [CHA]"

# Retrieve player stats
def get_stats(message):
    # Find the referenced character
    character = find_player(message)

    if character != "Player not found":
        return f"STR: {character.stats[0]}\nDEX: {character.stats[1]}\nCON: {character.stats[2]}\nINT: {character.stats[3]}\nWIS: {character.stats[4]}\nCHA: {character.stats[5]}\n"
    else:
        return f"Player {message} not found"

# Adds proficiencies to a player
def add_profic(message):
    words = get_word(message)
    proficiencies = []

    for i in range(1, len(words)):
        proficiencies.append(words[i])

    character = find_player(words[0])
    
    if character == "Player not found":
        return f"Player {words[0]} not found"
    else:
        character.add_proficiencies(proficiencies)
        return f"Proficiencies added to character {character.name}"

#Retrieves player proficiencies
def get_profic(message):
    character = find_player(message)

    if len(character.proficiencies) < 1:
        return f"Character {message} does not have any proficiencies"

    answer = f"Proficiencies for character {character.name}:\n"

    if character != "Player not found":
        for i in character.proficiencies:
            answer = answer + "- " + i
            answer = answer + "\n"
    else:
        return f"Player {message} not found"
    return answer

def remove_profic(message):
    words = get_word(message)
    name = words[0]
    profics = []
    
    for i in range(1, len(words)):
        profics.append(words[i])
    
    char = find_player(name)
    
    for i in words:
        for j in range(len(char.proficiencies)):
            if i == char.proficiencies[j]:
                char.proficiencies.pop(j)
                break
    
    return f"Proficiencies removed from character {name}"

#Makes a check using a player's proficiencies and ability scores
def make_check(message):
    words = get_word(message)
    name = words[0]
    skill = words[1]
    character = find_player(name)
    score = 0
    profic = 0

    if character == "Player not found":
        return f"Player {name} not found"

    if len(character.stats) == 0:
        return "Must give player stats before making a check"

    if len(character.proficiencies) > 0:
        for i in character.proficiencies:
            if i == skill:
                profic = math.ceil(character.level / 4) + 1
                break
    
    if skill == "acrobatics" or skill == "sleight" or skill == "stealth":
        score = character.stats[1]
    elif skill == "athletics":
        score = character.stats[0]
    elif skill == "arcana" or skill == "history" or skill == "investigation" or skill == "nature" or skill == "religion":
        score = character.stats[3]
    elif skill == "animal" or skill == "insight" or skill == "medicine" or skill == "perception" or skill == "survival":
        score = character.stats[4]
    elif skill == "deception" or skill == "intimidation" or skill == "performance" or skill == "persuasion":
        score = character.stats[5]
    else:
        return "Skill does not exist"

    score = (score - 10) // 2

    roll = random.randint(1, 20)
    bonus = score + profic
    total = roll + bonus
    print(roll, bonus, profic)

    return f"{skill} check for {name}: {roll} + {bonus} = {total}"
    

# Removes the command portion from the initial message. 
# @param the message to remove the command from and the character length of the specific command (plus the space after the command)
# @return a new message without the command portion
def remove_command(message, command_length):
    new_message = ""
    # Construct a new string starting immediately after the space after the command
    for i in range(command_length, len(message)):
        new_message = new_message + message[i]
    return new_message

# Take a string and turn it into a list of individual words
def get_word(message):
    words = []
    word = ""
    #Loop through the message
    for i in range(len(message)):
        # Constructs a word character by character until it runs into a space, 
        # At which point it adds the word into the list and moves onto the next word
        if message[i] != " ":
            word = word + message[i]
        else:
            words.append(word)
            word = ""
    words.append(word)

    return words

def find_player(name):
    for i in range(len(characters)):
        if characters[i].name == name:
            return characters[i]
    return "Player not found"
    





    