import re

class Bot:
    def __init__(self, url: str) -> None:
        try:
            self.protocol: str = re.search("(https:)", url).group()
            self.root_domain: str = re.search("(//discord)", url).group()
            self.top_level_domain: str = re.search("(.com)", url).group()
            self.slug: str = re.search("(/api/webhooks)" ,url).group()
            self.hook_number: str = re.search(r"(/\d{19})", url).group()
            self.hook_id: str = re.search(r"(/\w{68})", url).group()

        except AttributeError:
            raise Exception("The URL provided is not a valid Discord webhook")


    def __repr__(self) -> str:
        return f"Bot({self.hook_number.replace('/', '')})"

    def __str__(self) -> str:
        return f'{self.root_domain}{self.top_level_domain}{self.hook_number}'

def main():
    testbot: Bot = Bot("https://discord.com/api/webhooks/1274408342026190932/YzDllT6M0qpUO02kLNniXCc2GSqAagTeQqFGOoupDbxL_LRuWwcKQduyi9uRt_9jBFA8")

    print(repr(testbot))

if __name__ == '__main__':
    main()