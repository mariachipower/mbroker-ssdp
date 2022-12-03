from ssdpy import SSDPServer
from random import randrange

from socket import gethostbyname, gethostname

# get our IP. Be careful if you have multiple network interfaces or IPs
hostname = gethostname()
host_ip = gethostbyname(hostname)

id = randrange(100)
full_name = f'mac_{id}'
full_port = 1900

print(full_name)
print(f'{host_ip}:{full_port}')

extra = {
    'device_ip': host_ip
}
server = SSDPServer(full_name, device_type="mariachi-devices",
                    port=full_port, extra_fields=extra)
server.serve_forever()
