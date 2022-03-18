import os
import logging

from discord import (
    Client, Message, Reaction, User, Member, PartialMessage, MessageReference,
)

from utils import extract_emojis

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ReActionerClient(Client):

    def __init__(self):
        super().__init__()
        self.commands = {
            "vote_reactions": self.vote_reactions,
        }

    async def on_ready(self):
        print('We have logged in as {0}'.format(self.user))

    async def on_message(self, message: Message):
        if message.content.startswith("!"):
            cmd = message.content[1:].strip()
            handler = self.commands.get(cmd, None)
            if handler:
                await handler(message=message)

    @staticmethod
    async def vote_reactions(message: Message):
        if not message.reference:
            return
        referred_msg: Message = await message.channel.fetch_message(message.reference.message_id)
        emojis = extract_emojis(referred_msg.content)
        for emoji in emojis:
            await referred_msg.add_reaction(emoji)


client = ReActionerClient()
client.run(os.environ.get("discord-token"))
