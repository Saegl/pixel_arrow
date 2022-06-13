import socket
from contextlib import contextmanager

import upnpclient



used_device = None
used_ip = None

def myip() -> str:
    """Get local IP for port forwarding"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    s.connect(('8.8.8.8', 1))
    return s.getsockname()[0]


def set_port_forwarding(port: int) -> bool:
    """ This function is trying to open port using UPnP
    It goes through all devices and stops when it is possible to open the port
    Return value: True if success else otherwise
    """
    ip = myip()
    global used_device, used_ip

    for device in upnpclient.discover():
        add_port = device.find_action("AddPortMapping")

        if add_port is None:
            continue
        
        try:
            add_port(
                NewRemoteHost='0.0.0.0',
                NewExternalPort=port,
                NewProtocol='TCP',
                NewInternalPort=port,
                NewInternalClient=ip,
                NewEnabled='1',
                NewPortMappingDescription='CuteCats Pygame Client',
                NewLeaseDuration=10_000, # TODO Is this Lease duration ok?
            )
            used_device = device
            used_ip = ip
            return True
        except upnpclient.upnp.ValidationError:
            pass

def unset_port_forwarding(port):
    """Undo the function set_port_forwarding,
    do nothing if set_port_forwarding was never called or 
    unset_port_forwading called twice (i.e. it is safe to call this function
    multiple times)"""
    global used_device, used_ip

    if used_device is None:
        return

    delete_port = used_device.find_action('DeletePortMapping')
    # print(delete_port.args_in)
    delete_port(
        NewRemoteHost=used_ip,
        NewExternalPort=port,
        NewProtocol='TCP'
    )
    used_device = None
    used_ip = None

def my_external_ip() -> str:
    for device in upnpclient.discover():
        get_external_ip = device.find_action('GetExternalIPAddress')
        res = get_external_ip()
        return res['NewExternalIPAddress']


@contextmanager
def portforwarding(port):
    set_port_forwarding(port)
    ip = my_external_ip()
    try:
        yield ip
    finally:
        unset_port_forwarding(port)


# used_device = upnpclient.discover()[0]
# set_port_forwarding()
# print(unset_port_forwarding())
# print(myip())

# my_external_ip()
