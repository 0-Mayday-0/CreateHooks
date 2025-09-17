import re
import requests
from asyncio import run, Task, create_task, to_thread
import datetime


class Bot:
    def __init__(self, url: str) -> None:
        try:
            self._protocol: str = re.search("(https:)", url).group()
            self._root_domain: str = re.search("(//discord)", url).group()
            self._top_level_domain: str = re.search("(.com)", url).group()
            self._slug: str = re.search("(/api/webhooks)" ,url).group()
            self._hook_number: str = re.search(r"(/\d{19})", url).group()
            self._hook_id: str = re.search(r"(/)(\w|-){68}", url).group()

        except AttributeError:
            raise Exception("The URL provided is not a valid Discord webhook")

    @property
    def _assemble_url(self) -> str:
        return f'{self._protocol}{self._root_domain}{self._top_level_domain}{self._slug}{self._hook_number}{self._hook_id}'

    async def _send_message(self, message: str) -> requests.Response:
        response: requests.Response = await to_thread(requests.post, self._assemble_url, data={'content': message})
        return response

    @staticmethod
    def _prompt_current_time() -> tuple[bool, str]:
        user_invalid: bool = True
        valid_inputs: list[str] = ['0', '1']

        while user_invalid:
            current_time: datetime.datetime = datetime.datetime.now()
            user_now: str = input(f"Hiya! Did you take your meds at {current_time.strftime('%H:%M')}? [0/1]: ")

            user_invalid = user_now not in valid_inputs

            if user_invalid:
                print("\nInvalid input. Please try again.\n")

        # noinspection PyUnboundLocalVariable
        return bool(int(user_now)), current_time.strftime('%H:%M')

    @staticmethod
    def _prompt_actual_time() -> str:
        user_invalid: bool = True
        valid_pattern: re.Pattern = re.compile(r"\d{2}:\d{2}")

        while user_invalid:
            user_actual: str = input("What time did you take your meds? [xx:yy]: ")

            user_invalid = not bool(re.search(valid_pattern, user_actual))

            if user_invalid:
                print("\nInvalid input. Please try again.\n")

        #noinspection PyUnboundLocalVariable
        return user_actual

    @staticmethod
    def _prompt_funfact() -> str:
        user_in: str = input("Do you want to send a fun fact? Leave blank to skip: ")

        return user_in

    async def take_meds(self):
        took_now: tuple[bool, str] = self._prompt_current_time()
        current_date: datetime.datetime = datetime.datetime.today()
        suffixes: list[str] = ['th', 'st', 'nd', 'rd', 'th', 'th', 'th', 'th', 'th', 'th']

        funfact_in: str = self._prompt_funfact()

        if funfact_in:
            funfact_task: Task[requests.Response] = create_task(
                self._send_message(f"Mayday fun fact of the day: {funfact_in}"))


        if not took_now[0]:
            actual_time: str = self._prompt_actual_time()
            take_meds_task: Task[requests.Response] = create_task(
                self._send_message(f"Good {current_date.strftime('%A')}!"
                                   f" Today is the {current_date.strftime('%d')}"
                                   f"{suffixes[int(current_date.strftime('%d')[-1])]},"
                                   f" Mayday took her meds at {actual_time} :3"))


        else:
            take_meds_task: Task[requests.Response] = create_task(
                self._send_message(f"Good {current_date.strftime('%A')}!"
                                   f" Today is the {current_date.strftime('%d')}"
                                   f"{suffixes[int(current_date.strftime('%d')[-1])]},"
                                   f" Mayday took her meds at {took_now[1]} :3"))

        try:
            # noinspection PyUnboundLocalVariable
            return await take_meds_task, await funfact_task
        except UnboundLocalError:
            return await take_meds_task

    def __repr__(self) -> str:
        return f"Bot({self._hook_number.replace('/', '')})"

    def __str__(self) -> str:
        return f'{self._root_domain}{self._top_level_domain}{self._hook_number}'

async def main():
    testbot: Bot = Bot("https://discord.com/api/webhooks/1274408342026190932/YzDllT6M0qpUO02kLNniXCc2GSqAagTeQqFGOoupDbxL_LRuWwcKQduyi9uRt_9jBFA8")

    print(await testbot.take_meds())

if __name__ == '__main__':
    run(main())