####################################################
# DVrouter.py
# Names: Tong Pow, James Xue
# Penn IDs: 84233063, 51632014
#####################################################

import sys
from collections import defaultdict
from router import Router
from packet import Packet
from json import dumps, loads


class DVrouter(Router):
    """Distance vector routing protocol implementation."""

    def __init__(self, addr, heartbeatTime):
        """TODO: add your own class fields and initialization code here"""
        Router.__init__(self, addr)  # initialize superclass - don't remove
        self.last_time = 0
        self.heartbeatTime = heartbeatTime
        self.addr = addr
        self.table = {}  # {dst/port: {cost:, nextHop}}

    def handlePacket(self, port, packet):
        """TODO: process incoming packet"""
        # check whether the packet is a traceroute packet or a routing packet and
        # handle it appropriately
        if packet.isTraceroute():
            pass
        elif packet.isRouting():

            self.send(port, packet)
        pass

    def handleNewLink(self, port, endpoint, cost):
        """TODO: handle new link"""
        # should store the argument values in a data structure to use for routing.
        # If you want to send packets along this link, call self.send(port, packet)
        # if port in self.table:
        #     old_cost = self.table[port]["cost"]
        #     self.table[port]["cost"] = min(old_cost, cost)
        for k, v in self.table.iteritems():
            if port == k:
                if cost + 1 < self.table[k]["cost"]:
                    break
                elif

        pass

    def handleRemoveLink(self, port):
        """TODO: handle removed link"""

        pass

    def handleTime(self, timeMillisecs):
        """TODO: handle current time"""
        if timeMillisecs - self.last_time > self.heartbeatTime:
            for neighbors in self.table:
                self.send()
            self.last_time = timeMillisecs
        pass

    def debugString(self):
        """TODO: generate a string for debugging in network visualizer"""
        return self.links
