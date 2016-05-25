# -*- coding: utf-8 -*-
import thread, threading
import mysql.connector
import socket, select

MIN_SIZE = 5

data_buffer = []
lock = thread.allocate_lock()
con = threading.Condition(lock)

def push_to_database():
    cnx = mysql.connector.connect(user='root', password='abcdef',
                                  host='192.168.253.133',
                                  database='data')
    cursor = cnx.cursor()
    insert_data = ("INSERT INTO data_record "
              "(id, state, date) "
              "VALUES (%(id)s, %(state)s, %(date)s")
    while True:
        if len(data_buffer) >= MIN_SIZE:
            con.acquire()
            for data in data_buffer:
                cursor.execute(insert_data, data)
            data_buffer = []
            cursor.commit()
            con.release()
        else:
            con.wait()


def gather_in_buffer():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind(('0.0.0.0', 8484))
    serversocket.listen(5)
    serversocket.setblocking(0)
    epoll = select.epoll()
    epoll.register(serversocket.fileno(), select.EPOLLLIN)
    try:
        connections = {}
        res = {}
        while True:
            events = epoll.poll(1)
            for fileno, event in events:
                if fileno == serversocket.fileno():
                    connection, address = serversocket.accept()
                    connection.setblocking(0)
                    epoll.register(connection.fileno(), select.EPOLLIN)
                    connections[connection.fileno()] = connection
                elif event & select.EPOLLIN:     #读数据 如果完整直接入buffer，不完整等下次读完整再入  TODO：如何知道当前流已读完？
                    if !res.has_key(fileno):
                        res[fileno] = ''
                    while True:
                        cur_data = connections[fileno].recv(1024)
                        res[fileno] += cur_data
                        if not cur_data:
                            break
                    if res[fileno][-4:] = '####':
                        con.acquire()
                        data_buffer.append(res[fileno])
                        del res[fileno]
                        if len(data_buffer) == MIN_SIZE:
                            con.notify()
                        else:
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
    t1 = thread.start_new_thread(push_to_database)
    t2 = thread.start_new_thread(gather_in_buffer)
    t1.join()
    t2.join()
