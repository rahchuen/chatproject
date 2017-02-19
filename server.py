import socket
import sys
from Queue import Queue
import threading
import json

class ClientWorker(threading.Thread):
  def __init__(self, connection, queueWorker):
    threading.Thread.__init__(self)
    self.connection = connection
    self.queueWorker = queueWorker
 
  def run(self):
    while True:
      message = self.connection.recv(1024)
      print message
      formattedMessage = json.loads(message)
      self.queueWorker.put(formattedMessage)      

  def send(self, message):
    self.connection.sendall(message)

class QueueWorker(threading.Thread):
  def __init__(self, clientWorkers):
    threading.Thread.__init__(self)
    self.clientWorkers = clientWorkers
    self.queue = Queue(maxsize=0)

  def put(self, message):
      self.queue.put(message)

  def run(self):
    while True:
      formattedMessage = self.queue.get()
      sender = formattedMessage['name']
      for receiver, clientWorker in self.clientWorkers.iteritems():
        if sender != receiver:
          clientWorker.send(json.dumps(formattedMessage)) 
  
class Server():
  def __init__(self):
    self.clientWorkers = {}
    self.queueWorker = QueueWorker(self.clientWorkers)
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.server_address = ('localhost', 10000)

  def listenForConnection(self):
    self.sock.bind(self.server_address)
    self.sock.listen(5)

    while True:
      # Wait for a connection
      connection, client_address = self.sock.accept()
      message = connection.recv(1024) 
      print message
      formattedMessage = json.loads(message) 
      name = formattedMessage['name']
      clientWorker = ClientWorker(connection, self.queueWorker)
      self.clientWorkers[name] = clientWorker
      clientWorker.start()

if __name__ == "__main__":
  server = Server()
  server.queueWorker.start()
  server.listenForConnection()

