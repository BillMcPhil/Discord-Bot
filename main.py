import bot

# Only run discord bot when run with `python main.py` not on import
# such as `import main`
if __name__ == "__main__":
    TOKEN = "" # Your token here
    if TOKEN:
        bot.run_discord_bot(TOKEN)
    else:
        print("Please supply a token in `main.py`")

