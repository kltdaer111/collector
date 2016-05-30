# -*- coding: utf-8 -*-
import thread, threading
import mysql.connector
import socket, select
import copy
import pickle

MIN_SIZE = 5

data_buffer = []
lock = thread.allocate_lock()
con = threading.Condition(lock)

def push_to_database():
	cnx = mysql.connector.connect(user='root', password='juxienet',
                host='kakaroot.cn', port=53721,	database='work')
	cursor = cnx.cursor()
	insert_data = ("INSERT INTO wuxi "
			  "(factory_id, gate_id, node_id, record_time, parameter_type1, parameter_value1, parameter_type2, parameter_value2, parameter_type3, parameter_value3) "
			  "VALUES (%(factory_id)s, %(gate_id)s, %(node_id)s, FROM_UNIXTIME(%(record_time)s), %(parameter_type1)s, %(parameter_value1)s, %(parameter_type2)s, %(parameter_value2)s, %(parameter_type3)s, %(parameter_value3)s)")
	global data_buffer
	while True:
		con.acquire()
		if len(data_buffer) >= MIN_SIZE:
			print('db-thread will transport')
			copy_data = copy.deepcopy(data_buffer)
			data_buffer = []	
			con.release()
			for data in copy_data:
				try:
					cursor.execute(insert_data, data)
				except Exception, e:
					print e
			cnx.commit()
		else:
			print('db-thread will wait')
			con.wait()
			con.release()


def gather_in_buffer():
	serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	serversocket.bind(('0.0.0.0', 8484))
	serversocket.listen(5)
	serversocket.setblocking(0)
	epoll = select.epoll()
	epoll.register(serversocket.fileno(), select.EPOLLIN)
	try:
		connections = {}
		res = {}
		while True:
			events = epoll.poll(1)
			for fileno, event in events:
				#print('event:' + str(fileno))
				if fileno == serversocket.fileno():
					connection, address = serversocket.accept()
					connection.setblocking(0)
					epoll.register(connection.fileno(), select.EPOLLIN)
					connections[connection.fileno()] = connection
					print('Add a connection: ' + str(connection.fileno()))
				elif event & select.EPOLLIN:	 #读数据 如果完整直接入buffer，不完整等下次读完整再入  TODO：如何知道当前流已读完？
					#print('Receiving msg: ' + str(fileno))	
					if not res.has_key(fileno):
						res[fileno] = ''
					while True:
						cur_data = connections[fileno].recv(1024)
						#print 'cur_data:' + cur_data
						res[fileno] += cur_data	
						if res[fileno][-4:] == '####':
							break
					con.acquire()
					data_buffer.append(pickle.loads(res[fileno][:-4]))
					#print('Receiving')
					del res[fileno]
					if len(data_buffer) == MIN_SIZE:
						print('notify')
						con.notify()
					con.release()
				elif event & select.EPOLLHUP:
					epoll.unregister(fileno)
					connections[fileno].close()
					del connections[fileno]
	finally:
		epoll.unregister(serversocket.fileno())
		epoll.close()
		serversocket.close()

if __name__ == '__main__':
	t1 = thread.start_new_thread(push_to_database, ())
	t2 = thread.start_new_thread(gather_in_buffer, ())
	print t1, t2
	raw_input('collecting..')
