
# LFGbot

LFGbot is a basic Discord starboard bot.

## Features

- Monitors all channels and threads for reactions.
- Reposts messages to a specified channel when they receive a defined number of reactions.
- Ignores reactions from the message author.
- Ignores reactions in the target reposting channel.
- Reposts include a permalink to the original message and the message content in a block quote.

## Requirements

- Python 3.7+
- `discord.py` library
- `logging` library
- `asyncio` library

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/HighlightBot.git
   cd HighlightBot
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
   python highlight_bot.py
   ```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.