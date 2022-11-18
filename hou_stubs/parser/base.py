from dataclasses import dataclass, field
import re
from typing import Callable, ClassVar, Union


PATTERNS_TYPE = list[tuple[str, Union[str, Callable]]]


class Parser:

    fixed_types: dict[str, str] = {}
    replacements: dict[str, str] = {}
    patterns: PATTERNS_TYPE = []
    formatters: list[Callable[[str], str]] = []

    # def __init__(self) -> None:
    #     self.patters = [(re.compile(pattern), repl) for pattern, repl in self.patters]

    def replace_fixed_types(self, text: str) -> str:
        for pattern, repl in self.fixed_types.items():
            pattern = re.escape(pattern)
            pattern = rf"\b{pattern}\b"
            # print("pattern")
            # print(">>>", pattern)
            # print(text, repl)
            match = re.match(text, pattern)
            print(match)

            text = re.sub(pattern, repl, text)
        return text

    def pre(self, text) -> str:
        for src, tar in self.replacements.items():
            text = text.replace(src, tar)
        text = self.replace_fixed_types(text)
        return text

    def main(self, text) -> str:

        # if text in self.fixed_types:
        #     return self.fixed_types[text]

        # for t, r in self.fixed_types.items():
        #     text = text.replace(t, r)

        for formatter in self.formatters:
            new = formatter(text)
            if new != text:
                text = self.main(new)

        for pattern, repl in self.patterns:
            new = re.sub(pattern, repl, text)
            if new != text:
                return self.main(new)
        return text

    def parse(self, text: str) -> str:
        text = self.pre(text)
        text = self.main(text)
        return text
