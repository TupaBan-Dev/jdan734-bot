import asyncio

from ..config import dp


@dp.message_handler(commands=["ping"])
async def ping(message):
    reply = await message.reply("Pong")
    await asyncio.sleep(1)

    await message.delete()
    await reply.delete()
