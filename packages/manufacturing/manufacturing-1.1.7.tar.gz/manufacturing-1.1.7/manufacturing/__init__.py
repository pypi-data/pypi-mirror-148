import importlib.metadata

from manufacturing.analysis import calc_ppk, suggest_control_limits
from manufacturing.data_import import import_csv, import_excel
from manufacturing.report import generate_production_report
from manufacturing.visual import (
    ppk_plot,
    cpk_plot,
    control_chart,
    control_plot,
    x_mr_chart,
    moving_range,
    xbar_r_chart,
    xbar_s_chart,
)


__all__ = [
    "suggest_control_limits",
    "calc_ppk",
    "ppk_plot",
    "cpk_plot",
    "control_chart",
    "control_plot",
    "x_mr_chart",
    "moving_range",
    "xbar_r_chart",
    "xbar_s_chart",
    "import_csv",
    "import_excel",
    "generate_production_report",
]

__version__ = importlib.metadata.version("manufacturing")
