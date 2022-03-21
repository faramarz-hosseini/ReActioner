import emoji
import re
import random


emoji_regexp = emoji.get_emoji_regexp(language="python")
emoji_pattern = re.compile(emoji_regexp)


def extract_emojis(s):
    return re.findall(emoji_pattern, s)

def shuffle_list(lst: List):
    random.shuffle(lst)