from taipy.gui import Gui, notify
from math import cos, exp

value = 10

page = """
# Taipy *Demo*

The value is: <|{value*2}|>.


Interact: <|{value}|slider|>

<|{compute_data(value)}|chart|>
"""

def compute_data(decay):
    return [cos(i/6) * exp(-i*decay/600) for i in range(100)]

def on_change(state, var_name, var_value):
    if var_name == 'value':
        state.data = compute_data(var_value)

Gui(page).run(port=5025)