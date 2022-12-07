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

    def add_device(self, mac):
        print(f'>>> add_device {mac}')
        s_mac = str(mac)
        print(self.devices)
        ts = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        if s_mac in self.devices:
            device_obj = json.loads(self.devices[s_mac].replace("'", '"'))
            print(f'     >>> UPDATING {s_mac}')
            print(device_obj)
            device_obj["last_seen"] = ts
        else:
            print(f'     >>> INSERTING {s_mac}')
            self.devices[s_mac] = {
                "last_seen": ts
            }

    def read_config(self):
        print('>>> read_config')
        parser = configparser.RawConfigParser()
        parser.read([config_name])
        try:
            self.devices.update(parser.items("devices"))
        except configparser.NoSectionError:
            pass

    def write_config(self):
        print('>>> write_config')
        parser = configparser.RawConfigParser()
        parser.add_section("devices")
        for key, value in self.devices.items():
            parser.set("devices", key, value)
        with open(config_name, "w") as file:
            parser.write(file)
