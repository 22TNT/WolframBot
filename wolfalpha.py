import requests
import json
import discord
import shutil
from discord.ext import commands
from PIL import Image
import secret

prefix = "!w"
discord_token = secret.discord_token
wolfram_token = secret.wolfram_token
bot = commands.Bot(command_prefix=prefix)


def send_request_to_api(request):
    url = "http://api.wolframalpha.com/v1/simple?appid=" + wolfram_token + "&i=" + request
    response = requests.get(url, stream=True)
    if response.ok:
        with open("simple.gif", "wb") as out_file:
            shutil.copyfileobj(response.raw, out_file)
        im = Image.open('request.gif')
        transparency = im.info.get('transparency')
        im.save('request.png', transparency=transparency)
        del im
        del response
        return 0
    else:
        return response.status_code

