import discord
import logging
import asyncio
import json
import os

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Your bot's token
TOKEN = 'token-placeholder'

# The ID of the channel where the message will be reposted
TARGET_CHANNEL_ID = channel-id-placeholder

# Number of reactions to trigger repost
REACTION_THRESHOLD = 3

# File to store reposted message IDs
REPOSTED_MESSAGES_FILE = 'reposted_messages.json'

# Set to keep track of reposted message IDs
reposted_messages = set()
# Lock to handle concurrent access to reposted_messages
repost_lock = asyncio.Lock()

def save_reposted_messages():
    try:
        with open(REPOSTED_MESSAGES_FILE, 'w') as f:
            json.dump(list(reposted_messages), f)
        logging.info(f"Successfully saved {len(reposted_messages)} reposted message IDs to {REPOSTED_MESSAGES_FILE}.")
    except IOError as e:
        logging.error(f"IOError while saving reposted messages to {REPOSTED_MESSAGES_FILE}: {e}")
    except json.JSONEncodeError as e:
        logging.error(f"JSON encoding error while saving reposted messages: {e}")
    except Exception as e:
        logging.error(f"Unexpected error while saving reposted messages: {e}")
    else:
        logging.debug(f"Reposted messages saved successfully. Current count: {len(reposted_messages)}")

def load_reposted_messages():
    global reposted_messages
    try:
        if os.path.exists(REPOSTED_MESSAGES_FILE):
            with open(REPOSTED_MESSAGES_FILE, 'r') as f:
                reposted_messages = set(json.load(f))
            logging.info(f"Loaded {len(reposted_messages)} reposted message IDs from {REPOSTED_MESSAGES_FILE}.")
        else:
            logging.info(f"Reposted messages file not found. Starting with an empty set.")
            reposted_messages = set()
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON from {REPOSTED_MESSAGES_FILE}: {e}. Starting with an empty set.")
        reposted_messages = set()
    except Exception as e:
        logging.error(f"Unexpected error loading reposted messages: {e}. Starting with an empty set.")
        reposted_messages = set()

# Load reposted messages from file
load_reposted_messages()

class MyClient(discord.Client):
    async def on_ready(self):
        logging.info(f'Logged in as {self.user}')
        logging.info(f'Monitoring threads and channels for reactions')

    async def on_raw_reaction_add(self, payload):
        async with repost_lock:
            try:
                logging.debug(f'Reaction added: {payload.emoji} in channel {payload.channel_id} for message {payload.message_id}')

                # Ignore reactions in the target reposting channel
                if payload.channel_id == TARGET_CHANNEL_ID:
                    logging.debug(f'Ignoring reaction in target reposting channel.')
                    return

                # Get the channel or thread
                channel = self.get_channel(payload.channel_id) or await self.fetch_channel(payload.channel_id)
                logging.debug(f'Fetched channel: {channel}')

                message = await channel.fetch_message(payload.message_id)
                logging.debug(f'Fetched message: {message.content} by {message.author}')

                # Ignore reactions from the message author
                if message.author.id == payload.user_id:
                    logging.debug(f'Ignoring reaction from message author.')
                    return

                # Check if the message has already been reposted
                if message.id in reposted_messages:
                    logging.debug(f'Message {message.id} has already been reposted. Skipping.')
                    return

                # Count total number of valid reactions
                total_reactions = sum(reaction.count for reaction in message.reactions if reaction.count > 1)
                logging.debug(f'Total valid reactions on message: {total_reactions}')

                if total_reactions >= REACTION_THRESHOLD:
                    target_channel = self.get_channel(TARGET_CHANNEL_ID)
                    logging.debug(f'Target channel: {target_channel}')

                    # Generate the permalink
                    guild = message.guild
                    permalink = f"https://discord.com/channels/{guild.id}/{channel.id}/{message.id}"

                    repost_content = f"{permalink}\n**New highlight from {message.author.mention}:**\n> {message.content}\n"

                    if message.attachments:
                        logging.debug(f'Message has attachments: {message.attachments}')
                        for attachment in message.attachments:
                            await target_channel.send(repost_content)
                            await target_channel.send(file=await attachment.to_file())
                    else:
                        await target_channel.send(repost_content)
                    
                    logging.info(f'Message reposted to {target_channel.name}')
                    
                    # Add message ID to reposted_messages set
                    reposted_messages.add(message.id)
                    # Save updated reposted_messages to file
                    save_reposted_messages()
                else:
                    logging.debug(f'Not enough valid reactions on message: {total_reactions}')

            except Exception as e:
                logging.error(f'Error processing reaction: {e}')

intents = discord.Intents.default()
intents.reactions = True
intents.messages = True
intents.guilds = True
intents.message_content = True


client = MyClient(intents=intents)
client.run(TOKEN)
