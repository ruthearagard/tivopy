# Copyright 2020 Michael Rodriguez
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
# REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
# AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
# INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
# LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
# OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
# PERFORMANCE OF THIS SOFTWARE.

from PySide2.QtCore import QObject, QTimer, Slot
from PySide2.QtWidgets import QInputDialog, QLineEdit, QMessageBox

from .change_channel import ChangeChannel
from .main_window import MainWindow
from .select_tivo import SelectTiVoWidget
from .tivo_discovery import TiVoDiscovery
from .tivo_client import TiVoClient

class TiVoPy(QObject):
    """Main program controller."""
    def __init__(self):
        super(TiVoPy, self).__init__()

        # The main window will need to be referenced in `connect_to_tivo()`,
        # but it doesn't actually exist yet.
        self.main_window = None

        # The first thing we do is allow the user to select a TiVo to connect
        # to. This will govern the rest of the program startup routine.
        self.select_tivo()
    
    @Slot()
    def select_tivo(self):
        """
        Called at either program startup to select a TiVo or when the user
        wishes to change to a different TiVo.
        """
        self.tivo_discovery = TiVoDiscovery()

        self.select_tivo_widget = SelectTiVoWidget()
        self.select_tivo_widget.connect_to_tivo.connect(self.connect_to_tivo)

        # Discover TiVos on the local network every 5 seconds.
        self.discovery_timer = QTimer(self)
        self.discovery_timer.timeout.connect(self.discover_tivos)
        self.discovery_timer.start(5000)

        self.select_tivo_widget.show()

    @Slot(str)
    def send_command(self, command):
        """
        Called when the user presses a button on the virtual remote control.
        """
        self.client.send_command(command)

    @Slot(str, str)
    def connect_to_tivo(self, name, ip_address):
        """Called when the user wants to connect to a TiVo."""
        self.discovery_timer.stop()

        self.client = TiVoClient(ip_address)
        self.client.socket.errorOccurred.connect(self.socket_error)
        self.client.error_message.connect(self.error_message)
        self.client.channel_changed.connect(self.channel_changed)
        self.client.connection_error.connect(self.connection_error)

        # It's possible that this function was called during program startup,
        # so the main window may not be present yet.
        if not self.main_window:
            self.main_window = MainWindow()

            self.main_window.select_tivo.triggered.connect(self.select_tivo)
            self.main_window.input_text.triggered.connect(self.input_text)
            self.main_window.change_channel.triggered.connect(self.change_channel)

        self.main_window.setWindowTitle(f"TiVoPy - {name} ({ip_address})")

        self.main_window.command_requested.connect(self.send_command)

        self.select_tivo_widget.close()
        self.main_window.show()

    @Slot(str)
    def error_message(self, error):
        """Called when the TiVo sends us an error code."""
        text = ""

        if error == "NO_LIVE":
            text = "The DVR is not in live TV mode."
        elif error == "INVALID_CHANNEL":
            text = "Channel not found in TCD lineup."
        else:
            text = f'{error} reached.'

        QMessageBox.critical(self.main_window, "Error", text)

    @Slot()
    def change_channel(self):
        """
        Called when the user wishes to change the channel via the 'Change
        Channel' dialog. The user would have to do this especially if they want
        to forcibly change the channel, which involves stopping a recording if
        one is in progress.
        """
        self.change_channel = ChangeChannel()
        self.change_channel.change_channel.connect(self.on_change_channel)
        self.change_channel.show()

    @Slot()
    def on_change_channel(self, channel, stop_recording):
        # The TiVo must be in live TV mode for the command to succeed.
        #self.client.send_command("IRCODE LIVETV")

        if stop_recording:
            self.client.send_command(f"FORCECH {channel}")
        else:
            self.client.send_command(f"SETCH {channel}")

    @Slot()
    def socket_error(self):
        QMessageBox.critical(self.main_window,
                             "Network error",
                             self.client.socket.errorString())

    @Slot(str)
    def channel_changed(self, channel):
        """Called when the channel has been changed by any action."""
        self.main_window.update_channel(channel)

    @Slot()
    def input_text(self):
        text, ok = QInputDialog().getText(self.main_window,
                                          "Specify text",
                                          "Text:",
                                          QLineEdit.Normal)
    @Slot(str)
    def connection_error(self, error_string):
        QMessageBox.warning(self.main_window, "Network error", error_string)

    def discover_tivos(self):
        """
        Called every 5 seconds to add newly discovered TiVos to the select TiVo
        widget list.
        """
        self.select_tivo_widget.tivo_listings.clear()
    
        for name, ip_address in self.tivo_discovery.addresses:
            self.select_tivo_widget.add_tivo(name, ip_address)
