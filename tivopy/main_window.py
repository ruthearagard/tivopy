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
        self.remote_control_pixmap = QPixmap(":/assets/tivo_remote.jpg")

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
        # This data is also used for associating the button with a key binding.
        #
        # The data for each button is a dictionary with values of the
        # following:
        #
        # cmd (str): The protocol command assigned to this button.
        # key (int): The physical key assigned to this button.
        #
        # min_x (int): The minimum X position that the button corresponds to on
        #              the remote control image.
        #
        # max_x (int): The maximum X position that the button corresponds to on
        #              the remote control image.
        #
        # min_y (int): The minimum Y position that the button corresponds to on
        #              the remote control image.
        #
        # max_y (int): The maximum Y position that the button corresponds to on
        #              the remote control image.
        self.buttons = ({ "cmd"   : "IRCODE TIVO",
                          "key"   : Qt.Key_T,
                          "min_x" : 193,
                          "max_x" : 234,
                          "min_y" : 51,
                          "max_y" : 80 },
                        { "cmd"   : "IRCODE LIVETV",
                          "key"   : Qt.Key_L,
                          "min_x" : 258,
                          "max_x" : 273,
                          "min_y" : 66,
                          "max_y" : 95 },
                        { "cmd"   : "IRCODE TVINPUT",
                          "key"   : Qt.Key_Space,
                          "min_x" : 131,
                          "max_x" : 147,
                          "min_y" : 110,
                          "max_y" : 135 },
                        { "cmd"   : "IRCODE UP",
                          "key"   : Qt.Key_Up,
                          "min_x" : 207,
                          "max_x" : 220,
                          "min_y" : 109,
                          "max_y" : 129 },
                        { "cmd"   : "IRCODE INFO",
                          "key"   : Qt.Key_I,
                          "min_x" : 279,
                          "max_x" : 300,
                          "min_y" : 110,
                          "max_y" : 132 },
                        { "cmd"   : "IRCODE LEFT",
                          "key"   : Qt.Key_Left,
                          "min_x" : 161,
                          "max_x" : 179,
                          "min_y" : 153,
                          "max_y" : 174 },
                        { "cmd"   : "IRCODE SELECT",
                          "key"   : Qt.Key_Return,
                          "min_x" : 200,
                          "max_x" : 236,
                          "min_y" : 143,
                          "max_y" : 188 },
                        { "cmd"   : "IRCODE RIGHT",
                          "key"   : Qt.Key_Right,
                          "min_x" : 248,
                          "max_x" : 262,
                          "min_y" : 155,
                          "max_y" : 175 },
                        { "cmd"   : "IRCODE VOLUMEUP",
                          "key"   : Qt.Key_Plus,
                          "min_x" : 134,
                          "max_x" : 150,
                          "min_y" : 207,
                          "max_y" : 223 },
                        { "cmd"   : "IRCODE DOWN",
                          "key"   : Qt.Key_Down,
                          "min_x" : 202,
                          "max_x" : 225,
                          "min_y" : 200,
                          "max_y" : 223 },
                        { "cmd"   : "IRCODE CHANNELUP",
                          "key"   : Qt.Key_PageUp,
                          "min_x" : 276,
                          "max_x" : 296,
                          "min_y" : 206,
                          "max_y" : 223 },
                        { "cmd"   : "IRCODE VOLUMEDOWN",
                          "key"   : Qt.Key_Minus,
                          "min_x" : 140,
                          "max_x" : 161,
                          "min_y" : 260,
                          "max_y" : 276 },
                        { "cmd"   : "IRCODE GUIDE",
                          "key"   : Qt.Key_G,
                          "min_x" : 192,
                          "max_x" : 231,
                          "min_y" : 241,
                          "max_y" : 269 },
                        { "cmd"   : "IRCODE CHANNELDOWN",
                          "key"   : Qt.Key_PageDown,
                          "min_x" : 262,
                          "max_x" : 288,
                          "min_y" : 259,
                          "max_y" : 277 },
                        { "cmd"   : "IRCODE THUMBSDOWN",
                          "key"   : Qt.Key_End,
                          "min_x" : 143,
                          "max_x" : 160,
                          "min_y" : 296,
                          "max_y" : 328 },
                        { "cmd"   : "IRCODE MUTE",
                          "key"   : Qt.Key_M,
                          "min_x" : 178,
                          "max_x" : 204,
                          "min_y" : 281,
                          "max_y" : 308 },
                        { "cmd"   : "IRCODE RECORD",
                          "key"   : Qt.Key_R,
                          "min_x" : 224,
                          "max_x" : 244,
                          "min_y" : 282,
                          "max_y" : 306 },
                        { "cmd"   : "IRCODE THUMBSUP",
                          "key"   : Qt.Key_Home,
                          "min_x" : 266,
                          "max_x" : 285,
                          "min_y" : 296,
                          "max_y" : 326 },
                        { "cmd"   : "IRCODE PLAY",
                          "key"   : Qt.Key_P,
                          "min_x" : 207,
                          "max_x" : 220,
                          "min_y" : 326,
                          "max_y" : 348 },
                        { "cmd"   : "IRCODE REVERSE",
                          "key"   : Qt.Key_R,
                          "min_x" : 152,
                          "max_x" : 178,
                          "min_y" : 372,
                          "max_y" : 392 },
                        { "cmd"   : "IRCODE PAUSE",
                          "key"   : Qt.Key_S,
                          "min_x" : 196,
                          "max_x" : 228,
                          "min_y" : 358,
                          "max_y" : 407 },
                        { "cmd"   : "IRCODE FORWARD",
                          "key"   : Qt.Key_F,
                          "min_x" : 248,
                          "max_x" : 273,
                          "min_y" : 372,
                          "max_y" : 392 },
                        { "cmd"   : "KEYBOARD VIDEO_ON_DEMAND",
                          "key"   : Qt.Key_V,
                          "min_x" : 189,
                          "max_x" : 238,
                          "min_y" : 463,
                          "max_y" : 484 },
                        { "cmd"   : "IRCODE ACTION_A",
                          "key"   : Qt.Key_A,
                          "min_x" : 143,
                          "max_x" : 166,
                          "min_y" : 485,
                          "max_y" : 507 },
                        { "cmd"   : "IRCODE ACTION_B",
                          "key"   : Qt.Key_B,
                          "min_x" : 185,
                          "max_x" : 205,
                          "min_y" : 498,
                          "max_y" : 522 },
                        { "cmd"   : "IRCODE ACTION_C",
                          "key"   : Qt.Key_C,
                          "min_x" : 222,
                          "max_x" : 245,
                          "min_y" : 498,
                          "max_y" : 522 },
                        { "cmd"   : "IRCODE ACTION_D",
                          "key"   : Qt.Key_D,
                          "min_x" : 261,
                          "max_x" : 283,
                          "min_y" : 485,
                          "max_y" : 509 },
                        { "cmd"   : "IRCODE NUM1",
                          "key"   : Qt.Key_1,
                          "min_x" : 137,
                          "max_x" : 180,
                          "min_y" : 524,
                          "max_y" : 551 },
                        { "cmd"   : "IRCODE NUM2",
                          "key"   : Qt.Key_2,
                          "min_x" : 192,
                          "max_x" : 231,
                          "min_y" : 534,
                          "max_y" : 560 },
                        { "cmd"   : "IRCODE NUM3",
                          "key"   : Qt.Key_3,
                          "min_x" : 247,
                          "max_x" : 294,
                          "min_y" : 526,
                          "max_y" : 550 },
                        { "cmd"   : "IRCODE NUM4", 
                          "key"   : Qt.Key_4,
                          "min_x" : 134,
                          "max_x" : 175,
                          "min_y" : 560,
                          "max_y" : 586 },
                        { "cmd"   : "IRCODE NUM5",
                          "key"   : Qt.Key_5,
                          "min_x" : 192,
                          "max_x" : 236,
                          "min_y" : 568,
                          "max_y" : 596 },
                        { "cmd"   : "IRCODE NUM6",
                          "key"   : Qt.Key_6,
                          "min_x" : 253,
                          "max_x" : 295,
                          "min_y" : 559,
                          "max_y" : 589 },
                        { "cmd"   : "IRCODE NUM7",
                          "key"   : Qt.Key_7,
                          "min_x" : 128,
                          "max_x" : 170,
                          "min_y" : 594,
                          "max_y" : 620 },
                        { "cmd"   : "IRCODE NUM8",
                          "key"   : Qt.Key_8,
                          "min_x" : 192,
                          "max_x" : 232,
                          "min_y" : 603,
                          "max_y" : 630 },
                        { "cmd"   : "IRCODE NUM9",
                          "key"   : Qt.Key_9,
                          "min_x" : 257,
                          "max_x" : 295,
                          "min_y" : 593,
                          "max_y" : 621 },
                        { "cmd"   : "IRCODE CLEAR",
                          "key"   : Qt.Key_Backspace,
                          "min_x" : 127,
                          "max_x" : 167,
                          "min_y" : 628,
                          "max_y" : 656 },
                        { "cmd"   : "IRCODE NUM0",
                          "key"   : Qt.Key_0,
                          "min_x" : 194,
                          "max_x" : 230,
                          "min_y" : 639,
                          "max_y" : 667 },
                        { "cmd"   : "IRCODE ENTER",
                          "key"   : Qt.Key_Enter,
                          "min_x" : 257,
                          "max_x" : 301,
                          "min_y" : 628,
                          "max_y" : 656 })

        # The current button that the cursor is hovering over.
        self.current_button = { }

    def mouseMoveEvent(self, event):
        """Called when the cursor moves over the remote control."""
        # Every time a user makes a move, we have to check and see if the
        # cursor is hovering over a position we care about.
        for button in self.buttons:
            # Grab the X and Y positions of the cursor. We do this here so as
            # to not repeatedly call it over and over again in the following
            # code.
            x = event.x()
            y = event.y()

            # Is the cursor within the ranges of a button's bounding box?
            if (x >= button["min_x"] and x <= button["max_x"]) and \
               (y >= button["min_y"] and y <= button["max_y"]):
                # Yes, save the current button the user is hovering over. This
                # will prevent us from having to iterate again if the user
                # clicks on the zone.
                self.current_button = button

                # Change the cursor to pointing hand to signify that this area
                # is indeed clickable.
                self.setCursor(Qt.PointingHandCursor)
                break

            # The cursor is not hovering over a button, clear the current
            # button and return the cursor to normal.
            self.current_button = { }
            self.unsetCursor()

    def mousePressEvent(self, event):
        """Called when the mouse is left clicked on the remote control."""
        # It is very possible that the user will just click regardless of
        # whether or not they're hovering over a zone, so this check is
        # necessary.
        if self.current_button:
            # The user is pressing a button, dispatch the command string for
            # it.
            self.command_requested.emit(self.current_button["cmd"])

    def keyPressEvent(self, event):
        """Called when the user presses a key on the keyboard."""

        for button in self.buttons:
            if button["key"] == event.key():
              self.command_requested.emit(button["cmd"])
              break

    @Slot(QPoint)
    def on_context_menu(self, point):
        """Called when the mouse is right clicked on the remote control."""
        menu = QMenu(self)
        menu.addAction(self.current_channel)
        menu.addSeparator()
        menu.addAction(self.select_tivo)
        menu.addAction(self.input_text)
        menu.addAction(self.change_channel)
        menu.exec_(self.mapToGlobal(point))

    def update_channel(self, channel):
        """
        Updates the information specifying to the user what channel their TiVo
        is currently tuned into.
        """
        self.current_channel.setText(f"Current channel: {channel}")