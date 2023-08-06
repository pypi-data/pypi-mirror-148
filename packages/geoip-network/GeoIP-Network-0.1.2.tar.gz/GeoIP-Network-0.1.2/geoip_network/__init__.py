"""
GeoIP-Network
~~~~~~~~~~~~
The official GeoIP.Network Library.
This library uses GeoIP.Network to resolve IP addresses to locations.
GeoIP.Network is a Not-For-Profit and Open-Source project that aims to deliver the accurate GeoIP data.
"""


__author__ = 'Tim Armstrong'
__license__ = 'MIT'

from .geoip_network import lookup_cidr, lookup_ip, lookup_bulk, GeoIP