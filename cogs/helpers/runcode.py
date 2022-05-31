import discord
from io import StringIO
import textwrap
from contextlib import redirect_stdout
import traceback
import os, sys, linecache, signal, requests
import aiohttp
from .snekbox import nsjail

def _get_code(content: str):
    if content.startswith("```") and content.endswith("```"):
        new_content: str = content.replace("```", "").replace("py", "")
        return new_content

    return content

def post_eval_req(code: str):
    result = nsjail.NsJail().python3(_get_code(code))
    output = {
        "stdout": result.stdout,
        "returncode": result.returncode
    }

    return format_output(output)

def format_output(output: dict):
    stdout = output["stdout"]
    return_code = output["returncode"]

    if return_code == 0:
        if stdout is None or len(stdout) == 0 or stdout == '':
            return "Your eval job completed with code 5 :warning: \n```py\nNo output```"

        if len(stdout) > 2000:
            return upload_output(stdout)

        lines = stdout.split("\n")
        lines.pop()
        msg = ""
        for i in range(len(lines)):
            msg += f"0{i+1}|  {lines[i]}\n" if i < 100 else f"{i+1}|  {lines[i]}\n"

        return f"Your eval job completed with code 0 :white_check_mark: \n```py\n{msg}\n```"

    if return_code == 1:
        stdout = stdout.replace('"<string>"', '"<Your Code>"')
        return f"Your eval job completed with code 1 :x: \n```py\n{stdout}\n```"

    if return_code == 137:
        return "Your eval job completed with code 137 :x: \n```py\nTime limit exceed!\n```"

def upload_output(data: str):
    if len(data) > 10000:
        return "Output too long to upload to hastebin"
    
    req = requests.post("https://hastebin.com/documents", data=data.encode("utf-8"))
    if req.status_code != 200:
        return "Failed to upload output"

    return f"Output too long to send. Sent to hastebin instead\n<https://www.toptal.com/developers/hastebin/{req.json()['key']}>"