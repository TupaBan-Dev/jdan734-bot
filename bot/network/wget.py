import json
import sys
from datetime import datetime

import yaml

from ..config import dp
from ..lib.aioget import aioget
from ..lib.convert_bytes import convert_bytes
from ..lib.html import code
from ..lib.libtree import make_tree


@dp.message_handler(lambda message: message.from_user.id == 795449748,
                    commands=["d"])
async def download(message):
    options = message.text.split(maxsplit=1)

    if len(options) == 1:
        await message.reply("Напиши ссылку")
        return

    response = await aioget(options[1])
    text = await response.text()

    try:
        text = yaml.dump(json.loads(text))
    except json.decoder.JSONDecodeError:
        pass

    await message.reply(code(text[:4096]),
                        parse_mode="HTML")


@dp.message_handler(commands=["wget", "r", "request"])
async def wget(message):
    opt = message.text.split(maxsplit=1)
    if len(opt) == 1:
        await message.reply("Напиши ссылку")
        return

    time = datetime.now()
    url = opt[1]

    blacklist = ["mb", ".zip", ".7", ".gz", "98.145.185.175", ".avi",
                 "movie", "release", ".dll", "localhost", ".bin",
                 "0.0.0.1", "repack", "download"]

    if url.find("?") != -1:
        if url.split("/")[-1][:url.find("?")].find(".") != -1:
            await message.reply("Бан")
            return

    for word in blacklist:
        if url.lower().find(word) != -1:
            await message.reply("Ваша ссылка в черном списке")
            return

    try:
        response = await aioget(url)
    except Exception as e:
        await message.reply(code(e), parse_mode="HTML")
        return

    load_time = datetime.now() - time
    main = str(load_time).split(":")

    page = await response.text()

    tree = make_tree({
        "status": response.status,
        "size": convert_bytes(sys.getsizeof(page)),
        "time": f"{main[1]}:{main[2][:main[2].find('.')]}"
    }, url)

    await message.reply(code(tree), parse_mode="HTML")
