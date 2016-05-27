# -*- coding: utf-8 -*-
import socket, select
import random
import pickle
import socket
import time

DATA_S_IP = '127.0.0.1'
DATA_S_PORT = 8484

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
		self.factory_id = factory_id
		self.gate_id = gate_id
		self.node_id = node_id
		self.type1 = random.randint(1,5)
		self.type2 = random.randint(6,10)
		self.type3 = random.randint(11,15)
		self.interval = interval
		
	def update(self, time):
		if(time >= self.last_time + self.interval):
			self.send_info(time)
			return True
		else:
			return False

	def send_info(self, time):
		data_detail['factory_id'] = self.factory_id
		data_detail['gate_id'] = self.gate_id
		data_detail['node_id'] = self.node_id
		data_detail['parameter_type1'] = self.type1
		data_detail['parameter_value1'] = random.randint(1,100)
		data_detail['parameter_type2'] = self.type2
		data_detail['parameter_value2'] = random.randint(1,100)
		data_detail['parameter_type3'] = self.type3
		data_detail['parameter_value3'] = random.randint(1,100)
		data_detail['record_time'] = time
		self.last_time = time
		info = pickle.dumps(data_detail)
		info += '####'
		self.sock.send(info)

class Gate:
	nodes = []
	def __init__(self, factory_id, gate_id, port):
		self.gate_id = gate_id
		self.port = port
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.bind(('127.0.0.1', port))
		sock.connect((DATA_S_IP, DATA_S_PORT))
		self.sock = sock
		for i in range(1,random.randint(30,50)):
			self.nodes.append(Node(sock, factory_id, gate_id, i, random.randint(20,30)))
		self.nodes_amount = len(self.nodes)
			
if __name__ == '__main__':
	gates = []
	port = 20003
	total_nodes_amount = 0
	for i in range(1,20):
		for j in range(1,random.randint(1,6)):
			gates.append(Gate(i, j, port))
			port += 1
			total_nodes_amount += gates[-1].nodes_amount
	while True:
		begin_time = time.time()
		nodes_amount = 0
		for gate in gates:
			for node in gate.nodes:
				if node.update(int(begin_time)):
					nodes_amount += 1
		end_time = time.time()
		duration = end_time - begin_time
		print 'UPDATE_NODES_AMOUNT:' + str(nodes_amount)
		if duration < 1:
			time.sleep(1 - duration)
		
