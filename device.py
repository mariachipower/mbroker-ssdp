from ssdpy import SSDPServer
from random import randrange

id = randrange(100)
full_name = f'mac1_{id}'
print(full_name)

port = randrange(50)
full_port = 1900 + port
print(full_port)
server = SSDPServer(full_name, device_type="mariachi-devices", port=full_port)
server.serve_forever()
