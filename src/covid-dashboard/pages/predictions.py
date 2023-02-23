from taipy.gui import Markdown
from taipy.config import Config
import taipy as tp 
import pandas as pd

import datetime as dt

Config.load('config/config.toml')
scenario_cfg = Config.scenarios['scenario']

scenario_selector = [(s.id, s.name) for s in tp.get_scenarios()]
selected_scenario = None
selected_date = dt.datetime(2020,10,1)

scenario_country = "No selected scenario"
scenario_date = "No selected scenario"
scenario_name = ""

result = pd.DataFrame({"Date":[dt.datetime(2020,1,1)],
                       "Deaths_x":[0],"Deaths_y":[0],
                       "Predictions_x":[0],"Predictions_y":[0]})

def create_new_scenario(state):
    # 1) create the scenario based on scenario_cfg with a name
    # 2) add scenario in list of scenarios
    # 3) change state.selected_scenario
    # 4) write in country Data Node, the selected country
    # 5) write in country Data Node, the selected date
    # 6) actualize the graph with actualize_graph
    ...
        

def submit_scenario(state):
    # 1) get the selected scenario
    # 2) write in country Data Node, the selected country
    # 2) write in country Data Node, the selected date
    # 3) submit the scenario
    # 4) actualize the graph with actualize_graph
    ...

def actualize_graph(state):
    # 1) get scenario
    # 2) read result arima and linear
    # 3) concatenate to change state.result
    # 4) change selected_country and scenario_date with the predicted country of the scenario
    ...

predictions_md = Markdown("""
# Prediction page
  
## Scenario Creation
  
<|layout|columns=5 5 5 5|
**Scenario Name** <br/>
<|{scenario_name}|input|label=Name|> <br/> <|Create|button|on_action=create_new_scenario|>

**Prediction Date** <br/>
<|{selected_date}|date|label=Prediction date|>
<br/>
<|Submit|button|on_action=submit_scenario|>

<|{selected_country}|selector|lov={selector_country}|dropdown|on_change=on_change_country|label=Country|>
|>

---------------------------------------

## Result

<|layout|columns=2 3 3|
<|{selected_scenario}|selector|lov={scenario_selector}|on_change=actualize_graph|dropdown|value_by_id|label=Scenario|> 

### Country of prediction : <|{scenario_country}|>

### Date of prediction : <|{scenario_date}|>
|>
<br/>

<|{result}|chart|x=Date|y[1]=Deaths_x|type[1]=bar|y[2]=Predictions_x|y[3]=Predictions_y|>
""")