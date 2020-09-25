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

import assets
from PySide2.QtCore import Signal, Slot, QPoint, Qt
from PySide2.QtGui import QMouseEvent, QPixmap
from PySide2.QtWidgets import (QAction,
                               QLabel,
                               QLayout,
                               QMainWindow,
                               QMenu,
                               QPushButton)

class MainWindow(QLabel):
    """Defines the view for the remote control."""
    command_requested = Signal(str)

    def __init__(self):
        super(MainWindow, self).__init__()

        # Construct a QPixmap from the TiVo remote control image.
        self.remote_control_pixmap = QPixmap("tivo_remote.jpg")

        # Scale the window to the width and height of the TiVo remote control
        # image and disable resizing. We disable resizing because:
        #
        # 1) there's really no point to resizing it
        # 2) none of the images I have are going to look good scaled up
        # 3) it would only serve to complicate the clickable zone logic for no
        #    good reason (see below).
        self.setFixedSize(self.remote_control_pixmap.width(),
                          self.remote_control_pixmap.height())

        # Render the pixmap to the window.
        self.setPixmap(self.remote_control_pixmap)

        # Allow a context menu to be implemented.
        self.setContextMenuPolicy(Qt.CustomContextMenu)

        # Notify us when the user has right clicked on the window.
        self.customContextMenuRequested.connect(self.on_context_menu)

        # Define informational QActions to be displayed to the user on the
        # context menu.
        self.current_channel = QAction(self)
        self.connected_to = QAction(self)

        # Because they're informational, making them clickable would serve no
        # purpose.
        self.connected_to.setEnabled(False)
        self.current_channel.setEnabled(False)

        self.select_tivo = QAction("Connect to a different TiVo...", self)
        self.change_channel = QAction("Change channel...", self)
        self.input_text = QAction("Input text...", self)

        # We care about ALL movements of the user, regardless of whether or not
        # they're pressing buttons.
        self.setMouseTracking(True)

        # Button widgets are not used to handle input from the user, instead an
        # image of a TiVo remote control is displayed and the user merely has
        # to click on the button they wish to press as they would press it on a
        # real remote control. Therefore, the simplest solution is to intercept
        # cursor movements and check to see whether the coordinates fall within
        # the boundaries of a button.
        #
        # The boundary data for each button is a dictionary with values of the
        # following:
        #
        # cmd (str):   The command that will be sent when the zone is triggered
        # min_x (int): The minimum X position that the zone is in.
        # max_x (int): The maximum X position that the zone is in.
        # min_y (int): The minimum Y position that the zone is in.
        # max_y (int): The maximum Y position that the zone is in.
        self.clickable_zones = [{ "cmd"    : "IRCODE TIVO",
                                  "min_x"  : 193,
                                  "max_x"  : 234,
                                  "min_y"  : 51,
                                  "max_y"  : 80 },
                                { "cmd"    : "IRCODE LIVETV",
                                  "min_x"  : 258,
                                  "max_x"  : 273,
                                  "min_y"  : 66,
                                  "max_y"  : 95 },
                                { "cmd"    : "IRCODE TVINPUT",
                                  "min_x"  : 131,
                                  "max_x"  : 147,
                                  "min_y"  : 110,
                                  "max_y"  : 135 },
                                { "cmd"    : "IRCODE UP",
                                  "min_x"  : 207,
                                  "max_x"  : 220,
                                  "min_y"  : 109,
                                  "max_y"  : 129 },
                                { "cmd"    : "IRCODE INFO",
                                  "min_x"  : 279,
                                  "max_x"  : 300,
                                  "min_y"  : 110,
                                  "max_y"  : 132 },
                                { "cmd"    : "IRCODE LEFT",
                                  "min_x"  : 161,
                                  "max_x"  : 179,
                                  "min_y"  : 153,
                                  "max_y"  : 174 },
                                { "cmd"    : "IRCODE SELECT",
                                  "min_x"  : 200,
                                  "max_x"  : 236,
                                  "min_y"  : 143,
                                  "max_y"  : 188 },
                                { "cmd"    : "IRCODE RIGHT",
                                  "min_x"  : 248,
                                  "max_x"  : 262,
                                  "min_y"  : 155,
                                  "max_y"  : 175 },
                                { "cmd"    : "IRCODE VOLUMEUP",
                                  "min_x"  : 134,
                                  "max_x"  : 150,
                                  "min_y"  : 207,
                                  "max_y"  : 223 },
                                { "cmd"    : "IRCODE DOWN",
                                  "min_x"  : 202,
                                  "max_x"  : 225,
                                  "min_y"  : 200,
                                  "max_y"  : 223 },
                                { "cmd"    : "IRCODE CHANNELUP",
                                  "min_x"  : 276,
                                  "max_x"  : 296,
                                  "min_y"  : 206,
                                  "max_y"  : 223 },
                                { "cmd"    : "IRCODE VOLUMEDOWN",
                                  "min_x"  : 140,
                                  "max_x"  : 161,
                                  "min_y"  : 260,
                                  "max_y"  : 276 },
                                { "cmd"    : "IRCODE GUIDE",
                                  "min_x"  : 192,
                                  "max_x"  : 231,
                                  "min_y"  : 241,
                                  "max_y"  : 269 },
                                { "cmd"    : "IRCODE CHANNELDOWN",
                                  "min_x"  : 262,
                                  "max_x"  : 288,
                                  "min_y"  : 259,
                                  "max_y"  : 277 },
                                { "cmd"    : "IRCODE THUMBSDOWN",
                                  "min_x"  : 143,
                                  "max_x"  : 160,
                                  "min_y"  : 296,
                                  "max_y"  : 328 },
                                { "cmd"    : "IRCODE MUTE",
                                  "min_x"  : 178,
                                  "max_x"  : 204,
                                  "min_y"  : 281,
                                  "max_y"  : 308 },
                                { "cmd"    : "IRCODE RECORD",
                                  "min_x"  : 224,
                                  "max_x"  : 244,
                                  "min_y"  : 282,
                                  "max_y"  : 306 },
                                { "cmd"    : "IRCODE THUMBSUP",
                                  "min_x"  : 266,
                                  "max_x"  : 285,
                                  "min_y"  : 296,
                                  "max_y"  : 326 },
                                { "cmd"    : "IRCODE PLAY",
                                  "min_x"  : 207,
                                  "max_x"  : 220,
                                  "min_y"  : 326,
                                  "max_y"  : 348 },
                                { "cmd"    : "IRCODE REVERSE",
                                  "min_x"  : 152,
                                  "max_x"  : 178,
                                  "min_y"  : 372,
                                  "max_y"  : 392 },
                                { "cmd"    : "IRCODE PAUSE",
                                  "min_x"  : 196,
                                  "max_x"  : 228,
                                  "min_y"  : 358,
                                  "max_y"  : 407 },
                                { "cmd"    : "IRCODE FORWARD",
                                  "min_x"  : 248,
                                  "max_x"  : 273,
                                  "min_y"  : 372,
                                  "max_y"  : 392 },
                                { "cmd"    : "KEYBOARD VIDEO_ON_DEMAND",
                                  "min_x"  : 189,
                                  "max_x"  : 238,
                                  "min_y"  : 463,
                                  "max_y"  : 484 },
                                { "cmd"    : "IRCODE ACTION_A",
                                  "min_x"  : 143,
                                  "max_x"  : 166,
                                  "min_y"  : 485,
                                  "max_y"  : 507 },
                                { "cmd"    : "IRCODE ACTION_B",
                                  "min_x"  : 185,
                                  "max_x"  : 205,
                                  "min_y"  : 498,
                                  "max_y"  : 522 },
                                { "cmd"    : "IRCODE ACTION_C",
                                  "min_x"  : 222,
                                  "max_x"  : 245,
                                  "min_y"  : 498,
                                  "max_y"  : 522 },
                                { "cmd"    : "IRCODE ACTION_D",
                                  "min_x"  : 261,
                                  "max_x"  : 283,
                                  "min_y"  : 485,
                                  "max_y"  : 509 },
                                { "cmd"    : "IRCODE NUM1",
                                  "min_x"  : 137,
                                  "max_x"  : 180,
                                  "min_y"  : 524,
                                  "max_y"  : 551 },
                                { "cmd"    : "IRCODE NUM2",
                                  "min_x"  : 192,
                                  "max_x"  : 231,
                                  "min_y"  : 534,
                                  "max_y"  : 560 },
                                { "cmd"    : "IRCODE NUM3",
                                  "min_x"  : 247,
                                  "max_x"  : 294,
                                  "min_y"  : 526,
                                  "max_y"  : 550 },
                                { "cmd"    : "IRCODE NUM4", 
                                  "min_x"  : 134,
                                  "max_x"  : 175,
                                  "min_y"  : 560,
                                  "max_y"  : 586 },
                                { "cmd"    : "IRCODE NUM5",
                                  "min_x"  : 192,
                                  "max_x"  : 236,
                                  "min_y"  : 568,
                                  "max_y"  : 596 },
                                { "cmd"    : "IRCODE NUM6",
                                  "min_x"  : 253,
                                  "max_x"  : 295,
                                  "min_y"  : 559,
                                  "max_y"  : 589 },
                                { "cmd"    : "IRCODE NUM7",
                                  "min_x"  : 128,
                                  "max_x"  : 170,
                                  "min_y"  : 594,
                                  "max_y"  : 620 },
                                { "cmd"    : "IRCODE NUM8",
                                  "min_x"  : 192,
                                  "max_x"  : 232,
                                  "min_y"  : 603,
                                  "max_y"  : 630 },
                                { "cmd"    : "IRCODE NUM9",
                                  "min_x"  : 257,
                                  "max_x"  : 295,
                                  "min_y"  : 593,
                                  "max_y"  : 621 },
                                { "cmd"    : "IRCODE CLEAR",
                                  "min_x"  : 127,
                                  "max_x"  : 167,
                                  "min_y"  : 628,
                                  "max_y"  : 656 },
                                { "cmd"    : "IRCODE NUM0",
                                  "min_x"  : 194,
                                  "max_x"  : 230,
                                  "min_y"  : 639,
                                  "max_y"  : 667 },
                                { "cmd"    : "IRCODE ENTER",
                                  "min_x"  : 257,
                                  "max_x"  : 301,
                                  "min_y"  : 628,
                                  "max_y"  : 656 }]

        # The current zone that the cursor is hovering over.
        self.current_zone = { }

    def mouseMoveEvent(self, event):
        """Called when the cursor moves over the remote control."""
        # Every time a user makes a move, we have to check and see if the
        # cursor is hovering over a position we care about.
        for zone in self.clickable_zones:
            # Grab the X and Y positions of the cursor. We do this here so as
            # to not repeatedly call it over and over again in the following
            # code.
            x = event.x()
            y = event.y()

            # Is the cursor within the ranges of a zone's bounding box?
            if (x >= zone["min_x"] and x <= zone["max_x"]) and \
               (y >= zone["min_y"] and y <= zone["max_y"]):
                # Yes, save the current zone the user is hovering over. This
                # will prevent us from having to iterate again if the user
                # clicks on the zone.
                self.current_zone = zone

                # Change the cursor to pointing hand to signify that this area
                # is indeed clickable.
                self.setCursor(Qt.PointingHandCursor)
                break

            # The cursor is not hovering over a zone, clear the current zone
            # and return the cursor to normal.
            self.current_zone = { }
            self.unsetCursor()

    def mousePressEvent(self, event):
        """Called when the mouse is left clicked on the remote control."""
        # It is very possible that the user will just click regardless of
        # whether or not they're hovering over a zone, so this check is
        # necessary.
        if self.current_zone:
            # The user is pressing a button, dispatch the command string for
            # it.
            self.command_requested.emit(self.current_zone["cmd"])

    @Slot(QPoint)
    def on_context_menu(self, point):
        """Called when the mouse is right clicked on the remote control."""
        menu = QMenu(self)
        menu.addAction(self.connected_to)
        menu.addAction(self.current_channel)
        menu.addSeparator()
        menu.addAction(self.select_tivo)
        menu.addAction(self.input_text)
        menu.addAction(self.change_channel)
        menu.exec_(self.mapToGlobal(point))

    def update_connected_to(self, name, ip):
        """
        Updates the information specifying to the user what TiVo they're
        connected to and its IP.
        """
        self.connected_to.setText(f"Connected to {name} ({ip})")

    def update_channel(self, name, how):
        """
        Updates the information specifying to the user what channel their TiVo
        is currently tuned into.
        """
        self.current_channel.setText(f"Current channel: {name} ({how})")