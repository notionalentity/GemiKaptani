from ast import alias
from email.mime import message
from itertools import chain
from unicodedata import name
import discord
from discord.ext import commands
from utils import *
from functions import *
import database
import recommender
import appsettings

intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True, presences=True)
bot = commands.Bot(">", intents=intents)
game = Game()

TOKEN = open("token.txt","r").read()


@bot.event
async def on_ready():
    print("I'm ready onii-chan")

@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="giren")
    await channel.send(f"{member} sunucuya katıldı.")
    print(f"{member} sunucuya katıldı.")
@bot.event
async def on_member_remove(member):
    channel = discord.utils.get(member.guild.text_channels, name="çıkan")
    await channel.send(f"{member} sunucudan ayrıldı.")
    print(f"{member} sunucudan ayrıldı.")

@bot.command()
async def test(msg):
    await msg.send("Test")
@bot.command()
async def kumar(msg):
    await msg.send("Geliştiriliyor.")
@bot.command()
async def oyun(ctx, *args):
    if "roll" in args:
        await ctx.send(game.roll_dice())
    else:
        await ctx.send("please select a game")
@bot.command()
@commands.has_role("mod")
async def temizle(ctx, amount=15):
    await ctx.channel.purge(limit=amount)
@bot.command()
@commands.has_role("mod")
async def kick(ctx, member:discord.Member, *args, reason="Yok"):
    await member.kick(reason=reason)
@bot.command()
@commands.has_role("mod")
async def ban(ctx, member:discord.Member, *args, reason="Yok"):
    await member.ban(reason=reason)

#Anime Recommender Codes <3 uwu
@bot.command()
async def recommend(ctx, genre):
    anime = database.Get(genre)
    print(anime)
    if anime is not None:
        await ctx.send(f"Şunu dene! \n{anime}")
    else:
        await ctx.send(f"Maalesef böyle bir anime türü bulamadık. >genres yazarak türlere bakabilirsiniz.")

# (type ">genres to use comand)


@bot.command()
async def genres(ctx):
    GENRES = ['Sports', 'Shounen_Ai', 'Seinen', 'Shounen', 'Fantasy', 'Kids', 'Slice_of_Life', 'Mystery', 'Vampire', 'Shoujo', 'Sci-Fi', 'Game', 'Martial_Arts', 'Yuri', 'Adventure', 'Comedy', 'Magic', 'Romance', 'Mecha', 'Supernatural', 'Action',
              'Horror', 'Parody', 'Shoujo_Ai', 'School', 'Josei', 'Psychological', 'Thriller', 'Harem', 'Military', 'Super_Power', 'Samurai', 'Police', 'Demons', 'Music', 'Space', 'Cars', 'Dementia', 'Hentai', 'Historical', 'Yaoi', 'Ecchi', 'Drama']
    msg = '\n'.join(GENRES)
    await ctx.send(msg)

# (type ">search [anime] to use command)


@bot.command()
async def search(ctx, *anime):
    anime = ' '.join(anime)
    res = database.Search(anime)

    if len(res) != 0:
        out = f'showing {appsettings.AppSettings["MaxSearchResults"]} of {len(res)} results\n'
        for i, row in enumerate(res[:appsettings.AppSettings["MaxSearchResults"]],1):
            out += f"{i}. {row.Name}\n"
        await ctx.send(out)
    else:
        await ctx.send(f"Üzgünüz!, {anime} adında bir anime yok")

# (type ">similar [anime name]" to use command
@bot.command()
async def similar(ctx, *anime):
    anime = ' '.join(anime)
    if anime.strip() == '':
        await ctx.send(f"@{ctx.author} please specify an anime")
    else:
        res = recommender.FindSimilarJaccard(anime, appsettings.AppSettings["MaxRecommended"])
        if res == None:
            await ctx.send(f"Oops, {anime} adlı animeyi bulamadık.")
        else:
            msg = ''
            for row in res:
                msg += f"Şunu dene: {row[0]} skoru şundan iyi {row[1] * 100}%\n"
            await ctx.send(msg)

# (Type >random to use command)
@bot.command()
async def random(ctx):
    res = database.Random()
    await ctx.send(f"{res}")

# Allows user to change settings of the bot
#(type >set [prop] [val] where prop is a string and value is float or int)
@bot.command()
async def set(ctx, prop, val):
    if appsettings.AppSettings.get(prop) == None:
        await ctx.send('Öyle bir komut bulamadık. >settings yazarak bakabilirsiniz.')
    else:
        if prop == "MinSimilartityScore":
            val =  abs(float(val))
        else:
            val = abs(int(val))
        
        appsettings.AppSettings[prop] = val

#Allows user to view the settings of the bot
#(type >settings)
@bot.command()
async def settings(ctx):
    out = ""    
    for i, key in enumerate(appsettings.AppSettings.keys()):
        out += f"- {key}\n\t{appsettings.Descriptions[i]}\n"

    await ctx.send(out)

bot.run(TOKEN)    