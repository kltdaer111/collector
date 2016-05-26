# -*- coding: utf-8 -*-
import socket, select
import random
import pickle
import socket
import time
TYPE_AMOUNT = 10
PORT_TUPLE = (9455,9456,9457,9458)
data_detail = {
    'gate_id' : 0,
    'node_id' : 0,
    'state' : 0,
    'date' : 0,
    }

class Node:
    last_time = 0
    def __init__(self, sock, gate_id, node_id, interval):
        self.sock = sock
        self.gate_id = gate_id
        self.node_id = node_id
        self.interval = interval
        
    def update(self, time):
        if(time >= last_time + interval):
            self.send_info(time)

    def send_info(self, time):
        data_detail.gate_id = self.gate_id
        data_detail.node_id = self.node_id
        data_detail.state = random.randint(1,5)
        data_detail.date = time
        self.last_time = time
        info = pickle.dumps(data_detail)
        info += '####'
        self.sock.send(info)

class Gate:
    nodes = []
    def __init__(self, gate_id, port):
        self.gate_id = gate_id
        self.port = port
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind('127.0.0.1', port)
        self.sock = sock
        for i in range(1,random.randint(30,50)) do:
            self.nodes[i] = Node(sock, gate_id, i, randint(20,30))
            
if __name__ == '__main__':
    gates = []
    num = 1
    for port in PORT_TUPLE:
        gate = Gate(num, port)
        num += 1
    while True:
        time = int(time.time())
        for gate in gates:
            for node in gate.nodes
        
