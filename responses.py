import random
import math
characters = []

# Character class, takes in player name, character name, race and class as initial parameters
# Players can add stats and proficiencies using other commands
# Class is called cless because calling it class interferes with the class declaration :p


class Character:
    def __init__(self, player: str, name: str, race: str, cless: str, level: str):
        self.player = player
        self.name = name
        self.race = race
        self.cless = cless
        self.stats = []
        self.proficiencies = []
        self.level = level

    # Gives the player stats
    def add_stats(self, stats: list[int]) -> str:
        if len(stats) != 6:
            return "Invalid player stats, must be exactly 6"
        if max(stats) > 28 or min(stats) < 1:
            return "Incorrect player stats. No stat may exceed 28 or be less than 1"

        # If stats have already been added then replace the items in the current list
        if len(self.stats) > 0:
            for i in range(len(stats)):
                self.stats[i] = stats[i]
        else:
            for i in range(len(stats)):
                self.stats.append(stats[i])
        return f"Stats added to character {self.name}"

    # Adds proficiencies to the player characters

    def add_proficiencies(self, proficiency):
        for profic in proficiency:
            self.proficiencies.append(profic)
        return f"Proficiencies added to character {self.name}"

# first determines if the message is a command and then returns a response


def handle_response(message: str) -> str:
    # Make command all lowercase
    p_message = message.lower()

    # Takes the first word of any message sent in chat so it can be checked to see if it is a command
    command = p_message.split()[0]

    # Checks to see if a command has been made
    if command == "!roll":
        return roll(remove_command(p_message))
    elif command == "!randchar":
        return rand_char()
    elif command == "!addchar":
        return add_char(remove_command(p_message))
    elif command == "!getchar":
        return get_char(remove_command(p_message))
    elif command == "!addstats":
        return add_stats(remove_command(p_message))
    elif command == "!getstats":
        return get_stats(remove_command(p_message))
    elif command == "!addprofic":
        return add_profic(remove_command(p_message))
    elif command == "!getprofic":
        return get_profic(remove_command(p_message))
    elif command == "!check":
        return make_check(remove_command(p_message))
    elif command == "!delprofic":
        return remove_profic(remove_command(p_message))
    elif command == "!delchar":
        return remove_char(remove_command(p_message))
    elif command == "!lvlup":
        return level_up(remove_command(p_message))
    elif command == "!help":
        return help()

# Rolls dice
# @param the original message
# @return the result of the roll


def roll(message: str) -> str:
    roll = ""
    try:
        # Split the message by the plus sign to get roll and bonus info
        try:
            roll = message.split("+")[0]
            bonus = int(message.split("+")[1])
        except:
            roll = message
            bonus = 0

        # Split the roll string to get the number and type of die
        number = int(roll.split("d")[0])
        die_type = int(roll.split("d")[1])

    except Exception as e:
        return "Incorrect command. Format is [int]d[int]+[int]"

    # Rolls the dice and sum all rolls
    val = 0
    for i in range(number):
        val += random.randint(1, die_type)

    # Add the bonus
    total = val + bonus

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
        cless = words[3]
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

# Retrieves base character information a message containing the player name


def get_char(message):
    # Runs through the list of characters to find the one being referenced

    for character in characters:
        if character.player == message:
            return f"Character name: {character.name}\nRace: {character.race}\nClass: {character.cless}\nLevel: {character.level}"
    return f"Player {message} not found"

# Adds stats to the player


def add_stats(message):
    try:
        command = get_word(message)
        stats = []

        # Create a list containing only the stats, not the player name
        for i in range(1, len(command)):
            stats.append(int(command[i]))

        player = find_player(command[0])

        if player != "Player not found":
            return player.add_stats(stats)
        else:
            return f"Player {command[0]} not found"

    except Exception as e:
        print(e)
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

    # Put all inputted proficiencies into a list
    for i in range(1, len(words)):
        proficiencies.append(words[i])

    character = find_player(words[0])

    if character == "Player not found":
        return f"Player {words[0]} not found"
    else:
        character.add_proficiencies(proficiencies)
        return f"Proficiencies added to character {character.name}"

# Retrieves player proficiencies


def get_profic(message):
    character = find_player(message)

    answer = f"Proficiencies for character {character.name}:\n"

    # Checks to see if the character exists and then constructs a message to be returned
    if character != "Player not found":
        if len(character.proficiencies) < 1:
            return f"Character {message} does not have any proficiencies"
        for i in character.proficiencies:
            answer = answer + "- " + i + "\n"
    else:
        return f"Player {message} not found"
    return answer

# Removes proficiencies from a character


def remove_profic(message):
    words = get_word(message)
    name = words[0]
    profics = []

    for i in range(1, len(words)):
        profics.append(words[i])

    char = find_player(name)

    if char != "Player not found":
        for i in words:
            for j in range(len(char.proficiencies)):
                if i == char.proficiencies[j]:
                    char.proficiencies.pop(j)
                    break
    else:
        return f"Player {name} not found"

    return f"Proficiencies removed from character {name}"

# Makes a check using a player's proficiencies and ability scores


def make_check(message):
    try:
        words = get_word(message)
        name = words[0]
        skill = words[1]
        character = find_player(name)
        score = 0
        profic = 0

        # Make sure the player exists
        if character == "Player not found":
            return f"Player {name} not found"

        # Make sure the player has stats
        if len(character.stats) == 0:
            return "Must give player stats before making a check"

        # See if the player is proficient in this skill, and get the proficiency bonus from the charcter's level
        if len(character.proficiencies) > 0:
            for i in character.proficiencies:
                if i == skill:
                    profic = math.ceil(character.level / 4) + 1
                    break

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

# Removes a character from the list


def remove_char(name):
    char = find_player(name)
    if char == "Player not found":
        return f"Character {name} could not be found"
    else:
        characters.remove(char)
        return f"Character {name} removed"

# Levels up a character


def level_up(name: str) -> str:
    char = find_player(name)
    if char != "Player not found":
        char.level += 1
        return f"Character {name} leveled up to level {char.level}"
    else:
        return f"Character {name} could not be found."


def help():
    return "A bot for storing D&D character info within the discord chat for quick and easy reference. The bot has the following commands: \n> !roll - Rolls the specified number of dice \n> !randchar - Creates random set of 6 numbers for random character stats \n> !addchar - Adds a character \n> !getchar - Retrieves a character's info \n> !addstats - Adds or modifies to a character's base stats \n> !getstats - Displays a character's stats \n> !addprofic - Adds proficiencies to a character \n> !getprofic - Displays a character's proficiencies \n> !delprofic - Removes a specified proficiency from a character \n> !check - Makes a skill check using a character's stats and proficiencies \n> !delchar - Removes a specified character \n> !lvlup - Levels up a specified character"


# Removes the command portion from the initial message.
def remove_command(message: str) -> str:
    x = message.split()
    x.pop(0)
    new_message = ""
    # Construct a new string starting immediately after the space after the command
    for word in x:
        new_message = new_message + word + " "
    return new_message[:-1]

# Take a string and turn it into a list of individual words


def get_word(message: str):
    return message.split()

# Find a character within the list of characters


def find_player(name: str) -> Character:
    for i in range(len(characters)):
        if characters[i].name == name:
            return characters[i]
    return "Player not found"
