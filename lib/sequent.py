from manimlib.imports import *
from typing import List, Dict, Tuple

# A basic sequent, used as a node in the larger proof
# Supports formatting with colors
class Sequent(TexMobject):
    CONFIG = {
        "color": BLACK,
        "background_stroke_width": 0
    }

    def __init__(self, colored_tex: str, **kwargs):
        digest_config(self, kwargs)
        split, color_indexes = self.parse_colors(colored_tex)
        TexMobject.__init__(self, *split, **kwargs)

        for i, color in color_indexes.items():
            self[i].set_color(color)

    # Simple parse for the color markup in strings
    def parse_colors(self, colored_tex: str) -> Tuple[List[str], Dict[int, str]]:
        colors = {
            "b": "#2681ff",
            "r": "#ed0000"
        }

        tokens: List[str] = []
        current_token = ""

        for i in range(len(colored_tex)):
            c = colored_tex[i]

            if c in colors.keys():
                if colored_tex[i + 1] == "<":
                    if current_token != "":
                        tokens.append(current_token)

                    current_token = "#" + c
                else:
                    current_token += c
            elif c == ">":
                tokens.append(current_token)
                current_token = ""
            elif c != "<":
                current_token += c
        
        if current_token != "":
            tokens.append(current_token)

        split_text: List[str] = []
        color_indexes: Dict[int, str] = {}

        for i in range(len(tokens)):
            token = tokens[i]

            if token[0] == "#":
                color_indexes[i] = colors[token[1]]
                split_text.append(token[2:])
            else:
                split_text.append(token)
        
        return (split_text, color_indexes)