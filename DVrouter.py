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
        self.table = {}  # {dst: {cost:, nextHop port}}
        self.ports = set()

    def handlePacket(self, port, packet):
        """TODO: process incoming packet"""
        # check whether the packet is a traceroute packet or a routing packet and
        # handle it appropriately
        if packet.isTraceroute():
            pass
        elif packet.isRouting():
            #print("THIS IS THE PACKET", self.addr, packet.dstAddr)
            content = loads(packet.content)
            for k, v in content.iteritems():
                if k != self.addr:
                    if k not in self.table:
                        # Modify cost later
                        self.table[k] = {"cost": v["cost"], "nextHop": packet.srcAddr}
                    else:
                        self.table[k]["cost"] = min(self.table[k]["cost"], v["cost"])
                        if self.table[k]["cost"] == v["cost"]:
                            self.table[k]["nextHop"] = v["nextHop"]
            print(self.addr, self.table)
            #self.send(port, packet)
        pass

    def handleNewLink(self, port, endpoint, cost):
        """TODO: handle new link"""
        # should store the argument values in a data structure to use for routing.
        # If you want to send packets along this link, call self.send(port, packet)
        if endpoint not in self.table:
            self.table[endpoint] = {"cost": cost, "nextHop": port}
        else:
            if cost < self.table[endpoint]["cost"]:
                self.table[endpoint]["cost"] = cost
                self.table[endpoint]["nextHop"] = port
        pass

    def handleRemoveLink(self, port):
        """TODO: handle removed link"""

        pass

    def handleTime(self, timeMillisecs):
        """TODO: handle current time"""
        if timeMillisecs - self.last_time > self.heartbeatTime:
            for k in self.table.keys():
                for p in self.links.keys():
                    packet = Packet(Packet.ROUTING, self.addr, k)
                    packet.content = dumps(self.table)
                    self.send(p, packet)
            self.last_time = timeMillisecs
        pass

    def debugString(self):
        """TODO: generate a string for debugging in network visualizer"""
        return "Hello"
