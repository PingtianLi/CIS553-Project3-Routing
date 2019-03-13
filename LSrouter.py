####################################################
# LSrouter.py
# Names: Tong Pow, James Xue
# Penn IDs: 84233063, 51632014
#####################################################

import sys
from collections import defaultdict
from router import Router
from packet import Packet
from json import dumps, loads


class LSrouter(Router):
    """Link state routing protocol implementation."""

    def __init__(self, addr, heartbeatTime):
        """TODO: add your own class fields and initialization code here"""
        Router.__init__(self, addr)  # initialize superclass - don't remove
        self.addr = addr
        self.heartbeatTime = heartbeatTime
        self.lastTime = 0
        # self.neighbors = {} # directly connected neighbors: cost of link
        self.tentative = {}
        self.confirmed = {
            addr: {
                'cost': 0,
                'nextHop': None
            }
        }


    def handlePacket(self, port, packet):
        """TODO: process incoming packet"""
        content = packet.getContent()
        nextNeighbors = content['neighbors']

        for neighbor in nextNeighbors:
            newCost = self.tentative[packet.srcAddr]['cost'] + nextNeighbors[neighbor]['cost']
            if neighbor not in self.confirmed and not in self.tentative:
                self.tentative[neighbor] = {
                    'cost': newCost,
                    'nextHop': packet.srcAddr
                }
            elif neighbor in self.tentative and newCost < self.tentative[neighbor]['cost']:
                self.tentative[neighbor] = {
                    'cost': newCost,
                    'nextHop': packet.srcAddr
                }
        if self.tentative: # check if not empty
            # do something
            pass


    def handleNewLink(self, port, endpoint, cost):
        """TODO: handle new link"""
        pass


    def handleRemoveLink(self, port):
        """TODO: handle removed link"""
        pass


    def sendRoutingPacket():
        """Helper function that sends routing packets to all other nodes in network"""
        # content = {
        #     'neighbors': self.neighbors,
        #     'sequence_num': 0
        # }
        p = Packet(kind, srcAddr=addr, dstAddr, content=dumps(content))


    def handleTime(self, timeMillisecs):
        """TODO: handle current time"""
        if timeMillisecs - self.lastTime > self.heartbeatTime:
            self.sendRoutingPacket()
            self.lastTime = timeMillisecs


    def debugString(self):
        """TODO: generate a string for debugging in network visualizer"""
        return ""
