import inspect
import sys
from attr import (field, ib)
from attrs import define

import copy

from grafanalib.core import (Panel, GridPos, Dashboard)

from .helpers import gen_random_str

GRAFANA_DASHBOARD_SCREEN_WIDTH = 24

@define
class Row:
    """
    Panel Row

    :param height: row height
    :param panel_list: list of panels
    """

    height: int
    panel_list: list[Panel]

    def __init__(self, height: int, *args: Panel):
        self.height = height
        self.panel_list = args

    def to_panels(self, y: int):
        panel_width_int = int(
            GRAFANA_DASHBOARD_SCREEN_WIDTH / len(self.panel_list))
        auto_panel_list = []
        x_int = 0

        for panel in self.panel_list:
            panel_copy = copy.deepcopy(panel)
            auto_panel_list.append(panel_copy)
            panel_copy.gridPos = GridPos(
                h=self.height,
                w=panel_width_int,
                x=x_int,
                y=y)
            x_int += panel_width_int

        return auto_panel_list


@define
class Stack:
    """
    Panel Stack (of Rows)

    :param rows: list of rows

    """
    rows: list[Row]

    def __init__(self, *args: Row):
        self.rows = args

    def to_panels(self):
        y_int = 0
        panels = []
        for row in self.rows:
            panels += row.to_panels(y_int)
            y_int += row.height

        return panels


@define
class GritDash(Dashboard):
    """
    Compose dashboard from Stack

    :param stack: stack of panel rows
    :param dataSource: dataSource for panels
    :param register: automatically register the dashboard

    """
    stack: Stack = ib(default=False)
    dataSource: str = ib(default=False)
    panels: list[Panel] = field(default=[])
    register: bool = True

    def __init__(self, **kwargs):
        self.__attrs_init__(**kwargs)
        caller = inspect.currentframe().f_back
        caller_module = sys.modules[caller.f_globals['__name__']]
        setattr(caller_module, f"__dashboard__{gen_random_str()}", self)

    def __attrs_post_init__(self):
        def dataSource_override(p: Panel):
            if p.dataSource == None:
                p.dataSource = self.dataSource
            return p

        self.panels = list(map(dataSource_override, self.stack.to_panels()))
