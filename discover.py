from ssdpy import SSDPClient

client = SSDPClient()
devices = client.m_search("mariachi-devices")
for device in devices:
    print(device.get("usn"))
