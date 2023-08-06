from enum import Enum, auto


class Depth(Enum):
    EMPTY = 'empty'
    FILES = 'files'
    IMMEDIATES = 'immediates'
    INFINITY = 'infinity'

class Revision(Enum):
    HEAD = auto()
    BASE = auto()
    COMMITTED = auto()
    PREV = auto()

class CRAction(Enum):
    """Automatic conflict resolution action."""
    POSTPONE = 'postpone'
    WORKING = 'working'
    BASE = 'base'
    MINE_CONFLICT = 'mine-conflict'
    THEIRS_CONFLICT = 'theirs-conflict'
    MINE_FULL = 'mine-full'
    THEIRS_FULL = 'theirs-full'