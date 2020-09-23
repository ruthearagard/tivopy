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
    def __init__(self):
        super(TiVoPy, self).__init__()
    
        self.tivo_discovery = TiVoDiscovery()
    
        self.select_tivo_widget = SelectTiVoWidget()

        self.select_tivo_widget.setWindowTitle("Select TiVo")
        self.select_tivo_widget.resize(512, 384)

        self.select_tivo_widget.show()

        self.select_tivo_widget.connect_to_tivo.connect(self.connect_to_tivo)

        Timer(5.0, self.discover_tivos).start()

    @Slot(str)
    def connect_to_tivo(self, ip_address):
        self.client = TiVoClient(ip_address)
        self.client.channel_changed.connect(self.channel_changed)

        self.main_window = MainWindow()

        self.main_window.resize(800, 600)
        self.main_window.setWindowTitle("TiVoPy")

        self.select_tivo_widget.close()
        self.main_window.show()

    @Slot(tuple)
    def channel_changed(self, channel):
        print("Channel changed: %s %s", channel[0], channel[1])

    def discover_tivos(self):
        for name, ip_address in self.tivo_discovery.addresses:
            self.select_tivo_widget.add_tivo(name, ip_address)