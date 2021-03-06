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

from PySide2.QtCore import QByteArray, QObject, Signal
from PySide2.QtNetwork import QTcpSocket

class TiVoClient(QObject):
    """Implements the TiVo version 1.1 TCP Remote Protocol."""
    channel_changed = Signal(str)
    error_message = Signal(str)
    connection_error = Signal(str)

    def __init__(self, ip):
        super(TiVoClient, self).__init__()

        self.socket = QTcpSocket(self)

        # TiVos *always* serve on port 31339. 
        self.socket.connectToHost(ip, 31339)

        self.socket.readyRead.connect(self.handle_read)

    def send_command(self, command):
        print(f'Sending {command}...')

        # All commands are terminated with a carriage return. The end user
        # shouldn't have to care about this detail.
        command += "\r"

        data = QByteArray(bytes(command, encoding='ascii'))

        sent_bytes = self.socket.write(data)
        data_len = len(data)

        if sent_bytes != data_len:
            error_string = "Network error: Not all of the data was sent.\n\n" \
                           f"Command: {command}\n" \
                           f"Number of bytes sent: {sent_bytes}\n" \
                           f"Expected: {data_len}"
            self.connection_error.emit(error_string)

    def handle_read(self):
        """Handles data received by the socket."""

        # Grab the data from the socket.
        data = self.socket.readAll().data()

        # Remove whitespace from the data.
        data = data.strip()

        # Convert the data to a string.
        data = data.decode('utf-8')

        print(f"Received {data}")

        # Parameterize the string.
        data = data.split(' ')

        if data[0] == "CH_STATUS":
            self.channel_changed.emit(data[1])
        elif data[0] == "CH_FAILED":
            self.error_message.emit(data[1])
        else:
            self.error_message.emit(data[0])