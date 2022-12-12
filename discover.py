from ssdpy import SSDPClient
from config import Config
import os
import click
from pickle import FALSE

pass_config = click.make_pass_decorator(Config, ensure=True)


@pass_config
def write_config(config):
    config.write_config()


@pass_config
def read_config(config):
    config.read_config()


@pass_config
def scan_for_devices(config):
    client = SSDPClient()
    devices = client.m_search("mariachi-devices")
    for device in devices:
        config.add_device(device)


def print_devices(devices):
    ctx = click.get_current_context()
    verbose = ctx.params["verbose"]
    for key, value in devices.items():
        click.echo(f'{key} {value}')


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
@pass_config
def netstatus(config, scan, init, verbose):
    if scan:
        """(-scan): scans for other devices
        Scan network and show status of all devices found"""
        scan_for_devices()
        print_devices(config.devices)
    elif init:
        """(-init): scans for other devices
        Scan network and show status of all devices found
        Creates CONFIG"""
        if os.path.exists('config.ini'):
            click.echo(
                "Config file already exist in this folder. Please move to an empty directory and run mbroker init again.")
        else:
            scan_for_devices()
            write_config()
            print_devices(config.devices)

    else:
        """(DEFAULT): Reads CONFIG. Pulls status from all network devices. Does config exists?
        Y → Scan network and show status of devices in config file
        N → Warns there is no config and suggest using –scan"""
        if os.path.exists('config.ini'):
            read_config()
            scan_for_devices()
            write_config()
            print_devices(config.devices)
        else:
            click.echo(
                "Config file does not exist in this folder. Run mbroker init in order to create one.")


if __name__ == '__main__':
    netstatus()
