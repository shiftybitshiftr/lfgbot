
# LFGbot

stupid simple starboard bot for discord

![image](https://github.com/shiftybitshiftr/lfgbot/assets/13820335/cc261d14-43bf-437d-a1e1-1d5b776a6a82)

## Features

- Monitors all channels and threads for reactions.
- Reposts messages to a specified channel when they receive a defined number of reactions.
- Ignores reactions from the message author.
- Ignores reactions in the target reposting channel.
- Reposts include a permalink to the original message and the message content in a block quote.
- Reuploads message attachments.

## Requirements

- Python 3.7+
- `discord` library
- `logging` library
- `asyncio` library

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/shiftybitshiftr/lfgbot.git
   cd LFGBot
   ```

2. Create a virtual environment and activate it:
   ```sh
   python -m venv botenv
   source botenv/bin/activate  # On Windows use `botenv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```sh
   pip install discord.py
   ```

## Configuration

1. Replace `token-placeholder` with your actual bot OAuth token in the script.
2. Replace `channel-id-placeholder` with the ID of the channel where the messages should be reposted.

## Running the Bot

1. Activate the virtual environment if not already activated:
   ```sh
   source botenv/bin/activate  # On Windows use `botenv\Scripts\activate`
   ```

2. Run the bot:
   ```sh
   python lfgbot.py
   ```

![image](https://github.com/shiftybitshiftr/lfgbot/assets/13820335/ea567595-653c-4bdb-89c8-16f09d8f66eb)



