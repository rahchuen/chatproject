import json
import socket
import sys
import threading
import uuid


class Client():
    def __init__(self, name):
        self.name = name
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.recvWorker = RecvWorker(self.sock)

    def connect(self, ip, port):
        serverAddress = (ip, port)
        self.sock.connect(serverAddress)
        data = {}
        data["name"] = self.name
        data["msg"] = "ack"
        self.sock.sendall(json.dumps(data))

    def waitForMessage(self):
        while True:
            msg = raw_input(self.name.split(':')[0] + ": ")
            data = {}
            data["name"] = self.name
            data["msg"] = msg
            self.sock.sendall(json.dumps(data))


class RecvWorker(threading.Thread):
    def __init__(self, sock):
        threading.Thread.__init__(self)
        self.sock = sock

    def run(self):
        while True:
            msg = json.loads(self.sock.recv(1024))
            print msg["name"].split(':')[0] + ": " + msg["msg"] + "\n"


if __name__ == "__main__":
    ip = sys.argv[1]
    port = int(sys.argv[2])
    uid = str(uuid.uuid4())
    name = sys.argv[3] + ":" + uid
    client = Client(name)
    client.connect(ip, port)
    client.recvWorker.start()
    client.waitForMessage()
