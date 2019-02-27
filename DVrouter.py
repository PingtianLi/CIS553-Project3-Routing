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
        self.addr = addr
        self.heartbeatTime = heartbeatTime
        self.last_time = 0
        # Initialize routing table
        self.table = {}  # table[dstAddr] = {cost: cost, nextHop: address}
        # self.ports = set()


    def handlePacket(self, port, packet):
        """TODO: process incoming packet"""
        # check whether the packet is a traceroute packet or a routing packet and
        # handle it appropriately
        # Ignore traceroute packets and handle routing packets
        if packet.isRouting():
            print packet.srcAddr, packet.content
            # content = loads(packet.content)
            # update table
            # if packet came from a router not in table, add it to table with nextHop=srcAddr and cost=baseCost
            if packet.srcAddr not in self.table:
                self.table[packet.srcAddr] = {
                    'cost': 1,#getcost,
                    'nextHop': packet.srcAddr
                }
            # else check if cost to srcAddr can be lowered. if so then update table

            
            # update contents of table with contents of packet
                # for each row in packet.content, check if packet.content cost + cost from srcAddr to me is lower than existing
                    # if so, update with new cost and nextHop = dstAddr


            #print("THIS IS THE PACKET", self.addr, packet.dstAddr)
            # content = loads(packet.content)
            # for k, v in content.iteritems():
            #     if k != self.addr:
            #         if k not in self.table:
            #             # Modify cost later
            #             self.table[k] = {"cost": v["cost"], "nextHop": packet.srcAddr}
            #         else:
            #             self.table[k]["cost"] = min(self.table[k]["cost"], v["cost"])
            #             if self.table[k]["cost"] == v["cost"]:
            #                 self.table[k]["nextHop"] = v["nextHop"]
            # print(self.addr, self.table)


    def handleNewLink(self, port, endpoint, cost):
        """TODO: handle new link"""
        # should store the argument values in a data structure to use for routing.
        # If you want to send packets along this link, call self.send(port, packet)

        # if endpoint not in self.table:
        #     self.table[endpoint] = {"cost": cost, "nextHop": port}
        # else:
        #     if cost < self.table[endpoint]["cost"]:
        #         self.table[endpoint]["cost"] = cost
        #         self.table[endpoint]["nextHop"] = port
        pass


    def handleRemoveLink(self, port):
        """TODO: handle removed link"""
        pass


    def sendRoutingPackets(self):
        """Send routing packets to all neighbors"""
        for port, link in self.links.iteritems():
            # Initialize table
            if self.addr == link.e1 and link.e2 not in self.table:
                # This router is e1 so it needs to add e2 to its table
                self.table[link.e2] = {
                    'cost': link.l12,
                    'nextHop': link.e2
                }
            elif self.addr == link.e2 and link.e1 not in self.table:
                # This router is e2 so it needs to add e1 to its table
                self.table[link.e1] = {
                    'cost': link.l21,
                    'nextHop': link.e1
                }

            # Create packet
            packet = Packet(kind=Packet.ROUTING,
                            srcAddr=self.addr,
                            dstAddr=None,
                            content=dumps(self.table))

            # Send packet
            self.send(port, packet)
            

    def handleTime(self, timeMillisecs):
        """TODO: handle current time"""
        if timeMillisecs - self.last_time > self.heartbeatTime:
            self.sendRoutingPackets()
            self.last_time = timeMillisecs


    def debugString(self):
        """TODO: generate a string for debugging in network visualizer"""
        return
