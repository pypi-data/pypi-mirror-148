colors = {
    "black": (30, 90),
    "red": (31, 91),
    "green": (32, 92),
    "yellow": (33, 93),
    "blue": (34, 94),
    "magenta": (35, 95),
    "cyan": (36, 96),
    "white": (37, 97)
}

highlight_colors = {
    "black": (40, 100),
    "red": (41, 101),
    "green": (42, 102),
    "yellow": (43, 103),
    "blue": (44, 104),
    "magenta": (45, 105),
    "cyan": (46, 106),
    "white": (47, 107)
}

styles = {
    "bold": 1,
    "italic": 3,
    "underline": 4,
    "underline_bold": 21,
    "overline": 53,
    "strikethrough": 9
}


def to_color(text, color, degree=0):
    if color in colors:
        return "\u001b[%sm%s\u001b[0m" % (
            colors[color][degree],
            text
        )
    else:
        raise AttributeError(f"\"{color}\" doesn't exist in defined colors")


def to_highlight(text, highlight_color="white", text_color="black", highlight_color_degree=0, text_color_degree=0):
    if highlight_color in highlight_colors:
        if text_color in colors:
            return "\u001b[%s;%sm%s\u001b[0m" % (
                highlight_colors[highlight_color][highlight_color_degree],
                colors[text_color][text_color_degree],
                text
            )
        else:
            raise AttributeError("\"%s\" doesn't exist in defined colors" % text_color)
    else:
        raise AttributeError("\"%s\" doesn't exist in defined colors" % highlight_color)


def to_style(text, style, color="white", degree=0):
    if color in colors:
        if style in styles:
            return "\u001b[%s;%sm%s\u001b[0m" % (
                styles[style],
                colors[color][degree],
                text
            )
        else:
            raise AttributeError("\"%s\" doesn't exist in defined styles" % style)
    else:
        raise AttributeError("\"%s\" doesn't exist in defined colors" % color)
