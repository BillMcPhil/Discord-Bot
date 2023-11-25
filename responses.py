from typing import Iterable
import discord
import inspect
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
    # WARNING: This function can return None. Are the prints supposed to be returns?
    def add_stats(self, stats) -> str | None:
        s = []
        if len(stats) == 6:
            for i in range(len(stats)):
                if stats[i] < 28:
                    s.append(stats[i])
                else:
                    print("Invalid player stats, greater than 28")
            self.stats = s
            return f"Stats added to character {self.name}"
        else:
            print("Invalid player stats, more than 6")

    # Adds proficiencies to the player characters @param a list of proficiencies
    def add_proficiencies(self, proficiency: Iterable[str]) -> str:
        self.proficiencies.extend(proficiency)
        return f"Proficiencies added to character {self.name}"
    

# @param message 
# first determines if the message is a command and then @returns a response
# WARNING: This function doesn't return a string when there is not command in the message.
def handle_response(message: str) -> str | None:
    # Make command all lowercase
    p_message = message.lower()
    command_end = message.find(" ")

    # What should 
    if command_end == -1:
        command_end = len(message)

    command = p_message[0:command_end]
    rest = message[command_end:]

    # Make sure we have a proper command on our hands.
    if not command.startswith("!") or len(command) < 2:
        return None
        
    # `handle_response` could lead to players crashing the bot by nesting recursive calls.
    DISALLOWED = ["handle_response", "find_player"]

    # It would be safer to move all the command functions to another module, then use getattr(modulename, command[1:])
    # after `import modulename` to provide better sandboxing.
    delegate = globals().get(command[1:])

    # Make sure the function is a function and not `characters` or something else.
    if delegate is None or not callable(delegate):
        return None

    # Call the function according to parameters
    sig = inspect.signature(delegate)
    match len(sig.parameters):
        case 0:
            return delegate()
        case 1:
            return delegate(rest)
        case _:
            # We should not be calling anything with more than 1 arg.
            return None

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
def randchar():
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
def addchar(message):  
    try:
        words = message.split()
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
    
    # Add the player character to the list and return a confirmation message
    characters.append(char)
    return f"Character {character} has been added"

# Retrieves base character information @param a message containing the player name
def getchar(message):
    #Runs through the list of characters to find the one being referenced
    character = find_player(message)
    for char in characters:
        if char.player == message:
            return f"Character name: {char.name}\nRace: {char.race}\nClass: {char.cless}\nLevel: {char.level}"
    return f"Player {message} not found"
    
# Adds stats to the player
def addstats(message):
    try:
        command = message.split()
        stats = []

        # Create a list containing only the stats, not the player name
        for i in range(1, len(command)):
            stats.append(int(command[i]))

        # Make sure the there are only 6 stats in the list, no more and no less
        if len(stats) != 6:
            return "Incorrect player stats. Must be only 6 stats"
        # Make sure that each stat does not exceed 28
        if max(stats) > 28 or min(stats) < 1:
            return "Incorrect player stats. No stat may exceed 28 or be less than 1"
        
        character = find_player(command[0])
        if character is None:
            return f"Player {command[0]} not found"
        else:
            return character.add_stats(stats)
        
    except Exception as e:
        return "Incorrect command. Command format: !addstats [player name] [STR] [DEX] [CON] [INT] [WIS] [CHA]"

# Retrieve player stats
def getstats(message):
    # Find the referenced character
    character = find_player(message)

    if character is None:
        return f"Player {message} not found"

    return f"STR: {character.stats[0]}\nDEX: {character.stats[1]}\nCON: {character.stats[2]}\nINT: {character.stats[3]}\nWIS: {character.stats[4]}\nCHA: {character.stats[5]}\n"

# Adds proficiencies to a player
def addprofic(message):
    words = message.split()
    proficiencies = []

    # Put all inputted proficiencies into a list
    for word in words[1:]:
        proficiencies.append(word)

    character = find_player(words[0])
    
    if character is None:
        return f"Player {words[0]} not found"
    else:
        character.add_proficiencies(proficiencies)
        return f"Proficiencies added to character {character.name}"

# Retrieves player proficiencies
def getprofic(message):
    character = find_player(message)

    # Checks to see if the character exists
    if character is None:
        return f"Player {message} not found"
        
    # Constructs a message to be returned
    answer = f"Proficiencies for character {character.name}:\n"

    if len(character.proficiencies) < 1:
        return f"Character {message} does not have any proficiencies"

    for i in character.proficiencies:
        answer = answer + "- " + i + "\n"
    return answer

# Removes proficiencies from a character
def removeprofic(message):
    words = message.split()
    name = words[0]
    profics = words[1:]
    
    char = find_player(name)
    
    if char is None:
        return f"Player {name} not found"

    # Only removes first occurence of each proficiency.
    for profic in profics:
        try:
            char.proficiencies.pop(char.proficiencies.index(profic))
        except ValueError:
            # Value wasn't in proficiencies so it couldn't be removed.
            # Fine to continue.
            continue
    return f"Proficiencies removed from character {name}"

# Makes a check using a player's proficiencies and ability scores
def makecheck(message):
    try:
        words = message.split()
        name = words[0]
        skill = words[1]
        character = find_player(name)
        score = 0
        profic = 0

        # Make sure the player exists
        if character is None:
            return f"Player {name} not found"

        # Make sure the player has stats
        if len(character.stats) == 0:
            return "Must give player stats before making a check"

        # See if the player is proficient in this skill, and get the proficiency bonus from the charcter's level
        if len(character.proficiencies) > 0:
            if skill in character.proficiencies:
                profic = math.ceil(character.level / 4) + 1
        
        # Check the skill and apply the applicable stat
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

        # Get the player 
        score = (score - 10) // 2
        roll = random.randint(1, 20)
        bonus = score + profic
        total = roll + bonus
        print(roll, bonus, profic)

        return f"{skill} check for {name}: {roll} + {bonus} = {total}"
    except:
        return "Incorrect command format"

#Removes a character from the list
def removechar(name):
    char = find_player(name)
    if char is None:
        return f"Character {name} could not be found"
    else:
        characters.remove(char)
        return f"Character {name} removed"

# Levels up a character
def levelup(name):
    char = find_player(name)

    if char is None:
        return f"Character {name} could not be found."

    char.level += 1
    return f"Character {name} leveled up to level {char.level}"
    
def help():
    return """A bot for storing D&D character info within the discord chat for
quick and easy reference. The bot has the following commands: 
    > !roll - Rolls the specified number of dice 
    > !randchar - Creates random set of 6 numbers for random character stats 
    > !addchar - Adds a character 
    > !getchar - Retrieves a character's info 
    > !addstats - Adds or modifies to a character's base stats
    > !getstats - Displays a character's stats 
    > !addprofic - Adds proficiencies to a character 
    > !getprofic - Displays a character's proficiencies 
    > !delprofic - Removes a specified proficiency from a character 
    > !check - Makes a skill check using a character's stats and proficiencies 
    > !delchar - Removes a specified character 
    > !lvlup - Levels up a specified character"""

# Find a character within the list of characters
def find_player(name: str) -> Character | None:
    for char in characters:
        if char.name == name:
            return char
    return None
