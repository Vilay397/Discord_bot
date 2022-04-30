import json
import string
import discord
from discord.ext import commands
import os, sqlite3


bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print('Censor ready')

    global base, cur
    base = sqlite3.connect('Censor.db')
    cur = base.cursor()
    if base:
        print('DataBase connected...OK')


@bot.event
async def on_member_join(member):
    await member.send('Привет! Я бот Censor, просмотр команд начинается с !инфо')

    for ch in bot.get_guild(member.guild.id).channels:
        if ch.name == 'основной':
            await bot.get_channel(ch.id).send(f'{member}, хорошо что ты с нами в лс инфо')

@bot.event
async def on_member_remove(member):
    for ch in bot.get_guild(member.guild.id).channels:
        if ch.name == 'основной':
            await bot.get_channel(ch.id).send(f'{member}, нам будет тебя не хватать')

@bot.command()
async def test(ctx):
    await ctx.send('грязно выругался...')

@bot.command()
async def инфо(ctx, arg=None):
    author = ctx.message.author
    if arg == None:
        await ctx.send(f'{author.mention} Введите:\n!инфо общая\n!инфо команды')
    elif arg == 'общая':
        await ctx.send(f'{author.mention} Я Censor и слежу за порядком в чате. 3-е предупреждение за мат - БАН')
    elif arg == 'команды':
        await ctx.send(f'{author.mention} !test - Бот онлайн?\n !статус - мои предупреждения')
    else:
        await ctx.send(f'{author.mention} Такой команды нет...')

@bot.command()
async def статус(ctx):
    base.execute('CREATE TABLE IF NOT EXISTS {}(userid INT, count INT)'.format(ctx.message.guild.name))
    base.commit()
    warning = cur.execute('SELECT * FROM {} WHERE userid == ?'.format(ctx.message.guild.name), (ctx.message.author.id,)).fetchone()
    if warning == None:
        await ctx.send(f'{ctx.message.author.mention}, У вас нет предупреждений !!!')
    else:
        await ctx.send(f'{ctx.message.author.mention}, У вас {warning[1]} предупреждений !!!')

@bot.event
async def on_message(message):
    if {i.lower().translate(str.maketrans('','', string.punctuation)) for i in message.content.split(' ')}\
    .intersection(set(json.load(open('cenz.json')))) != set():
        await message.channel.send(f'{message.author.mention}, ууу...тут нельзя ругаться матом!!!')
        await message.delete()

        name = message.guild.name

        base.execute('CREATE TABLE IF NOT EXISTS {}(userid INT, count INT)'.format(name))
        base.commit()

        warning = cur.execute('SELECT * FROM {} WHERE userid == ?'.format(name),(message.author.id,)).fetchone()

        if warning == None:
            cur.execute('INSERT INTO {} VALUES(?, ?)'.format(name),(message.author.id,1))
            base.commit()
            await message.channel.send(f'{message.author.mention}, первое предупреждение, 3-е БАН!')
        elif warning[1] == 1:
            cur.execute('UPDATE {} SET count == ? WHERE userid == ?'.format(name),(2,message.author.id))
            base.commit()
            await message.channel.send(f'{message.author.mention}, 2-е предупреждение, на 3-е БАН!')
        elif warning[1] == 2:
            cur.execute('UPDATE {} SET count == ? WHERE userid == ?'.format(name), (3, message.author.id))
            base.commit()
            await message.channel.send(f'{message.author.mention}, Забанен в чате. ')
            await message.author.ban(reason='Нецензурные выражения')

    await bot.process_commands(message)

bot.run(os.getenv('TOKEN'))
