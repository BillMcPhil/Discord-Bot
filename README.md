# Setup
### Part 1 - Discord Configuration
You're going to need a discord API key. To get one get on Discord and open up
settings. Next click on "Advanced" and turn on "Developer Mode" if it isn't
already on. 

Then go to https://discord.com/developers/applications/, and click "New
Application". Choose whatever name you want ("D&D Bot" is a decent choice). Go
to the "Bot" tab and  click "Reset Token" to get a new token, and **make sure
you save it** (otherwise you'll need to get another).

### Part 2 - Download Code and Libraries
Have a recent version of python installed. You will need the `discord.py`.
Install it in a virtualenv if you know how otherwise just run the `pip install
discord` below.

```bash
git clone https://github.com/BillMcPhil/DnD-Discord-Bot.git
pip install discord
```

### Part 3 - Running
Open up `main.py` and replace `<YOUR TOKEN HERE>` with your Bot's token.

Then run normally, no env variables or program args necessary:

```bash
python main.py
```

# DnD-Discord-Bot
A bot for storing D&D character info within the discord chat for quick and easy
reference. The bot has the following commands:
>!roll [int]d[int]+[int]- Rolls the specified number of dice
>
>!randchar - Creates random set of 6 numbers for random character stats
>
>!addchar [player] [character name] [race] [class] [level]- Adds a character
>
>!getchar [character] - Retrieves a character's info
>
>!addstats [character] [int]x6 - Adds or modifies to a character's base stats. Individual stats must be between 1 and 28
>
>!getstats [character] - Displays a character's stats
>
>!addprofic [character] [proficiency] - Adds proficiencies to a character
>
>!getprofic [character] - Displays a character's proficiencies
>
>!delprofic [character] [proficiency] - Removes a specified proficiency from a character
>
>!check [character] [ability] - Makes a skill check using a character's stats and proficiencies
>
>!delchar [character] - Removes a specified character
>
>!lvlup [character] - Levels up a specified character
>
>!help - Displays available commands
