from data import *


def beautiful_console(text, text_color=None, highlight_color=None, style=None, blink=False, text_color_degree=0, highlight_color_degree=0):
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
    beautiful_text += f"m{text}"

    return f"\u001b[{beautiful_text}\u001b[0m"
