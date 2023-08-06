from .data import *
from .utils import *


@end_point
def beautiful_console(text, text_color=None, highlight_color=None, continuous_color=None, style=None, blink=False, text_color_degree=0, highlight_color_degree=0, continuous_color_degree=0, get_input=False):
    beautiful_text = ""

    if text_color is not None:
        try:
            beautiful_text += f"{text_colors[text_color][text_color_degree]};"
        except KeyError:
            raise AttributeError("\"%s\" doesn't exist in defined colors" % text_color)

    if highlight_color is not None:
        try:
            beautiful_text += f"{highlight_colors[highlight_color][highlight_color_degree]};"
        except KeyError:
            raise AttributeError("\"%s\" doesn't exist in defined highlight colors" % highlight_color)

    if style is not None:
        try:
            beautiful_text += f"{styles[style]};"
        except KeyError:
            raise AttributeError("\"%s\" doesn't exist in defined styles" % style)

    if blink:
        beautiful_text += f"{blink_code};"
        
    beautiful_text = beautiful_text[:len(beautiful_text)-1]
    beautiful_text = f"\u001b[{beautiful_text}m{text}\u001b[0m"
    
    if get_input is True or get_input == f"{get_input=}".split('=')[0]:
        if continuous_color is not None:
            try:
                beautiful_text += f"\u001b[{text_colors[continuous_color][continuous_color_degree]}m"
            except KeyError:
                raise AttributeError("\"%s\" doesn't exist in defined colors" % continuous_color)

    return beautiful_text
