import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Bot
from discord.utils import get

import asyncio

from loguru import logger

from datetime import datetime

from settings import guild_id, readonly_id, archive_id, bot_use_id, clown_id, achievements_id, concussion_id

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(command_prefix='/', intents=intents)
tree = app_commands.CommandTree(client)

server_id = 1158788577505841202

def log(content):
    with open(f"logs/{datetime.now().strftime("%Y-%m-%d")}.log", "a", encoding="utf-8") as logs:
        logs.write(f'{datetime.now().strftime("%Y-%m-%d %H:%M")} -- {content}\n')
        
@client.event
async def on_connect():
    logger.info('✅ Bot successfully connected to discord')
    log("bot connected")
    
@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=server_id))
    logger.info('✅ Bot fully launched')
    log("bot started")
    
@tree.command(
    name="readonly",
    description="Выдать роль @Read Only",
    guild=discord.Object(id=server_id)
)
@app_commands.describe(member="Кому выдать мут", reason="Причина выдачи мута", mute_time="Срок наказания")
@app_commands.checks.has_permissions(mute_members=True)
async def readonly(interaction: discord.Interaction, member: discord.Member, reason: str, mute_time: str):
    role=get(interaction.guild.roles, id=readonly_id)
    time_convert={"s":1, "m":60, "h":3600, "d":86400}
    tempmute=int(mute_time[:-1]) * time_convert[mute_time[-1]]
    await member.add_roles(role)
    log(f'{interaction.user.name} выдал ридонли {member.name} на {mute_time} за {reason}')
    await interaction.response.send_message(f'{member.mention} выдана роль <@&{readonly_id}>',ephemeral=True)
    await interaction.guild.get_channel(archive_id).send(f'1. {member.mention}\n2. <@&{readonly_id}>\n3. {mute_time}\n4. {reason}\n5. {interaction.user.mention}')
    await asyncio.sleep(tempmute)
    log(f'У {member.name} снялось ридонли')
    await member.remove_roles(role)
    
@tree.command(
    name="clown",
    description="Выдать роль @🤡клоун🤡",
    guild=discord.Object(id=server_id)
)
@app_commands.describe(member="Кому выдать клоуна", reason="Причина выдачи клоуна")
@app_commands.checks.has_role(bot_use_id)
async def clown(interaction: discord.Interaction, member: discord.Member, reason: str):
    role = get(interaction.guild.roles, id=clown_id)
    await member.add_roles(role)
    log(f'{interaction.user.name} выдал лычку клоуна {member.name} за {reason}')
    await interaction.response.send_message(f'{member.mention} выдана роль <@&{clown_id}>',ephemeral=True)
    await interaction.guild.get_channel(archive_id).send(f'1. {member.mention}\n2. <@&{clown_id}>\n3. -\n4. {reason}\n5. {interaction.user.mention}')
    await interaction.guild.get_channel(achievements_id).send(f'{member.mention} получает лычку <@&{clown_id}> за {reason}')

@tree.command(
    name="concussion",
    description="Выдарь роль @😵Контуженный😵",
    guild=discord.Object(id=server_id)
)
@app_commands.describe(member="Кого контузить", reason="Причина контузии")
@app_commands.checks.has_role(bot_use_id)
async def concussion(interaction: discord.Interaction, member: discord.Member, reason: str):
    role = get(interaction.guild.roles, id=concussion_id)
    await member.add_roles(role)
    log(f'{interaction.user.name} выдал лычку контуженного {member.name} за {reason}')
    await interaction.response.send_message(f'{member.mention} выдана роль <@&{concussion_id}>',ephemeral=True)
    await interaction.guild.get_channel(archive_id).send(f'1. {member.mention}\n2. <@&{concussion_id}>\n3. -\n4. {reason}\n5. {interaction.user.mention}')
    await interaction.guild.get_channel(achievements_id).send(f'{member.mention} получает лычку <@&{concussion_id}> за {reason}')

@tree.command(
    name="clearwarn",
    description="Очистить варны",
    guild=discord.Object(id=server_id)
)
@app_commands.describe(member="Кому очистить", reason="Причина")
@app_commands.checks.has_role(bot_use_id)
async def clear_warn(interaction: discord.Interaction, member: discord.Member, reason: str):
    clown_role = get(interaction.guild.roles, id=clown_id)
    concussion_role = get(interaction.guild.roles, id=concussion_id)
    await member.remove_roles(clown_role, concussion_role)
    log(f'{interaction.user.name} снял варны {member.name} за {reason}')
    await interaction.response.send_message(f'{member.mention} сняты все варны.',ephemeral=True)
    await interaction.guild.get_channel(archive_id).send(f'1. {member.mention}\n2. Снятие варнов\n3. -\n4. {reason}\n5. {interaction.user.mention}')

client.run('token')