# -*- coding: utf-8 -*-
import socket, select
import random
import pickle
import socket
import time
TYPE_AMOUNT = 10
PORT_TUPLE = (19455,19456,19457,19458,19568,19569,19570,19571,19572,19573)
data_detail = {
    'factory_id' : 0,
    'gate_id' : 0,
    'node_id' : 0,
    'record_time' : 0,
    'parameter_type1' : 0,
    'parameter_value1' : 0,
    'parameter_type2' : 0,
    'parameter_value2' : 0,
    'parameter_type3' : 0,
    'parameter_value4' : 0,
    }

class Node:
    last_time = 0
    def __init__(self, sock, factory_id, gate_id, node_id, interval):
        self.sock = sock
        self.gate_id = gate_id
        self.node_id = node_id
        self.type1 = random.randint(1,5)
        self.type2 = random.randint(6,10)
        self.type3 = random.randint(11,15)
        self.interval = interval
        
    def update(self, time):
        if(time >= last_time + interval):
            self.send_info(time)

    def send_info(self, time):
        data_detail.factory_id = self.factory_id
        data_detail.gate_id = self.gate_id
        data_detail.node_id = self.node_id
        data_detail.parameter_type1 = self.type1
        data_detail.parameter_value1 = random.randint(1,100)
        data_detail.parameter_type2 = self.type2
        data_detail.parameter_value2 = random.randint(1,100)
        data_detail.parameter_type3 = self.type3
        data_detail.parameter_value3 = random.randint(1,100)
        data_detail.record_time = time
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
        begin_time = time.time()
        for gate in gates:
            for node in gate.nodes:
                node.update(int(begin_time))
        end_time = time.time
        duration = end_time - begin_time
        if duration < 1:
            time.sleep(1 - duration)
        
