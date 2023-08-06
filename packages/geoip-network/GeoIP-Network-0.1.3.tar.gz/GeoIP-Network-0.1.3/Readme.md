# GeoIP.Network Python Library
![Release Badge](https://gitlab.com/geoip.network/python-library/-/badges/release.svg)
![Pipeline Badge](https://gitlab.com/geoip.network/python-library/badges/master/pipeline.svg)

The official python interface to GeoIP.Network

![Screenshot of example code below](https://gitlab.com/geoip.network/python-library/-/raw/031021231b1275e3b015b178a39ed2f7b61c3450/screenshots/screenshot.png)

Localize IP addresses instantly anywhere in the world.

Improve your customer’s experience and optimize your marketing by using GeoIP.Network to discover your client’s location in real-time.

Our API is free to use for up to 10,000 requests per day (more than most commercial projects offer per month in their paid packages) - or unlimited if you sponsor the project for the cost of a cup of coffee per month.
Discover details like ISP, Country, and Location instantly.
GeoIP.Network is a Not-For-Profit (and open-source) project that aims to provide reliable and accurate IP localization data for free to everyone. Building on research done at world leading universities, we use a blend of information from the Internet Routing Registry (IRR), live BGP streams, and a stochastic-progressive latency measurement algorithm to provide the most up-to-date and accurate data possible.

TLDR; We use science and public data and offer accurate GeoIP data for free.

## Usage (free < 10000 requests / day):

___NOTE: The following IP addresses are Documentation addresses. As such you will need to replace them with valid public IP addresses for these examples to work.___

```python
import geoip_network
# Single IP
result = geoip_network.lookup_ip("198.51.100.1")
print(result.to_dict())
# {"allocated_cc": "--", "as-name": "Documentation ASN", "asn": "AS64496", "cidr": "198.51.100.0/24", "geo": {"geometry": {"coordinates": [-112.404207, 45.73643438], "type": "Point"}, "properties": {"radius": 0.0}, "type": "Feature"}, "rir": "IANA", "timestamp": 1643422555},

# IP Range (CIDR)
result = geoip_network.lookup_cidr("198.51.100.0/24")
print(result.to_dict())
# {"allocated_cc": "--", "as-name": "Documentation ASN", "asn": "AS64496", "cidr": "198.51.100.0/24", "geo": {"geometry": {"coordinates": [-112.404207, 45.73643438], "type": "Point"}, "properties": {"radius": 0.0}, "type": "Feature"}, "rir": "IANA", "timestamp": 1643422555},

# Bulk lookup
for result in geoip_network.lookup_bulk(["2001:db8::/48", "198.51.100.1", "0.0.0.0/24"]):
    print(result.to_dict())
# {"allocated_cc": "--", "as-name": "Documentation ASN", "asn": "AS64496", "cidr": "2001:db8::/32", "geo": {"geometry": {"coordinates": [16.72425629, 62.88018421], "type": "Point"}, "properties": {"radius": 0.0}, "type": "Feature"}, "rir": "IANA", "timestamp": 1634593342},
# {"allocated_cc": "--", "as-name": "Documentation ASN", "asn": "AS64496", "cidr": "198.51.100.0/24", "geo": {"geometry": {"coordinates": [-112.404207, 45.73643438], "type": "Point"}, "properties": {"radius": 0.0}, "type": "Feature"}, "rir": "IANA", "timestamp": 1643422555},
# {"error": "no covering prefix found"}
```

## Usage (sponsor):
___NOTE: The following IP addresses are Documentation addresses. As such you will need to replace them with valid public IP addresses for these examples to work.___
```python
import geoip_network
# Login

geoip = geoip_network.GeoIP("api_username", "api_password")
# Single IP

result = geoip.lookup_ip("198.51.100.1")
print(result.to_dict())
# {"allocated_cc": "--", "as-name": "Documentation ASN", "asn": "AS64496", "cidr": "198.51.100.0/24", "geo": {"geometry": {"coordinates": [-112.404207, 45.73643438], "type": "Point"}, "properties": {"radius": 0.0}, "type": "Feature"}, "rir": "IANA", "timestamp": 1643422555},

# IP Range (CIDR)
result = geoip.lookup_cidr("198.51.100.0/24")
print(result.to_dict())
# {"allocated_cc": "--", "as-name": "Documentation ASN", "asn": "AS64496", "cidr": "198.51.100.0/24", "geo": {"geometry": {"coordinates": [-112.404207, 45.73643438], "type": "Point"}, "properties": {"radius": 0.0}, "type": "Feature"}, "rir": "IANA", "timestamp": 1643422555},

# Bulk lookup
for result in geoip.lookup_bulk(["2001:db8::/48", "198.51.100.1", "0.0.0.0/24"]):
    print(result.to_dict())
# {"allocated_cc": "--", "as-name": "Documentation ASN", "asn": "AS64496", "cidr": "2001:db8::/32", "geo": {"geometry": {"coordinates": [16.72425629, 62.88018421], "type": "Point"}, "properties": {"radius": 0.0}, "type": "Feature"}, "rir": "IANA", "timestamp": 1634593342},
# {"allocated_cc": "--", "as-name": "Documentation ASN", "asn": "AS64496", "cidr": "198.51.100.0/24", "geo": {"geometry": {"coordinates": [-112.404207, 45.73643438], "type": "Point"}, "properties": {"radius": 0.0}, "type": "Feature"}, "rir": "IANA", "timestamp": 1643422555},
# {"error": "no covering prefix found"}
```
### Alternatively
___NOTE: The following IP addresses are Documentation addresses. As such you will need to replace them with valid public IP addresses for these examples to work.___
```python
import geoip_network
# Single IP

result = geoip_network.lookup_ip("198.51.100.1", auth="<bearer_token>")
print(result.to_dict())
# {"allocated_cc": "--", "as-name": "Documentation ASN", "asn": "AS64496", "cidr": "198.51.100.0/24", "geo": {"geometry": {"coordinates": [-112.404207, 45.73643438], "type": "Point"}, "properties": {"radius": 0.0}, "type": "Feature"}, "rir": "IANA", "timestamp": 1643422555},

# IP Range (CIDR)
result = geoip_network.lookup_cidr("198.51.100.0/24", auth="<bearer_token>")
print(result.to_dict())
# {"allocated_cc": "--", "as-name": "Documentation ASN", "asn": "AS64496", "cidr": "198.51.100.0/24", "geo": {"geometry": {"coordinates": [-112.404207, 45.73643438], "type": "Point"}, "properties": {"radius": 0.0}, "type": "Feature"}, "rir": "IANA", "timestamp": 1643422555},

# Bulk lookup
for result in geoip_network.lookup_bulk(["2001:db8::/48", "198.51.100.1", "0.0.0.0/24"], auth="<bearer_token>"):
    print(result.to_dict())
# {"allocated_cc": "--", "as-name": "Documentation ASN", "asn": "AS64496", "cidr": "2001:db8::/32", "geo": {"geometry": {"coordinates": [16.72425629, 62.88018421], "type": "Point"}, "properties": {"radius": 0.0}, "type": "Feature"}, "rir": "IANA", "timestamp": 1634593342},
# {"allocated_cc": "--", "as-name": "Documentation ASN", "asn": "AS64496", "cidr": "198.51.100.0/24", "geo": {"geometry": {"coordinates": [-112.404207, 45.73643438], "type": "Point"}, "properties": {"radius": 0.0}, "type": "Feature"}, "rir": "IANA", "timestamp": 1643422555},
# {"error": "no covering prefix found"}
```

## Installation (from pip):
```shell
pip install geoip_network
```

## Installation (from source):
```shell
git clone https://gitlab.com/geoip.network/python-library
poetry install
```
