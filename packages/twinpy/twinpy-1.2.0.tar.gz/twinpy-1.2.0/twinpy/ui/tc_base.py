"""This file defines abstract and helper classes for TcWidgets.
"""

from typing import Optional, Any, Tuple, Union, Callable, List, Dict
from abc import ABC, abstractmethod, ABCMeta
import time
import os
from PyQt5.QtWidgets import QWidget, QMessageBox, QApplication
from PyQt5.QtCore import pyqtSlot, QTimer
from pyads import ADSError

from ..twincat.connection import TwincatConnection
from ..twincat.symbols import Symbol


PACKAGE_DIR = os.path.abspath(os.path.dirname(__file__) + "/../..")


class QABCMeta(ABCMeta, type(QWidget)):
    """Create a meta class that combines ABC and the Qt meta class."""


class TcWidget(ABC, metaclass=QABCMeta):
    """Abstract class, to be multi-inherited together with a Qt item.

    There are different event types, which determine how and when new remote
    values are retrieved:

        * `EVENT_NOTIFICATION`: An ADS notification is created, resulting in a
          callback on a remote value change. Suitable for rarely changing values or
          when a very quick response is needed.
          ADS notifications have some overhead. No more than 200 symbol
          notifications should exist at the same time.
        * `EVENT_TIMER`: New values are read at a fixed interval. Useful when
          remote values change often but no instant response is needed. This
          method has very little overhead.
        * `EVENT_NONE`: No attempts are made to update according to remote values.

    You can override the defaults for your entire project by changing the
    ``TcWidget.DEFAULT_EVENT_TYPE`` and ``TcWidget.DEFAULT_UPDATE_FREQ``
    class properties. Make sure to update these before any widgets are
    created and they will have new standard values.

    :cvar DEFAULT_EVENT_TYPE: (default: EVENT_NOTIFICATION)
    :cvar DEFAULT_UPDATE_FREQ: (default: 10.0 Hz)
    """

    EVENT_NOTIFICATION = "notification"
    EVENT_TIMER = "timer"
    EVENT_NONE = "none"

    DEFAULT_EVENT_TYPE = EVENT_NOTIFICATION
    DEFAULT_UPDATE_FREQ = 10.0  # Hz

    _TIMERS: Dict[int, QTimer] = {}  # Store timers, keyed by interval in ms

    def __init__(self, *args, **kwargs):
        """

        It is important to call this init() as late as possible from a
        subclass! The order should be:

           1. Subclass specific stuff (e.g. number formatting)
           2. Call to super().__init__(...) - Now the QWidget stuff has been
              made ready
           3. QWidget related stuff

        Note: these methods do not affect when or how a value is _written_ to the ADS
        pool.

        :param args:
        :param kwargs: See list below - kwargs are passed along to
            `connect_symbol` too

        :kwargs:
            * `symbol`: ``Symbol`` to link to
                        (i.e. to read from and/or write to)
            * `format`: Formatter symbol, e.g. '%.1f' or '%d' or callable
                        ('%.3f' by default, ignored when not relevant)
                        Callable must have a single argument
            * `event_type`:     Possible values are EVENT_* constants
                                (default: ``DEFAULT_EVENT_TYPE``)
            * `update_freq`:    Frequency (Hz) for timed update
                                (for EVENT_TIMER only, default: ``DEFAULT_UPDATE_FREQ``)
            * `greyed`:         When true, the widget is visibly disabled
                                When false, the widget is shown normally even when
                                disconnected (default: `true`)

        """

        self._symbol: Optional[Symbol] = kwargs.pop("symbol", None)
        # Included None fallback

        self.value_format: Union[str, Callable[[Any], str]] = kwargs.pop(
            "format", "%.3f"
        )

        self.event_type = kwargs.pop("event_type", self.DEFAULT_EVENT_TYPE)

        self.update_freq = kwargs.pop("update_freq", self.DEFAULT_UPDATE_FREQ)

        self.greyed = kwargs.pop("greyed", True)

        self._handles: Optional[Tuple[int, int]] = None
        # Handles to the notification specific for this widget

        self._skip_event: bool = False  # If true, QWidget events should not result in
        # a change of the ADS symbol

        self._last_update: Optional[float] = None  # Timestamp of the last successful
        # twincat_send(), used to prevent an event loop

        self._timer: Optional[TcTimer] = None  # Reference to the linked TcTimer
        self._last_value: Optional[Any] = None  # For timed event loop

        # Disable widget
        if self.greyed:
            self.setDisabled(True)

        if self._symbol:
            self.connect_symbol(self._symbol, **kwargs)
            # Connect already if passed

    def connect_symbol(self, new_symbol: Optional[Symbol] = None, **kwargs):
        """Connect a symbol (copy is left as property).

        By default a device callback is created with an on-change event
        from TwinCAT.
        Old callbacks are deleted first. Pass None to only clear callbacks.
        The notification handles are stored locally.
        Extend (= override but call the parent first) this method to
        configure more of the widget, useful if e.g. widget callbacks depend
        on the symbol.

        :param new_symbol: Symbol to link to (set None to only clear the
            previous)
        :param kwargs: See list below - Keyword arguments are passed along as
            device notification settings too

        :kwargs:
            * `event_type`:     See :class:`TcWidget`
            * `update_freq`:    See :class:`TcWidget`
        """

        if self._symbol is not None:
            if self._handles is not None:
                self._symbol.del_device_notification(self._handles)
                # In case previous callback existed, clear it
                self._handles = None

            if self._timer is not None:
                self._timer.remove_widget(self)
                if self._timer.get_number_of_widgets() == 0:
                    del self._TIMERS[self._timer.interval()]
                self._timer = None  # Clear reference

        self._symbol = new_symbol

        if "event_type" in kwargs:
            self.event_type = kwargs.pop("event_type")
        if "update_freq" in kwargs:
            self.update_freq = kwargs.pop("update_freq")

        if new_symbol is None:
            if self.greyed:
                self.setDisabled(True)
        else:
            connected = True  # New connected state
            if self.event_type == self.EVENT_NOTIFICATION:
                self._handles = self._symbol.add_device_notification(
                    self.twincat_receive_wrapper, **kwargs
                )
                # It seems a notification is always fired on creation, so we don't
                # need to call it now
                if self._handles is None:  # In case the callback quietly failed
                    connected = False

            elif self.event_type == self.EVENT_TIMER:
                m_sec = int(1000 / self.update_freq)
                if m_sec not in self._TIMERS:
                    plc = (
                        self._symbol[0]._plc
                        if isinstance(self._symbol, list)
                        else self._symbol._plc
                    )
                    self._TIMERS[m_sec] = TcTimer(plc, m_sec)
                self._timer = self._TIMERS[m_sec]  # Keep local reference
                self._timer.add_widget(self)

            elif self.event_type == self.EVENT_NONE:
                pass  # Nothing to be done

            else:
                ValueError("Unrecognized event type: " + self.event_type)

            if self.greyed and connected:
                self.setDisabled(False)

    def twincat_receive_wrapper(self, value):
        """Intermediate twincat_receive callback to prevent event loops."""

        # If incoming value equals old buffered value
        if value == self._symbol.value and self._last_update is not None:

            elapsed_ms = (time.time() - self._last_update) * 1000
            if elapsed_ms < 50:
                # If within 50 ms of the last update, discard this notification
                # This is typically a callback after a twincat_send()
                return

        self.twincat_receive(value)

    def on_mass_timeout(self):
        """Callback for the event timer.

        This assumes the remote read was already performed!
        """
        # We use the buffered _symbol.value (assume it was updated externally)
        # This is slightly risky, because the buffered value could be changed by
        # something else too
        new_val = self._symbol._value
        if new_val != self._last_value:
            # Trigger incoming-value callback
            self.twincat_receive(new_val)
            self._last_value = new_val

    @abstractmethod
    def twincat_receive(self, value):
        """Callback attached to the TwinCAT symbol.

        Note: changing a state of a widget (e.g. checkbox being checked through
        `setChecked(True)`) will typically fire the on-change events again. So be
        careful to prevent an event loop when updating a widget based on a remote
        change: a change could result in a state change, which could result in a
        remote change, etc.

        :param value: New remote value
        """

    def twincat_send(self, value: Any):
        """Set value in symbol (and send to TwinCAT).

        Method is safe: if symbol is not connected, nothing will happen.
        """
        self._last_update = time.time()  # Current floating point timestamp

        if self._symbol is not None:  # Safe for unconnected symbols
            try:
                self._symbol.set(value)
            except ADSError as err:
                TcWidget.close_with_error(err)

    def format(self, value: Any) -> str:
        """ "Use the stored formatting to created a formatted text.

        In case the format specifier is a string and the new value is a list,
        element-wise string formatting will be concatenated automatically.
        """
        if isinstance(self.value_format, str):
            if isinstance(value, list):
                elements = [self.value_format % item for item in value]
                return ", ".join(elements)

            return self.value_format % value

        if callable(self.value_format):
            return self.value_format(value)

        raise NotImplementedError(
            "The format `{}` could not be processed".format(self.value_format)
        )

    @staticmethod
    def close_with_error(err: Exception):
        """Show an error popup and close the active application.

        This uses `QApplication.instance()` to find the current application and won't
        work perfectly.
        """

        print(err)

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("ADS Error")
        msg.setInformativeText(str(err))
        msg.setWindowTitle("ADS Error")
        msg.exec_()

        app = QApplication.instance()
        if app is not None:
            app.exit(1)

    def __del__(self):
        """Destructor."""

        if self._symbol is not None:
            try:
                # Element is about to become extinct, so clear callbacks
                self._symbol.clear_device_notifications()
            except (ADSError, KeyError):
                pass  # Quietly continue, nothing we could do now


