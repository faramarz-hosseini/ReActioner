import emoji
import re


regexp = emoji.get_emoji_regexp(language="python")
pattern = re.compile(regexp)


def extract_emojis(s):
    return re.findall(pattern, s)

