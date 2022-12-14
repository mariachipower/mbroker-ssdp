import configparser
import os
import json
from datetime import datetime


config_name = "config.ini"


class Config:
    """The config in this example only holds devices."""

    def __init__(self):
        self.path = os.getcwd()
        self.devices = {}

    def add_device(self, device):
        s_mac = device["usn"]
        ts = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        if s_mac in [device_key for device_key in self.devices.keys()]:
            device_obj = json.loads(self.devices[s_mac].replace("'", '"'))
            device_obj["last_seen"] = ts
            self.devices[s_mac] = device_obj
        else:
            self.devices[s_mac] = {
                "last_seen": ts,
                "mac": s_mac,
                "host": device["host"],
                "device_ip": device["device_ip"],
                "nt": device["nt"],
                "nts": device["nts"]
            }

    def read_config(self):
        parser = configparser.RawConfigParser()
        parser.read([config_name])
        try:
            self.devices.update(parser.items("devices"))
        except configparser.NoSectionError:
            pass

    def write_config(self):
        parser = configparser.RawConfigParser()
        parser.add_section("devices")
        for key, value in self.devices.items():
            parser.set("devices", key, value)
        with open(config_name, "w") as file:
            parser.write(file)
