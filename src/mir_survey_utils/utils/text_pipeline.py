from typing import Callable, List


class TextPipeline(object):
    def __init__(self, tasks: List[Callable]):
        self.tasks = tasks

    def __call__(self, text: str) -> str:

        for task in self.tasks:
            text = task(text)
        return text