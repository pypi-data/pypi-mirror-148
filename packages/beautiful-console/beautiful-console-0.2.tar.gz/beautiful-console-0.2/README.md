# Beautiful Console

## installation :

install :
>pip install beautiful-console

import :
```python
from beautiful_console.beautiful_console import *
```
## List of Functions :
- to_color()
- to_highlight()
- to_style()

## defined colors : 
>black, red, green, yellow, blue, magenta, cyan, white


## defined highlight colors : 
>black, red, green, yellow, blue, magenta, cyan, white


## defined styles :
>**bold**, _italic_, underline, underline_bold, overline, ~~strikethrough~~

<br><br>

## to_color()
Returns colored text.

```python
# only text-parameter and color-parameter must be filled (degree-parameter have default value).

print(to_highlight(
    "text",
    "color", # color of text
    "degree" # intensity of text color <0 or 1>
))
```
---
## to_highlight()
Returns highlighted text.

```python
# only text-parameter must be filled (others have default value).

print(to_highlight(
    "text",
    "highlight_color", # color of background
    "text_color", # color of text
    "highlight_color_degree", # intensity of background color <0 or 1>
    "text_color_degree" # intensity of text color <0 or 1>
))
```
---
## to_style()
Returns styled text.

```python
# only text-parameter and style-parameter must be filled (others have default value).

print(to_style(
    "text",
    "style", # style of text
    "color", # color of text
    "degree" # intensity of text color <0 or 1>
))
```
---
# Tips :
>**Tip** : some things may not work on some consoles.

### Things that may not work on all consoles :
- "underline_bold" style 
    - "underline_bold" bolds under line of text (not text, just under line of text).
- setting **background color** and **text color** together.

---
send your feedbacks to : pourya90091@gmail.com