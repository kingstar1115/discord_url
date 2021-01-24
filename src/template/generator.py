import re
from . import icon


class Channels:
    LOWEST_CHAR_LIMIT = 75
    HIGHEST_CHAR_LIMIT = 166
    EXT_CHAR_LIMIT = 260

    def __init__(self, channels: list):
        self.channels = channels

    def length(self):
        return sum([len(_) for _ in self.channels]) + 2 * (len(self.channels) - 1)

    def truncate(self, highest_char_limit=HIGHEST_CHAR_LIMIT):
        while self.length() > highest_char_limit:
            self.channels.pop()


class GenerateTemplate:
    ICON_PATH = 'images/server_icons'

    def __init__(self, name: str, invite_code: str, official: bool, homepage: str, git: str, notable_channels: list,
                 language, icon_path=ICON_PATH):
        self.name = name
        self.invite_code = invite_code
        self.official = official
        self.homepage = homepage
        self.git = git
        self.channels = notable_channels
        self.language = language
        self.icon_path = icon_path

    def format_name(self):
        return f'{self.name}'

    def format_invite(self):
        return f'https://discord.com/invite/{self.invite_code}'

    def format_icon(self):
        if self.icon_path is GenerateTemplate.ICON_PATH:  # alternative: self.__init__.__defaults__[0]
            return f'<img align="left" height="94px" width="94px" alt="Server Icon" src="{self.icon_path}/' \
                   f'{icon.GetIcon.icon_name(self.name)}.webp" /> '
        return f'<img align="left" height="94px" width="94px" alt="Server Icon" src="{self.icon_path}" /> '

    def format_reddit(self):
        # From subreddit name rule: https://redd.it/592kmw
        m = re.search(r'reddit.com/r/[a-zA-Z0-9_]+/?', self.homepage) if self.homepage else None
        if m:
            return f' [<img height="16px" width="16px" alt="Reddit Badge" src="images/badges/reddit.webp">]' \
                   f'(badges.md#reddit-badge)'
        return f''

    def format_official(self):
        if self.official:
            return f' [<img height="16px" width="16px" alt="Official Badge" src="images/badges/official.webp">]' \
                   f'(badges.md#official-identification-badge)'
        return f''

    def format_homepage(self):
        if self.homepage:
            return f' [<img height="16px" width="16px" alt="Homepage URL" src="images/badges/homepage.webp">]' \
                   f'({self.homepage})'
        elif self.official and not self.homepage:
            raise ValueError('An official community must have a homepage that claims its ownership')
        return f''

    def format_git(self):
        if self.git:
            return f' [<img height="16px" width="16px" alt="Git Repository" src="images/badges/git.webp">]({self.git})'
        return f''

    def format_channels(self):
        channels = ["#" + _ for _ in self.channels]
        c = Channels(channels)
        initial_length = c.length()
        if initial_length >= c.EXT_CHAR_LIMIT:
            c.truncate(c.HIGHEST_CHAR_LIMIT - 15)
            channels.append('**[`so much more`](badges.md#so-much-more)**')
        else:
            c.truncate()
        return ', '.join(channels)

    def format_language(self):
        languages = ', '.join(self.language) if isinstance(self.language, list) else self.language
        return languages

    def padding(self):
        return f'<br />' if len(self.format_channels()) <= Channels.LOWEST_CHAR_LIMIT else f''
