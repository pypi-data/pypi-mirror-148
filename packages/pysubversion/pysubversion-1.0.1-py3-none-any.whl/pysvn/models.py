from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto
from typing import List

@dataclass
class LogEntry:
    message: str
    author: str
    revision: str
    date: datetime

@dataclass
class SVNItemPath:
    item: str
    props: str
    kind: str
    filepath: str

@dataclass
class Diff:
    paths: List[SVNItemPath]
