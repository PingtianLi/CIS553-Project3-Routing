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
        self.graph = {}  # directly connected neighbors: cost of link
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
        packet_graph = content['graph']

        # Populate self.tentative with this packet's neighbors
        for neighbor in nextNeighbors:
            # Update self.graph
            if packet.srcAddr not in self.graph:
                self.graph[packet.srcAddr] = {neighbor: packet_graph[packet.srcAddr][neighbor]}
            else:
                self.graph[packet.srcAddr][neighbor] = min(self.graph[packet.srcAddr][neighbor], packet_graph[packet.srcAddr][neighbor])

        # Place current node into self.tentative
        self.tentative[packet.srcAddr] = {
            'cost': 0,
            'nextHop': None
        }

        # Djikstra's, updating shortest path
        while self.tentative:
            # Pop lowest cost member
            lowestCostEntry = min(self.tentative, key=lambda k: self.tentative[k]['cost'])

            # Iterate through neighbors of lowestCostEntry, update
            curr_neighbors = self.graph[lowestCostEntry]
            for n in curr_neighbors:
                newCost = self.tentative[lowestCostEntry]['cost'] + curr_neighbors[lowestCostEntry][n]
                tentativeCost = self.tentative[n]['cost']

                # If found lower cost path, update tentative and graph
                if (n not in self.confirmed and n not in self.tentative) or (n in self.tentative and newCost < tentativeCost):
                    self.tentative[n] = {
                        'cost': newCost,
                        'nextHop': lowestCostEntry
                    }

            # Update self.confirmed and pop
            self.confirmed[lowestCostEntry] = self.tentative[lowestCostEntry]
            del self.tentative[lowestCostEntry]

    def handleNewLink(self, port, endpoint, cost):
        """TODO: handle new link"""

        pass

    def handleRemoveLink(self, port):
        """TODO: handle removed link"""
        pass

    def sendRoutingPacket():
        """Helper function that sends routing packets to all other nodes in network"""
        # content = {
        #     'graph': {A: {B: cost, ...}, ...}
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
