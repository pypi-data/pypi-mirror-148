from dataclasses import dataclass

from typing import List, Union


@dataclass
class ChapterDTO:
    index: int
    title: str
    url: str
    content: Union[str, List[str]] = None
