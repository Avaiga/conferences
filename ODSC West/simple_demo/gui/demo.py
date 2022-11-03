from taipy.gui import Gui, notify
from math import cos, exp


value = 10

page = """
Markdown
# Taipy *Demo*

Value: <|{value}|text|>

<|{value}|slider|>

<|{compute_data(value)}|chart|>
"""

def compute_data(decay):
    return [cos(i/6) * exp(-i*decay/600) for i in range(100)]


Gui(page).run(port=5099,
              async_mode="threading",
              use_reloader=True,
              dark_mode=False)