import discord
from data import *

intents = discord.Intents.all()
client = discord.Client(command_prefix='$', intents=intents)
TOKEN = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' # Use your discord bot token

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$val'):
        msg = message.content.split()
        username,tagline = msg[1].split('#')
        
        gen_data = get_general_data(username,tagline)
        mmr_data = get_mmr_data(username,tagline)
        account_lvl = get_account_lvl(gen_data)
        rank_icon_link = get_rank_icon(mmr_data)
        rank = get_rank(mmr_data)
        rr = get_rr(mmr_data)
        mmr_history = get_mmr_history(username,tagline)
        wl_history = get_wl_history(mmr_history)

        if msg[-1].lower() == 'history':
            match_history = get_match_history(username,tagline)
            last_5_history,last_5_agents = get_last_played(match_history,username)
            acs, kills, deaths, assists, hs, maps = get_last_5_stats(last_5_history,match_history)

            # Send msg
            embed2 = discord.Embed(title = f'{username}#{tagline} Match History')
            embed2.add_field(name=f'Match 1 {wl_history[0]}', value = f'Map: {maps[0]} Agent: {last_5_agents[0]} Score: {acs[0]} \n KDA: {kills[0]}/{deaths[0]}/{assists[0]} HS%: {hs[0]}')
            embed2.add_field(name=f'Match 2 {wl_history[1]}', value = f'Map: {maps[1]} Agent: {last_5_agents[1]} Score: {acs[1]} \n KDA: {kills[1]}/{deaths[1]}/{assists[1]} HS%: {hs[1]}', inline=False)
            embed2.add_field(name=f'Match 3 {wl_history[2]}', value = f'Map: {maps[2]} Agent: {last_5_agents[2]} Score: {acs[2]} \n KDA: {kills[2]}/{deaths[2]}/{assists[2]} HS%: {hs[2]}', inline=False)
            embed2.add_field(name=f'Match 4 {wl_history[3]}', value = f'Map: {maps[3]} Agent: {last_5_agents[3]} Score: {acs[3]} \n KDA: {kills[3]}/{deaths[3]}/{assists[3]} HS%: {hs[3]}', inline=False)
            embed2.add_field(name=f'Match 5 {wl_history[4]}', value = f'Map: {maps[4]} Agent: {last_5_agents[4]} Score: {acs[4]} \n KDA: {kills[4]}/{deaths[4]}/{assists[4]} HS%: {hs[4]}', inline=False)

            await message.reply(embed = embed2)
        
        else:
            # Send msg
            embed1 = discord.Embed(title=f'{username}#{tagline}')
            embed1.set_thumbnail(url=rank_icon_link)
            embed1.add_field(name="Rank", value = rank)
            embed1.add_field(name="Current RR", value = rr)
            embed1.add_field(name="Account Level", value = account_lvl, inline=False)
            embed1.add_field(name = 'Match History', value = wl_history, inline = False)
            await message.reply(embed = embed1)

client.run(TOKEN)
