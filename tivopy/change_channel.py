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

from PySide2.QtCore import Qt, Signal, Slot
from PySide2.QtWidgets import (QCheckBox,
                               QDialog,
                               QDialogButtonBox,
                               QFormLayout,
                               QSpinBox)

class ChangeChannel(QDialog):
    change_channel = Signal(int, int, bool)

    """Allows the user to change the channel."""
    def __init__(self):
        super(ChangeChannel, self).__init__()

        self.setModal(True)

        self.stop_recording = QCheckBox(self)
        self.channel = QSpinBox(self)

        self.sub_channel = QSpinBox(self)
        self.sub_channel.setValue(1)

        self.channel.setRange(0, 9999)
        self.sub_channel.setRange(0, 9999)

        self.button_boxes = QDialogButtonBox(QDialogButtonBox.Ok |
                                             QDialogButtonBox.Cancel)

        self.button_boxes.accepted.connect(self.accepted)
        self.button_boxes.rejected.connect(self.rejected)

        self.layout = QFormLayout(self)
        self.layout.addRow("Channel:", self.channel)
        self.layout.addRow("Subchannel (1 for default):", self.sub_channel)
        self.layout.addRow("Stop recording if in progress:",
                           self.stop_recording)
        self.layout.addRow(self.button_boxes)

        self.setWindowTitle("Change TiVo channel")
        self.resize(320, 400)

    @Slot()
    def accepted(self):
        self.change_channel.emit(self.channel.value(),
                                 self.sub_channel.value(),
                                 self.stop_recording.isChecked())
        self.close()

    @Slot()
    def rejected(self):
        self.close()