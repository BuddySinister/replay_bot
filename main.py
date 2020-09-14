from abc import ABC
from dotenv import load_dotenv
from time import time
from twitchio.ext import commands
import keyboard
import os

load_dotenv()

TOKEN = os.getenv("TOKEN_KEY")
CLIENTID = os.getenv("CLIENT_ID")
NICK = os.getenv("NICK")
PREFIX = os.getenv("PREFIX")
CHANNEL = os.getenv("CHANNEL")


class InertBot(commands.Bot, ABC):
    def __init__(self):
        self.call_freq = 30
        self.cmd_tracker = {'cmd': '', 'last_use': 0.0}
        super().__init__(irc_token=TOKEN,
                         client_id=CLIENTID,
                         nick=NICK, prefix=PREFIX, initial_channels=[CHANNEL])

    def process_replay(self):
        if time() - self.cmd_tracker['last_use'] > self.call_freq:
            self.cmd_tracker['last_use'] = time()
            keyboard.press_and_release('f13')
        else:
            return

    async def event_ready(self):
        print(f'Ready | {self.nick}')

    async def event_message(self, message):
        if message.author.name.lower() == self.nick.lower():
            return
        print(message.content)
        await self.handle_commands(message)

    @commands.command(name='replay')
    async def replay_cmd(self, ctx):
        _ = ctx  # unused
        self.process_replay()


if __name__ == '__main__':
    try:
        bot = InertBot()
        bot.run()
    except KeyboardInterrupt:
        exit()
