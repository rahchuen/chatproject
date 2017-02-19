import socket
import sys
from queue import Queue
import thread
import json

class Server():
  def __init__(self):
    self.clientWorkers = {}
    self.queueWorker = QueueWorker(clientWorkers)
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.server_address = ('localhost', 10000)

  def listenForConnection(self):
    sock.bind(server_address)
    sock.listen(1)

    while True:
      # Wait for a connection
      connection, client_address = sock.accept()
      message = json.loads(connection.recv()) 
      name = message['name']
      clientWorker = ClientWorker(connection, self.queueWorker)
      clientWorkers[name] = clientWorker
      clientWorker.run()

class ClientWorker(threading.Thread):
  def __init__(self, connection, queueWorker):
        self.connection = connection
        self.queueWorker = queueWorker
 
  def run(self):
    while True:
      message = json.loads(self.connection.recv())
      self.queueWorker.put(message)      

  def send(self, message):
    self.connection.sendall(message)

class QueueWorker(threading.Thread):
  def __init__(self, clientWorkers):
    self.clientWorkers = clientWorkers
    self.queue = Queue(maxsize=0)

  def put(message):
      self.queue.put(message)

  def run(self):
    while True:
      message = self.queue.get()
      for worker in clientWorkers.values():
        worker.send(json.dumps(message)) 
  
if __name__ == "__main__":
  server = Server()
  server.queueWorker.run()
  server.listenForConnection()

