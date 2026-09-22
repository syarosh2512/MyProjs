import scapy
from scapy import *

def ping(host):
    packet = IP (dst=host)/ICMP()
    response = sr1(packet, timeout=2, verbose=0)
    if response:
        return f"{host} is online"
    else:
        return f"{host} is offline"

hostscan = "10.221.131.9"
result = ping(hostscan)