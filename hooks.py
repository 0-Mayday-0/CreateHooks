import re
import requests
from asyncio import run, Task, create_task, to_thread
from collections.abc import Coroutine

class Bot:
    def __init__(self, url: str) -> None:
        try:
            self._protocol: str = re.search("(https:)", url).group()
            self._root_domain: str = re.search("(//discord)", url).group()
            self._top_level_domain: str = re.search("(.com)", url).group()
            self._slug: str = re.search("(/api/webhooks)" ,url).group()
            self._hook_number: str = re.search(r"(/\d{19})", url).group()
            self._hook_id: str = re.search(r"(/\w{68})", url).group()

        except AttributeError:
            raise Exception("The URL provided is not a valid Discord webhook")

    @property
    def _assemble_url(self) -> str:
        return f'{self._protocol}{self._root_domain}{self._top_level_domain}{self._slug}{self._hook_number}{self._hook_id}'

    async def _send_message(self, message: str) -> requests.Response:
        response: requests.Response = await to_thread(requests.post, self._assemble_url, data={'content': message})
        return response

    def take_meds(self):
        raise NotImplementedError

    def __repr__(self) -> str:
        return f"Bot({self._hook_number.replace('/', '')})"

    def __str__(self) -> str:
        return f'{self._root_domain}{self._top_level_domain}{self._hook_number}'

async def main():
    testbot: Bot = Bot("https://discord.com/api/webhooks/1274408342026190932/YzDllT6M0qpUO02kLNniXCc2GSqAagTeQqFGOoupDbxL_LRuWwcKQduyi9uRt_9jBFA8")

    msg_task: Task[requests.Response] = create_task(testbot._send_message("Hello World!"))

    print(await msg_task)

if __name__ == '__main__':
    run(main())