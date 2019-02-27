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
        self.table = {}  # {addr: {cost:, nextHop: addr, port: }}
        self.infinity = 16

    def handlePacket(self, port, packet):
        """TODO: process incoming packet"""
        # check whether the packet is a traceroute packet or a routing packet and
        # handle it appropriately
        if packet.isTraceroute():
            if packet.dstAddr in self.table:
                self.send(self.table[packet.dstAddr]["port"], packet)
        elif packet.isRouting():
            #     #print("THIS IS THE PACKET", self.addr, packet.dstAddr)
            content = loads(packet.content)
            for k, v in content.iteritems():
                if k != self.addr:
                    if k not in self.table:
                        # Modify cost later
                        self.table[k] = {
                            "cost": v["cost"] + self.table[packet.srcAddr]["cost"],
                            "nextHop": packet.srcAddr,
                            "port": self.table[packet.srcAddr]["port"]
                        }
                    else:
                        if self.table[packet.srcAddr]["cost"] + v["cost"] < self.table[k]["cost"]:
                            self.table[k]["cost"] = self.table[packet.srcAddr]["cost"] + v["cost"]
                            self.table[k]["nextHop"] = packet.srcAddr
                            self.table[k]["port"] = self.table[packet.srcAddr]["port"]

            print("SOURCE ADDRESS: ", packet.srcAddr)
            print("DESTINATION ADDRESS: ", packet.dstAddr)
            print(content)
        #self.send(port, packet)

    def handleNewLink(self, port, endpoint, cost):
        """TODO: handle new link"""
        # should store the argument values in a data structure to use for routing.
        # If you want to send packets along this link, call self.send(port, packet)
        if endpoint not in self.table:
            self.table[endpoint] = {"cost": cost, "nextHop": endpoint, "port": port}
            #print("SOURCE ADDRESS: ", self.addr)
            # print(dumps(self.table))
        # else:
        #     if cost < self.table[endpoint]["cost"]:
        #         self.table[endpoint]["cost"] = cost
        #         self.table[endpoint]["nextHop"] = port

    def handleRemoveLink(self, port):
        """TODO: handle removed link"""

        pass

    def handleTime(self, timeMillisecs):
        """TODO: handle current time"""
        if timeMillisecs - self.last_time > self.heartbeatTime:
            for k, v in self.table.iteritems():
                packet = Packet(Packet.ROUTING, self.addr, k)
                packet.content = dumps(self.table)
                self.send(v["port"], packet)
            self.last_time = timeMillisecs

    def debugString(self):
        """TODO: generate a string for debugging in network visualizer"""
        return "Hello"
