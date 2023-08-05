#from core_gps_visualization_app.tasks import build_visualization_data
from core_gps_visualization_app.components.plots.operations import plot_layout_by_time_range
from core_gps_visualization_app.utils import data_utils as utils
from core_gps_visualization_app.data_config import info_id_legend

import logging
import param
import holoviews as hv
import time

logger = logging.getLogger(__name__)
hv.extension('bokeh')

# Init legend
legend_name = info_id_legend['legendName']
legend_path = info_id_legend['legendPath']
results = utils.query_data(legend_path)
for i in range(len(results)):
    results[i] = legend_name + ': ' + str(results[i])


class Chart(param.Parameterized):
    plot_selected = param.Selector(default="Scatter", objects=["Scatter", "Line"])
    time_selected = param.Selector(default="Seconds", objects=["Seconds", "Minutes", "Hours", "Days"])
    legend = param.ListSelector(default=results, objects=results)

    def __init__(self, **params):
        super().__init__(**params)

    @param.depends('plot_selected', 'time_selected', 'legend')
    def update_plot(self):
        self.plot_selected = self.plot_selected
        self.time_selected = self.time_selected
        self.legend = self.legend
        visualization_data = build_visualization_data(self.legend)
        if visualization_data is None:
            visualization_data = []
        if len(visualization_data) == 0:
            return '# No charts for this configuration...'
        chart = plot_layout_by_time_range(visualization_data, self.plot_selected, self.time_selected)

        return chart


def build_visualization_data(legend):
    """

    Returns: list of charts with same x and y but different ids and data

    """
    try:
        start_time = time.time()
        logger.info("Periodic task: START creating plots objects")

        x_parameter = api.get_x_parameter()
        y_parameter = api.get_y_parameter()
        data_sources = api.get_data_sources()

        # TODO: FIX Chart optimization
        # if api.plots_exist(x_parameter, y_parameter, data_sources):
        #    list_of_charts = api.get_plots_data(x_parameter, y_parameter, data_sources)
        #    return list_of_charts

        data = utils.get_all_data()

        list_of_charts = parse_data(data, x_parameter, y_parameter, data_sources, legend)

        # TODO: FIX Chart optimization
        # api.create_plots(list_of_charts, x_parameter, y_parameter, data_sources)

        logger.info("Periodic task: FINISH creating plots objects " +
                    "(" + str((time.time() - start_time) / 60) + "minutes)")

        return list_of_charts

    except Exception as e:
        logger.error("An error occurred while creating plots objects: " + str(e))