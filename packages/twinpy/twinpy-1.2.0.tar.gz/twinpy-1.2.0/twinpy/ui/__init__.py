"""TwinPy.UI module.

These imports allow the user to skip the file names in their import.
"""

from .tc_base import TcWidget
from .tc_widgets import (
    TcLabel,
    TcPushButton,
    TcLineEdit,
    TcRadioButton,
    TcRadioButtonGroupBox,
    TcCheckBox,
    TcSlider,
    TcGraph,
    TcMainWindow,
)
from .custom_widgets import (
    ScrollLabel,
    GraphWidget,
)
from .base_widgets import (
    TcErrorsLabel,
    ErrorPopupWindow,
    DrivesWidget,
    ErrorsWidget,
    SystemBackpackWidget,
    SystemWRBSWidget,
)
from .base_gui import BaseGUI
from .tabs import ConsoleTab, FirmwareTab
