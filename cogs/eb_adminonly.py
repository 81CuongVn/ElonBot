import discord
from eb_vars import *
from keyHandling import setAdminOnly, isAdminOnly
from discord.ext import commands

class adminonlyClass(commands.Cog):
  
  def __init__(self, client):
    self.client = client
    
  @commands.Cog.listener()
  async def on_ready(self):
    print("AdminOnly Cog Running")
  
  
  #COMMANDS
  @commands.command()
  async def adminOnly(self, ctx):
    if ctx.author.guild_permissions.administrator:
      boolVal = isAdminOnly(ctx.guild.id)
      if boolVal != 404:
        if boolVal:
          setAdminOnly(False, ctx.guild.id)
          await ctx.send("ElonBot Commands are now **not** Admin-Only")
        else:
          setAdminOnly(True, ctx.guild.id)
          await ctx.send("ElonBot Commands are now Admin-Only")
      else:
        await ctx.send(embed = em_setUpReqd)
      
def setup(client):
  client.add_cog(adminonlyClass(client))