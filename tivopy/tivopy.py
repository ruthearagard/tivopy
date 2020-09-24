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

from threading import Timer
from PySide2.QtCore import QObject, Slot

from .main_window import MainWindow
from .select_tivo import SelectTiVoWidget
from .tivo_discovery import TiVoDiscovery
from .tivo_client import TiVoClient

class TiVoPy(QObject):
    """Main program controller."""
    def __init__(self):
        super(TiVoPy, self).__init__()
    
        self.tivo_discovery = TiVoDiscovery()

        # The first thing we do is allow the user to select a TiVo to connect
        # to.
        self.select_tivo_widget = SelectTiVoWidget()
        self.select_tivo_widget.show()

        self.select_tivo_widget.connect_to_tivo.connect(self.connect_to_tivo)
        Timer(5.0, self.discover_tivos).start()

    @Slot(str)
    def send_command(self, command):
        """
        Called when the user presses a button on the virtual remote control.
        """
        self.client.send_command(command)

    @Slot(str, str)
    def connect_to_tivo(self, name, ip_address):
        self.client = TiVoClient(ip_address)
        self.client.channel_changed.connect(self.channel_changed)

        self.main_window = MainWindow()
        self.main_window.setWindowTitle(f"TiVoPy - {name} ({ip_address})")

        self.main_window.command_requested.connect(self.send_command)

        self.main_window.update_connected_to(name, ip_address)

        self.select_tivo_widget.close()
        self.main_window.show()

    @Slot(tuple)
    def channel_changed(self, channel):
        """Called when the channel has been changed by any action."""
        self.main_window.update_channel(channel[0], channel[1])

    def discover_tivos(self):
        for name, ip_address in self.tivo_discovery.addresses:
            self.select_tivo_widget.add_tivo(name, ip_address)
