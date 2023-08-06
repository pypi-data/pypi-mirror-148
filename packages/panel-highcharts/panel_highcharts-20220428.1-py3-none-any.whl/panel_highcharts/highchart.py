"""The HighChart pane enables you to use the Highchart chart in Panel """
import param
from panel.pane.base import PaneBase
from panel.util import lazy_load, string_types
from pyviz_comms import JupyterComm

from . import config  # pylint: disable=unused-import


class HighChart(PaneBase):
    """A Panel HighChart pane"""

    # Events: https://api.highcharts.com/highcharts/plotOptions.series.point.events
    object = param.Dict(
        default=None,
        doc="""
        The initial user configuration of the chart. Will reset the chart when ever a
        configuration is provided.""",
    )
    object_update = param.Dict(doc="""Incremental change to the initial user configuration.""")

    event = param.Dict(doc="""Events raised by the chart""", readonly=True)

    priority = None

    _rename = {"object": "config", "object_update": "config_update"}

    _updates = True

    @classmethod
    def applies(cls, obj):
        if isinstance(obj, (dict, string_types)):
            return 0
        return False

    def _get_model(self, doc, root=None, parent=None, comm=None):
        _BkHighChart = lazy_load(  # pylint: disable=invalid-name
            "panel_highcharts.models.highchart", "HighChart", isinstance(comm, JupyterComm)
        )
        props = self._process_param_change(self._init_params())
        if not "config_update" in props:
            props["config_update"] = self.object_update
        model = _BkHighChart(config=self.object, **props)
        root = root or model
        self._link_props(
            model,
            [
                "event",
            ],
            doc,
            root,
            comm,
        )
        self._models[root.ref["id"]] = (model, parent)
        return model

    def _update(self, ref=None, model=None):
        model.update(config=self.object, config_update=self.object_update)
