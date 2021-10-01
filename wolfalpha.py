import requests
import discord
from discord.ext import commands
import shutil
from PIL import Image
import secret

prefix = "="
bot = commands.Bot(command_prefix=prefix)
bot.remove_command("help")


def send_request_to_api(request, token):
    url = "http://api.wolframalpha.com/v1/simple?appid=" + token + "&i=" + request + "&width=1000"
    response = requests.get(url, stream=True)
    if response.ok:
        with open("request.gif", "wb") as out_file:
            shutil.copyfileobj(response.raw, out_file)
    return response.status_code


def convert_gif_to_png(filename):
    im = Image.open(filename + '.gif')
    im.save(filename + '.png', transparency=im.info.get('transparency'))
    return 0


@bot.command()
async def query(ctx, *request):
    request = " ".join(request[:])
    response = send_request_to_api(request.replace("+", "%2B"), secret.wolfram_token)
    if response == 200:
        convert_gif_to_png('request')
        file = discord.File("request.png", filename="request.png")
        await ctx.send("Here's the result for `" + request + "`", file=file)
    else:
        await ctx.send("Something went wrong, code = " + str(response))


@bot.command()
async def help(ctx):
    e = discord.Embed(Title="Help", description="Use `=query <query>` to send a request")
    await ctx.send(embed=e)

bot.run(secret.discord_token)
