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

from PySide2.QtCore import QObject, Signal
from PySide2.QtNetwork import QTcpSocket

class TiVoClient(QObject):
    """Implements the TiVo version 1.1 TCP Remote Protocol."""
    channel_changed = Signal(tuple)
    error_message = Signal(str)

    def __init__(self, ip):
        super(TiVoClient, self).__init__()

        self.socket = QTcpSocket(self)
        self.socket.connectToHost(ip, 31339)

        self.socket.readyRead.connect(self.handle_read)

    def ircode(self, code):
        pass

    def keyboard(self, code):
        pass

    def setch(self, channel, sub_channel=0):
        if sub_channel != 0:
            self.socket.write("SETCH %d %d" % channel, sub_channel)
        else:
            self.socket.write("SETCH %d" % channel)

    def forcech(self, channel, sub_channel=0):
        if sub_channel != 0:
            self.socket.write("FORCECH %d %d" % channel, sub_channel)
        else:
            self.socket.write("FORCECH %d" % channel)

    def teleport(self, screen):
        """Forcibly changes the DVR to a specific screen."""
        pass

    def handle_read(self):
        """Handles data received by the socket."""

        # Grab the data from the socket.
        data = self.socket.readAll().data()

        # Remove whitespace from the data.
        data = data.strip()

        # Convert the data to a string.
        data = data.decode('utf-8')

        # Parameterize the string.
        data = data.split(' ')

        if data[0] == "CH_STATUS":
            if len(data) == 4:
                self.channel_changed.emit((data[1], data[3]))
            else:
                self.channel_changed.emit((data[1], data[2]))
        elif data[0] == "CH_FAILED":
            self.error_message.emit(data[1])
        elif data[0] == "LIVETV_READY":
            pass
        elif data[0] == "MISSING_TELEPORT_NAME":
            pass