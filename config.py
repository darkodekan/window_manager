from Xlib import XK, X
from enum import Enum, auto

BORDER_WIDTH = 2

wallpaper = ""

class Commands(Enum):
    DESTROY_WINDOW = auto()
    MOVE_LEFT = auto()
    MOVE_DOWN = auto()
    MOVE_UP = auto()
    MOVE_RIGHT = auto()
    RESIZE_RIGHT = auto()

key_mappings = [
    [(X.Mod4Mask, XK.XK_Return), "xterm" ],
    [(X.Mod4Mask, XK.XK_Q), Commands.DESTROY_WINDOW ],
    [(X.Mod4Mask, XK.XK_Right), Commands.MOVE_RIGHT ],
    [(X.Mod1Mask, XK.XK_Right), Commands.RESIZE_RIGHT ]


]

