import requests
import json
import discord
import shutil
from discord.ext import commands
from PIL import Image


prefix = "!wa"
discordtoken = ""
wolframtoken = ""
bot = commands.bot(command_prefix=prefix)


def normalize_equation_string(input_string):
    input_string.replace(" ", "")
    input_string.replace("/", "%2F")
    input_string.replace("%", "%25")
    input_string.replace("=", "%3D")
    input_string.replace("+", "%2B")
    return input_string


def normalize_request_string(input_string):
    input_string.replace(" ", "+")
    input_string.replace("+", "%2B")
    input_string.replace("%", "%25")
    input_string.replace("?", "%3F")
    return input_string


def send_request_to_api(request):
    url = "http://api.wolframalpha.com/v1/simple?appid="+wolframtoken+"&i="+request
    response = requests.get(url, stream=True)
    if response.ok:
        with open("simple.gif", "wb") as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response
        im = Image.open('simple.gif')
        transparency = im.info['transparency']
        im.save('simple.png', transparency=transparency)
        del im
        return 0
    else:
        return response.status_code
