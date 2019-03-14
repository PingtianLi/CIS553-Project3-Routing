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
        self.neighbors = {}  # {endpoint: {port, sequence}
        self.graph = {}  # directly connected neighbors: cost of link
        self.packets = {}  # {addr: packet}
        self.tentative = {}
        self.confirmed = {
            addr: {
                'cost': 0,
                'nextHop': None
            }
        }
        self.mysqn = 0

    def handlePacket(self, port, packet):
        """TODO: process incoming packet"""

        if packet.isTraceroute():
            # print(self.addr, self.confirmed.keys())  # , packet.dstAddr)

            if packet.dstAddr in self.confirmed:
                self.send(self.neighbors[self.confirmed[packet.dstAddr]["nextHop"]]['port'], packet)

        # Distribute information on map
        elif packet.isRouting():
            content = loads(packet.content)
            # Add packet into self.packets if it's newer
            if packet.srcAddr not in self.packets or content['sqn'] > loads(self.packets[packet.srcAddr].content)['sqn']:
                self.packets[packet.srcAddr] = packet
                for n in self.neighbors:
                    if port != self.neighbors[n]['port']:
                        self.send(self.neighbors[n]['port'], packet)

            # Create + update map
            for packet_addr in self.packets:
                curr_content = loads(self.packets[packet_addr].content)
                curr_cost = curr_content['neighbors'][self.addr]['cost']

                if packet_addr not in self.graph:
                    self.graph[packet_addr] = {self.addr: curr_cost}
                    # print(packet_addr, self.addr, packet_addr, curr_cost)
                else:
                    self.graph[packet_addr][self.addr] = curr_cost
                if self.addr not in self.graph:
                    self.graph[self.addr] = {packet_addr: curr_cost}
                else:
                    self.graph[self.addr][packet_addr] = curr_cost

            self.tentative = {}
            self.confirmed = {}

            # Place current node into self.tentative
            self.tentative[packet.srcAddr] = {
                'cost': 0,
                'nextHop': None
            }

            visited = set()

            # Djikstra's, updating shortest path
            while self.tentative:
                # Pop lowest cost member
                lowestCostEntry = min(self.tentative, key=lambda k: self.tentative[k]['cost'])
                print(self.addr, lowestCostEntry, packet.srcAddr, self.confirmed.keys())
                # Iterate through neighbors of lowestCostEntry, update
                for n in self.graph[lowestCostEntry]:
                    newCost = self.tentative[lowestCostEntry]['cost'] + self.graph[lowestCostEntry][n]
                    tentativeCost = float('inf')
                    if n in self.tentative:
                        tentativeCost = self.tentative[n]['cost']

                    # If found lower cost path, update tentative and graph
                    if (n not in self.confirmed and n not in self.tentative) or (n in self.tentative and newCost < tentativeCost):

                        self.tentative[n] = {
                            'cost': newCost,
                            'nextHop': packet.srcAddr
                        }

                # Update self.confirmed and pop
                if lowestCostEntry not in visited:
                    self.confirmed[lowestCostEntry] = self.tentative[lowestCostEntry]
                visited.add(lowestCostEntry)
                # print(self.confirmed)
                del self.tentative[lowestCostEntry]

    def handleNewLink(self, port, endpoint, cost):
        """TODO: handle new link"""
        if endpoint not in self.neighbors:
            self.neighbors[endpoint] = {"port": port, "sqn": 0, "cost": cost}

        if self.addr not in self.graph:
            self.graph[self.addr] = {endpoint: cost}
        else:
            self.graph[self.addr][endpoint] = cost
        if endpoint not in self.graph:
            self.graph[endpoint] = {self.addr: cost}
        else:
            self.graph[endpoint][self.addr] = cost

        content = {
            'sqn': self.mysqn,
            'neighbors': self.neighbors
        }
        for k, v in self.neighbors.iteritems():
            p = Packet(Packet.ROUTING, self.addr, k, dumps(content))
            self.send(v['port'], p)

    def handleRemoveLink(self, port):
        """TODO: handle removed link"""
        pass

    def sendRoutingPacket(self):
        """Helper function that sends routing packets to all other nodes in network"""
        content = {
            #'graph': {A: {B: cost, ...}, ...}
            'sqn': self.mysqn,
            'neighbors': self.neighbors
        }
        for n in self.neighbors:
            p = Packet(2, self.addr, n, content=dumps(content))
            self.send(self.neighbors[n]['port'], p)

    def handleTime(self, timeMillisecs):
        """TODO: handle current time"""
        if timeMillisecs - self.lastTime > self.heartbeatTime:
            self.sendRoutingPacket()
            self.lastTime = timeMillisecs
            self.mysqn += 1

    def debugString(self):
        """TODO: generate a string for debugging in network visualizer"""
        return dumps(self.neighbors)
