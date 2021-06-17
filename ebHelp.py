import discord
import os
from discord.ext import commands

class ebHelpCommand(commands.HelpCommand):

  def __init__(self):
    super().__init__

  async def eb_help(self, mapping):
    for thing in mapping:
      await self.