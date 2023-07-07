from dataclasses import dataclass, field
from typing import List
from wordlist import WordList

@dataclass
class Phrase():
    wordLengths: List[int] = field(default_factory=list)
    words: List[WordList] = field(default_factory=list)
    disallowed: str = ''
