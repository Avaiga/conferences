import numpy as np

import taipy as tp
from taipy.gui import Gui

from pages.country import country_md, on_change_country, selected_representation, data_country_date, pie_chart
from pages.world import world_md
from pages.map import map_md
from pages.predictions_sol import predictions_md

from data.data import data


selector_country = list(np.sort(data['Country/Region'].astype(str).unique()))
selected_country = 'France'

pages = {
    "/":"<|navbar|>",
    "Country":country_md,
    "World":world_md,
    "Map":map_md,
    "Predictions":predictions_md
}

tp.Core().run()
gui_multi_pages = Gui(pages=pages)

if __name__ == '__main__':
    gui_multi_pages.run(title="Covid Dashboard",
    		            dark_mode=False,
                        use_reloader=True,
                        port=5039)