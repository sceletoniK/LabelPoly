import os
from enum import Enum
from pathlib import Path

from PyQt5.QtGui import QIcon, QPixmap

FILE = Path(__file__).resolve().parent


class IconsPath(Enum):
    drag = str(FILE / r"drag.png")
    insert = str(FILE / r'insert.png')
    next = str(FILE / r'next.png')
    open_folder = str(FILE / r'open_folder.png')
    open_single = str(FILE / r'open_single.png')
    prev = str(FILE / r'prev.png')
