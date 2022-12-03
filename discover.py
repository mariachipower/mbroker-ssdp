from ssdpy import SSDPClient
from config import Config
import os
import click
from pickle import FALSE

pass_config = click.make_pass_decorator(Config, ensure=True)


class State:
    pass


state = State()
state.devices = []


@pass_config
def config_exists(config):
    """Creates config.json + dirs for each mac address found. Warns if run in a project dir. User to optionally provide a list of mac addresses (obtained with mariachi status –-netscan)"""
    if os.path.exists('config.ini'):
        click.echo(
            "Config file already exist in this folder. Please move to an empty directory and run mbroker init again.")
    else:
        return FALSE


def scanForDevices():
    client = SSDPClient()
    state.devices = client.m_search("mariachi-devices")


def printDevices():
    for device in state.devices:
        click.echo(f'{device.get("usn")} {device.get("device_ip")}')


@click.command()
@click.option(
    "--scan",
    is_flag=True,
    show_default=True,
    default=False,
    help="Scan for devices not in network."
)
@click.option(
    "--init",
    is_flag=True,
    show_default=True,
    default=False,
    help="Scan for devices not in network."
)
@click.option(
    "--verbose",
    is_flag=True,
    show_default=True,
    default=False,
    help="Verbose output."
)
def netstatus(scan, init, verbose):
    if scan:
        """(-scan): scans for other devices
        Scan network and show status of all devices found"""
        scanForDevices()
    elif init:
        """(-init): scans for other devices
        Scan network and show status of all devices found
        Creates CONFIG"""
        scanForDevices()
    else:
        """(DEFAULT): Reads CONFIG. Pulls status from all network devices. Does config exists?
        Y → Scan network and show status of devices in config file
        N → Warns there is no config and suggest using –scan"""
        scanForDevices()

        """Simple program that greets NAME for a total of COUNT times."""
        if config_exists():
            click.echo(
                "Config file does not Exist in this folder. Add option -scan to look for Mariachi devices in your LAN anyway.")

    printDevices()


if __name__ == '__main__':
    netstatus()
