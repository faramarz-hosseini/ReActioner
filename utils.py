import emoji
import re


emoji_regexp = emoji.get_emoji_regexp(language="python")
emoji_pattern = re.compile(emoji_regexp)


def extract_emojis(s):
    return re.findall(emoji_pattern, s)
