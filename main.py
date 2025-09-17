import asyncio
from hooks import Bot
from dotenv import load_dotenv
from os import getenv

async def main():
    load_dotenv('.env')

    testbot = Bot(getenv("TESTBOT"))
    maydaybot = Bot(getenv("MAYDAYAIDER"))


    input(await maydaybot.take_meds())


if __name__ == '__main__':
    asyncio.run(main())