class TcTimer(QTimer):
    """Timer object which can trigger an update for multiple TcWidgets.

    Uses reading by list to get multiple values using a single request.

    A single instance of this class should be made per update rate. Additional
    TcWidgets can then be registered to existing timer instances.
    """

    def __init__(self, plc: TwincatConnection, rate: int):
        """

        :param plc: Twincat connection object - a reference will be kept
        :param rate: Update rate in milliseconds
        """

        super().__init__()

        self._plc = plc

        self.setInterval(rate)

        self.timeout.connect(self.on_timeout)

        self.widgets: List[TcWidget] = []  # List of linked widgets
        self.symbols: List[Symbol] = []  # List of symbols of those widgets

    @pyqtSlot()
    def on_timeout(self):
        """Callback for this timer.

        Will do combined update for all linked widgets.
        """

        try:
            # Perform combined read
            self._plc.read_list_of_symbols(self.symbols)
            # This will update all the `_value` properties of the symbols
        except ADSError as err:
            self.stop()
            TcWidget.close_with_error(err)
            return  # Abort this loop

        # Trigger updates for all linked widgets
        for widget in self.widgets:
            widget.on_mass_timeout()

    def add_widget(self, widget: TcWidget):
        """Register a new widget to be updated by this timer.

        Start timer if it wasn't running yet.

        :param widget: New widget
        """
        self.widgets.append(widget)

        new_symbol = widget._symbol

        # We will keep a ready array of symbols so we won't have to find them on
        # every timeout. This should be a little bit faster
        if isinstance(new_symbol, list):
            for sym in new_symbol:
                self.symbols.append(sym)
        elif new_symbol is not None:
            self.symbols.append(new_symbol)

        if not self.isActive():
            self.start()

        return len(self.widgets)

    def remove_widget(self, widget: TcWidget):
        """De-register a new widget from this timer.

        Will also stop timer if no widgets remain.

        :param widget: Widget to remove
        """
        self.widgets.remove(widget)

        symbol = widget._symbol

        # We will keep a ready array of symbols so we won't have to find them on
        # every timeout. This should be a little bit faster
        if isinstance(symbol, list):
            for sym in symbol:
                self.symbols.remove(sym)
        elif symbol is not None:
            self.symbols.remove(symbol)

        if not self.widgets:
            self.stop()  # Stop timer if no widgets remain

    def get_number_of_widgets(self) -> int:
        """
        :return: Number of linked widgets
        """
        return len(self.widgets)
