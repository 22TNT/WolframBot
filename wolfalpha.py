import requests
import json
import discord
import shutil
from discord.ext import commands
from PIL import Image
import secret

prefix = "="
discord_token = secret.discord_token
wolfram_token = secret.wolfram_token

bot = commands.Bot(command_prefix=prefix)
bot.remove_command("help")


def send_request_to_api(request):
    url = "http://api.wolframalpha.com/v1/simple?appid=" + wolfram_token + "&i=" + request + "&width=1000"
    response = requests.get(url, stream=True)
    if response.ok:
        with open("request.gif", "wb") as out_file:
            shutil.copyfileobj(response.raw, out_file)
        im = Image.open('request.gif')
        transparency = im.info.get('transparency')
        im.save('request.png', transparency=transparency)
        return 0
    else:
        return response.status_code


@bot.command()
async def query(ctx, *request):
    request = " ".join(request[:])
    request = request.replace("+", "%2B")
    if not send_request_to_api(request):
        file = discord.File("request.png", filename="request.png")
        await ctx.send("Here's the result for `" + request.replace("%2B", "+") + "`", file=file)
    else:
        await ctx.send("Something went wrong, try again or contact admin")


@bot.command()
async def help(ctx):
    e = discord.Embed(Title="Help", description="Use `=query <query>` to send a request")
    await ctx.send(embed=e)

bot.run(discord_token)
