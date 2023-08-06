# Beautiful Console

## installation :

install :
```bash
pip install beautiful-console
```

import :
```python
from beautiful_console.beautiful_console import beautiful_console
```

## defined text colors : 
>black, red, green, yellow, blue, magenta, cyan, white


## defined highlight colors : 
>black, red, green, yellow, blue, magenta, cyan, white


## defined styles :
>**bold**, _italic_, underline, underline_bold, overline, ~~strikethrough~~

<br>

## beautiful_console()
Returns beautiful text.

```python
# only the text-parameter is required, then you can use any option you need

print(beautiful_console(
    "text",
    "text_color", # color of text
    "highlight_color", # color of background
    "style", # style of text
    "blink", # blinking text <True or False>
    "text_color_degree", # intensity of text color <0 or 1>
    "highlight_color_degree" # intensity of background color <0 or 1>
))
```

>**Tip** : some things may not work on some consoles.
---
send your feedbacks to : pourya90091@gmail.com