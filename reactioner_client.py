import inspect
import random

from typing import List

from discord import (
    Client, Message, Reaction, User, Member, PartialMessage, Guild,
)
from utils import extract_emojis, shuffle_list
from const import MESSAGE_STYLES, PRE_EVENT_TEXT


class ReActionerClient(Client):

    def __init__(self, token):
        super().__init__()
        self.token = token
        self.non_command_methods = {"on_ready", "on_message"}
        self.commands = self._get_command_methods()

    async def on_ready(self):
        print('We have logged in as {0}'.format(self.user))

    async def on_message(self, message: Message):
        if message.content.startswith("!"):
            cmd_parts = message.content[1:].strip().split()
            cmd, args = cmd_parts[0], cmd_parts[1:]
            handler = self.commands.get(cmd, None)
            if handler:
                await handler(message, *args)
                await message.delete()

    @staticmethod
    async def vote_reactions(message: Message, *args):
        if not message.reference:
            return
        referred_msg: Message = await message.channel.fetch_message(message.reference.message_id)
        emojis = extract_emojis(referred_msg.content)
        for emoji in emojis:
            await referred_msg.add_reaction(emoji)

    @staticmethod
    async def rand_roles(message: Message, *args):
        roles = [role.name for role in message.guild.roles]
        shuffle_list(roles)

        pre_event_text = PRE_EVENT_TEXT+" " if args else PRE_EVENT_TEXT.replace("for", "").strip()
        event_name = MESSAGE_STYLES['bold'].format(" ".join(args)) if args else ""
        event_desc = MESSAGE_STYLES['quote'].format(pre_event_text+event_name+":\n")
        role_counter = 1
        event_roles_text = []
        for role in roles:
            event_roles_text.append(str(role_counter)+") "+role)
            role_counter += 1
        event_roles_text = "\n".join(event_roles_text)

        await message.channel.send(event_desc+event_roles_text)

    def _get_command_methods(self):
        all_methods = inspect.getmembers(ReActionerClient, predicate=inspect.isfunction)
        return {
            func_name: func for func_name, func in all_methods
            if not func_name.startswith("_")
            and func_name not in dir(Client)
            and func_name not in self.non_command_methods
        }
