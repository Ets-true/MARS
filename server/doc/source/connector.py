import glob
import socket
import select
import serial
import sys

sock = socket.socket()


class ReadLine:
    """This class is used to create an object, that can optimize getting data from arduino board, cause it may take
        too long to parse it."""
    def __init__(self, s):
        self.buf = bytearray()
        self.s = s

    def readline(self):
        i = self.buf.find(b"\n")
        if i >= 0:
            r = self.buf[:i + 1]
            self.buf = self.buf[i + 1:]
            return r
        while True:
            i = max(1, min(2048, self.s.in_waiting))
            data = self.s.read(i)
            i = data.find(b"\n")
            if i >= 0:
                r = self.buf + data[:i + 1]
                self.buf[0:] = data[i + 1:]
                return r
            else:
                self.buf.extend(data)


def serial_ports():
    """This function is used to search connected serial ports on user's device.
       Returns array of connected ports.
       """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


def connect():
    """This function is used to connect to serial port
       It uses serial_ports() to identify connected ports
       After connection is established it automatically starts receiving data and trying to connect to server"""
    global realport, rl
    try:
        port = serial_ports()
        realport = serial.Serial(port[0], baudrate=9600, timeout=.01)
        rl = ReadLine(realport)
    except Exception as e:
        print(e)
    connect_server()


def connect_server():
    """This function is used to connect to our server
       After connection is established it automatically starts send data"""
    global sock
    sock = socket.socket()
    try:
        sock.connect(("0meka0.hopto.org", 443))
    except:
        print("connection error")
    sock.send(bytes("This is connector", "utf-8"))
    receive_send()


def receive_send():
    """This function is used to send data from serial port to server or receive data from server and send it
    through serial port."""
    global sock, rl
    while True:
        if realport.inWaiting() > 0:
            line = rl.readline().strip()
            if line:
                try:
                    sock.send(line + b'/')
                except:
                    connect_server()
        ready = select.select([sock], [], [], .1)
        if ready[0]:
            data = sock.recv(1024)
            if not data:
                sock.close()
            realport.write(data)
            realport.flush()


if __name__ == "__main__":
    connect()
