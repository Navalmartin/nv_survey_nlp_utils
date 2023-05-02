from .text_helpers import remove_punctuation


class ReplaceTask(object):
    def __init__(self, text_to_replace: str,
                 replace_with: str):
        self.text_to_replace = text_to_replace
        self.replace_with = replace_with

    def __call__(self, text: str) -> str:
        text = text.replace('.', '')
        return text


class RemovePunctuation(object):
    def __init__(self, regex: str = '–«!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~»●·’“”'):
        self.regex = regex

    def __call__(self, text: str) -> str:
        return remove_punctuation(text=text, regex=self.regex)


class LStrip(object):
    def __init__(self):
        pass

    def __call__(self, text: str) -> str:
        text = text.lstrip()
        return text


class RStrip(object):
    def __init__(self):
        pass

    def __call__(self, text: str) -> str:
        text = text.rstrip()
        return text
