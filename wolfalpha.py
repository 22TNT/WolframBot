import requests
import discord
from discord.ext import commands
import shutil
import secret

prefix = "="
bot = commands.Bot(command_prefix=prefix)
bot.remove_command("help")


def send_request_to_api(request, token):
    """ Sends a GET request to WolframAlpha API and saves the file as a .gif. """
    url = "http://api.wolframalpha.com/v1/simple?appid=" + token + "&i=" + request + "&width=1000"
    response = requests.get(url, stream=True)
    if response.ok:
        with open("request.gif", "wb") as out_file:
            shutil.copyfileobj(response.raw, out_file)
    return response.status_code


@bot.command()
async def query(ctx, *request):
    """ Reads a message from Discord that starts with =, calls send_request_to_api() and sends the .gif
    as a .png to the Discord chat that ran the query or returns the error code. """
    request = " ".join(request[:])
    response = send_request_to_api(request.replace("+", "%2B"), secret.wolfram_token)
    if response == 200:
        file = discord.File("request.gif", filename="request.png")
        await ctx.send("Here's the result for `" + request + "`", file=file)
    else:
        await ctx.send("Something went wrong, code = " + str(response))


@bot.command()
async def help(ctx):
    """ A Help command. """
    e = discord.Embed(Title="Help", description="Use `=query <query>` to send a request")
    await ctx.send(embed=e)

bot.run(secret.discord_token)
