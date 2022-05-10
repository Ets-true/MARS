import socket
import select
import threading
import mysql.connector
from datetime import datetime, timedelta
import time
import json
from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler

'''
cnx1 = mysql.connector.connect(user="root",
                               password="12345",
                               host='192.168.0.102',
                               database='Data')

cnx2 = mysql.connector.connect(user="root",
                               password="12345",
                               host='192.168.0.102',
                               database='Data')

cursor1 = cnx1.cursor(buffered=True)
cursor2 = cnx2.cursor(buffered=True)
'''

sock = socket.socket()
sock.bind(('192.168.0.103', 443))
sock.listen(5)

hostName = "192.168.0.103"
serverPort = 80


class MyServer(BaseHTTPRequestHandler):
    """This class is used to create an instance of http server to send data to web interface."""
    def do_GET(self):
        if datetime.now().second % 5 == 0:
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(bytes(json.dumps(get_data_web()), "utf-8"))
            time.sleep(1)


def connected():
    """This function is used to accept tcp connection from connector module or android client."""
    global sock
    while True:
        ready = select.select([sock], [], [], .1)
        if ready[0]:
            conn, addr = sock.accept()
            try:
                check = conn.recv(512)
                if check.decode() == "This is connector":
                    print('connected new connector:', addr)
                    threading._start_new_thread(receive_connector, (conn,))
                elif check.decode() == "This is android client":
                    print('connected new android client:', addr)
                    threading._start_new_thread(send_android, (conn,))
            except:
                pass


def receive_connector(client):
    """This function is used to receive data from connector module."""
    global received, connector_send
    while True:
        data = client.recv(512)
        received = data[:-1]
        if not data:
            client.close()
            # add_data(data.decode())
            # print(data.decode())

        def connector_send(data):
            client.send(data)


def send_android(client):
    """This function is used to send data to android client or receive it."""
    global received_android
    while True:
        '''
        index = index + 1
        dict_res = {"Moisture": 0, "Moisture_Time": 0, "CO2": 0, "CO2_Time": 0, "Motion": 0, "Motion_Time": 0,
                    "Illumination": 0, "Illumination_Time": 0}
        dict_init = {"Moisture": 0, "CO2": 0, "Motion": 0, "Illumination": 0}
        for key in dict_init.keys():
            sql = "select * from " + str(key) + " LIMIT 1 OFFSET " + str(index)
            cursor2.execute(sql)
            records = cursor2.fetchall()
            dict_res[key] = records[0][0]
            dict_res[key + "_Time"] = records[0][1]
        '''
        try:
            client.send(bytes(get_data() + b"/"))
        except:
            pass
        ready = select.select([client], [], [], .1)
        if ready[0]:
            data = client.recv(1024)
            connector_send(data)


def add_data(data):
    dict = json.loads(data[0:data.find('/')])
    for key in dict.keys():
        sql = "insert into " + str(key) + " (" + str(key) + ", Time) values (%s, %s)"
        val = (dict[key], str(datetime.now()))
        cursor1.execute(sql, val)
        cnx1.commit()
    data = data[data.find('/') + 1:]
    if data != "":
        add_data(data)


def start_server(server):
    """This function is used to start http server"""
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass

    server.server_close()
    print("Server stopped.")


def roundTime(dt=None, roundTo=1):
    """This function is used to round up the time to minutes."""
    if dt is None: dt = datetime.datetime.now()
    seconds = (dt.replace(tzinfo=None) - dt.min).seconds
    rounding = (seconds + roundTo / 2) // roundTo * roundTo
    return dt + timedelta(0, rounding - seconds, -dt.microsecond)


def get_data():
    return received


def get_data_web():
    """This function is used to parse data to send it to web interface"""
    dict_res = {"Moisture": 0, "CO2": 0, "Motion": 0, "Illumination": 0, "Time": 0}
    dict_init = json.loads(received)
    for key in dict_init.keys():
        dict_res[key] = dict_init[key]
    dict_res["Time"] = str(roundTime(datetime.now()))
    return dict_res


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))
    threading._start_new_thread(start_server, (webServer,))
    connected()
