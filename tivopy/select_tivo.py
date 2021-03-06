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

from PySide2.QtCore import Signal

from PySide2.QtWidgets import (QDialog,
                              QInputDialog,
                              QLabel,
                              QLineEdit,
                              QTreeWidget,
                              QTreeWidgetItem,
                              QVBoxLayout)

class SelectTiVoWidget(QDialog):
    """Displays the list of TiVos that were discovered on the network."""

    # Signals
    connect_to_tivo = Signal(str, str)

    def __init__(self):
        super(SelectTiVoWidget, self).__init__()

        self.tivos_found = []

        self.label = QLabel(self)

        self.label.setText('Below is a listing of all TiVos discovered on your'
                           ' network, which will refresh every 5 seconds. If y'
                           'ou do not see your TiVo, '
                           '<a href="#specify_ip">click here to specify an IP'
                           ' address.</a>')

        self.label.linkActivated.connect(self.specify_ip_address)

        self.tivo_listings = QTreeWidget(self)
        self.tivo_listings.itemDoubleClicked.connect(self.tivo_selected)
        self.tivo_listings.setHeaderLabels(["Name", "IP Address"])

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.tivo_listings)

        self.setWindowTitle("Select TiVo")
        self.resize(512, 384)

        self.setModal(True)

    def add_tivo(self, name, ip_address):
        item = QTreeWidgetItem()
        item.setText(0, name)
        item.setText(1, ip_address)

        self.tivo_listings.addTopLevelItem(item)
        self.tivos_found.append(item)

    def tivo_selected(self, item, column):
        self.connect_to_tivo.emit(item.text(0), item.text(1))

    def specify_ip_address(self, link):
        text, ok = QInputDialog().getText(self,
                                          "Specify TiVO IP address",
                                          "IP address:",
                                          QLineEdit.Normal)

        if ok:
            self.connect_to_tivo.emit("unknown", text)