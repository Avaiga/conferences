import taipy as tp
from backend.config import *

Config.configure_global_app(clean_entities_enabled=True)
tp.clean_all_entities()

def create_scenario(date: dt.datetime):
    scenario = tp.create_scenario(config=scenario_cfg, name="scenario_" + str(date.date()))
    scenario.day.write(date)
    tp.submit(scenario)
    return scenario


if __name__ == "__main__":
    my_first_scenario = create_scenario(dt.datetime(2021, 1, 25))
    
    predictions = my_first_scenario.baseline.predictions.read()
    print("Predictions\n",predictions)  
    
    for i in range(1,10):
        print("Creating scenario for day: ", i)
        date = dt.datetime(2021, 1, 25) + dt.timedelta(days=10*i)
        create_scenario(date)
    
    maes = []
    names = []
    
    for scenario in tp.get_scenarios():
        evaluation = scenario.evaluation.read()
        print(f"\nscenario : {scenario.name}")
        print(f"Metric: {evaluation}")
    
        maes.append(evaluation)
        names.append(scenario.name)

    from taipy.gui import Gui
    df_metrics = pd.DataFrame({"Names": names, "MAE": maes})
    Gui('<|{df_metrics}|chart|x=Names|y=MAE|type=bar|>').run(port=5006, use_reloader=False)
