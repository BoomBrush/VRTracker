import zmq, json, time, sys, struct
from collections import namedtuple
from construct import Int32ub, Int32ul, Float32l, Struct, Const, Padded, Array
from math import pi

#All this class does is prints messages to the screen so I can see what going on.
class debug: 
    def __init__(self, socket):
        self.socket = socket
        
    def send(self, text):
        self.socket.send(text)
        print("Send: " + str(text))

    def recv(self):
        recieved = self.socket.recv()
        print("Recived: " + str(recieved))
        return recieved

# Setup some fancy ZMQ socket stuff and connect to the vridge api
context = zmq.Context()
control_channel = context.socket(zmq.REQ)
control_channel.connect("tcp://127.0.0.1:38219")
# First you connect to a control channel (setting up debug class)
vridge_control = debug(control_channel)

# Say hi (this doesnt do anything just confirms everything works)
vridge_control.send('{"ProtocolVersion":1,"Code":2}')
vridge_control.recv()

# Request special connection for head tracking stuff
vridge_control.send('{"RequestedEndpointName":"HeadTracking","ProtocolVersion":1,"Code":1}')
newconnection = json.loads(vridge_control.recv())
#vridge_control.close() # Close socket

# Connect to new socket (timeout is normally 15 seconds)
endpoint_address = newconnection['EndpointAddress']
endpoint = context.socket(zmq.REQ)
endpoint.connect(endpoint_address)
# Connect to the endpoint channel (setting up debug class)
vridge_endpoint = debug(endpoint)

# Specify the structure for the fancy position matrix
structure = Struct(
        Const(Int32ul, 2),
        Const(Int32ul, 3),
        Const(Int32ul, 24),
        "data" / Padded(64, Array(6, Float32l)),
)

while True:
    for i in range(100):    
        position = [0.0, 0.0, pi, 0.0, 1.0+(i*0.04), 0.0]
        byte_packet = structure.build(dict(data=position))
        endpoint.send(byte_packet)
        print("Send: " + str(structure.parse(byte_packet)))
        #print("Recieved: " + str(structure.parse(endpoint.recv())))
        endpoint.recv()

        time.sleep(0.1)
