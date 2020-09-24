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

from socket import inet_ntoa
from zeroconf import ServiceBrowser, Zeroconf

class TiVoDiscovery:
    """Discovers TiVos on the local network using Zeroconf."""
    def __init__(self):
        self.addresses = []

        self.zeroconf = Zeroconf()
        self.browser = ServiceBrowser(self.zeroconf,
                                      "_tivo-mindrpc._tcp.local.",
                                      self)
    
    def remove_service(self, zeroconf, type, name):
        """
        Called by zeroconf.ServiceBrowser when a TiVo has been removed from
        the network. We should probably care about this, but we don't
        currently.
        """
        pass

    def add_service(self, zeroconf, type, name):
        """
        Called by zeroconf.ServiceBrowser when a TiVo has been detected on the
        network.
        """
        info = zeroconf.get_service_info(type, name)

        for address in info.addresses:
            # The user should not care about the underlying service name.
            result = (name.strip('._tivo-mindrpc._tcp.local.'),
                      inet_ntoa(address))

            if result not in self.addresses:
                self.addresses.append(result)