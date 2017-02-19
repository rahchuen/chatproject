import json
import socket
import sys
import threading
import uuid


class Client():
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, ip, port):
        serverAddress = (ip, port)
        self.sock.connect(serverAddress)
        self.sock.sendall("{name: " + self.name + ", msg: ack}")

    def waitForMessage(self):
        while True:
            msg = raw_input(name + ": ")
            self.sock.sendall("{name: " + self.name + ", msg: " + msg + "}")


class RecvWorker(threading.Thread):
    def __init__(self, sock):
        self.sock = sock

    def run(self):
        while True:
            msg = json.loads(self.sock.recv())
            print msg["name"] + ": " + msg["msg"] + "\n"


if __name__ == "__main__":
    ip = sys.argv[2]
    port = sys.argv[3]
    uid = uuid.uuid4()
    name = sys.argv[4] + uid
    client = Client(ip, port)
    client.connect(ip, port)
    client.waitForMessage()
