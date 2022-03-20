import os
import inspect
import logging

from types import FunctionType

from discord import (
    Client, Message, Reaction, User, Member, PartialMessage, MessageReference,
)

from utils import extract_emojis

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ReActionerClient(Client):

    def __init__(self):
        super().__init__()
        self.non_command_methods = ["on_ready", "on_message", "_get_command_methods"]
        self.commands = self._get_command_methods()

    async def on_ready(self):
        print('We have logged in as {0}'.format(self.user))

    async def on_message(self, message: Message):
        if message.content.startswith("!"):
            cmd = message.content[1:].strip()
            handler = self.commands.get(cmd, None)
            if handler:
                await handler(message=message)
                await message.delete()

    @staticmethod
    async def vote_reactions(message: Message):
        if not message.reference:
            return
        referred_msg: Message = await message.channel.fetch_message(message.reference.message_id)
        emojis = extract_emojis(referred_msg.content)
        for emoji in emojis:
            await referred_msg.add_reaction(emoji)

    def _get_command_methods(self):
        all_methods = inspect.getmembers(ReActionerClient, predicate=inspect.isfunction)
        return {
            func_name: func for func_name, func in all_methods
            if not func_name.startswith("__")
            and func_name not in dir(Client)
            and func_name not in self.non_command_methods
        }


client = ReActionerClient()
client.run("OTU0MzU5NDg1MjY5NDI2MjI4.YjR-iA.7_y3ReiquziSFPLUYuc6cQmTzMQ")
