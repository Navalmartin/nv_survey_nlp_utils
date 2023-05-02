from typing import Any


def remove_punctuation(text: str, regex: str = '–«!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~»●·’“”'):
    """custom function to remove the punctuation"""
    return text.translate(str.maketrans('', '', regex))


def remove_stopwords(text: str, stop_words_dict: Any):
    """custom function to remove stopwords"""
    return [word for word in str(text).split() if word not in stop_words_dict]