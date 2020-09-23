# TiVoPy -- TiVo Virtual Remote Control

This program is open source but copyrighted under the ISC license; refer to the
"license.txt" file for more information.

Introduction
------------

TiVoPy is a [PySide2](https://www.qt.io/qt-for-python) based virtual
remote control for TiVo, utilizing the _Network Remote Control_ feature.

To enable it, nagivate to TiVo Central -> Messages & Settings -> Settings ->
Remote, CableCARD & Devices -> Network Remote Control. This program WILL NOT
WORK if the protocol isn't enabled.

TiVoPy is capable of autodetecting TiVos on your local network, or allowing you
to specify the IP address of the TiVo you want to connect to.

Operation
---------

Each time the program is opened, every TiVo on your local network will
automatically be detected. All you have to do is double click on the TiVo that
you care about to connect to it. If you do not see your TiVo listed, you may
enter its IP address manually.

Following this, a TiVo remote control will appear on your screen. The operation
of this remote is analagous to how you would use a TiVo remote control in
reality: click a button on the virtual remote control and it will perform
exactly the same action as if you had pressed the same button on your physical
remote.

Right clicking on the remote will display a context menu, allowing you to
change the TiVo the program is connected to, input arbitrary text, or perform
other miscellanious actions.

I tried to make the program as self-explanatory as I possibly could, as such
there's no set of instructions beyond this readme.

I'm [open to feature suggestions](https://github.com/ruthearagard/tivopy/issues/new/choose) and
pull requests.

Downloads
---------

Credits
-------

Michael Rodriguez <ruthearagard -at- gmail -dot- com>
