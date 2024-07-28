import logging
from telethon import TelegramClient, events
from googletrans import Translator
from keys import BOT_TOKEN, API_ID, API_HASH


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


# Initialize the client
client = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)
translator = Translator()

CAPTION_MAX_LENGTH = 1024

# Source and destination channel IDs
source_channel_id = 'code_with_me1'
destination_channel_id = 'code_with_me_rus'


@client.on(events.NewMessage(chats=source_channel_id))
async def handler(event):
    # Get the message text and media
    message = event.message
    text = message.message
    media = message.media

    # Translate the text
    translated_text = translator.translate(text, dest='ru').text

    # Send the translated text and media to the destination channel
    if media:
        if len(translated_text) > CAPTION_MAX_LENGTH:
            # Split the text if it exceeds the caption limit
            await client.send_message(destination_channel_id, translated_text[:CAPTION_MAX_LENGTH], file=media)
            await client.send_message(destination_channel_id, translated_text[CAPTION_MAX_LENGTH:])
    else:
        await client.send_message(destination_channel_id, translated_text)


# Run the client
client.start()
client.run_until_disconnected()
