from eb_vars import *
from keyHandling import isAdminOnly
from discord.ext import commands
import json

class hereClass(commands.Cog):
  
  def __init__(self, client):
    self.client = client
    
  @commands.Cog.listener()
  async def on_ready(self):
    print("here Cog Running")
  
  
  #COMMANDS
  @commands.command()
  async def here(self, ctx):
    is_admin_only = isAdminOnly(str(ctx.guild.id))
    is_server_admin = ctx.author.guild_permissions.administrator
    if is_admin_only != 404:
      if is_admin_only and is_server_admin or not is_admin_only:
        guildID = ctx.guild.id
        channelID = ctx.channel.id
        try:
          with open(f'./guild-files/{guildID}_keywords.json', 'r', encoding="utf-8") as file:
              data = json.load(file)
              data["activeChannelID"] = channelID
          with open(f'./guild-files/{guildID}_keywords.json', 'w', encoding="utf-8") as file:
              data = json.dump(data,file)
          await ctx.send("Updating Here!")
        except:
          await ctx.send("There was a problem changing channels")
    else:
      await ctx.send(embed = em_setUpReqd)
      
def setup(client):
  client.add_cog(hereClass(client))