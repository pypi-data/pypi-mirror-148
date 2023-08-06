from datetime import timedelta, datetime
from ipaddress import IPv4Address, IPv6Address, IPv4Network, IPv6Network, ip_address, ip_network
from typing import Union, Optional, List, Generator

import requests
from requests import Session

from .models import Result


def lookup_ip(
        ip: Union[str, IPv4Address, IPv6Address],
        auth: Optional[str] = None,
        raise_on_missing: bool = False
) -> Result:
    '''
    :param ip: The IP address that you wish to lookup
    :param auth: Optional Authentication (Bearer token only)
    :param raise_on_missing: Optional raise error if not found
    :return: A Result object containing the result of the lookup
    '''
    if isinstance(ip, str):
        ip = ip_address(ip)
    if auth is None:
        result = requests.get(f"https://api.geoip.network/v1.0/cidr/{ip.compressed}")
    elif isinstance(auth, str):
        result = requests.get(f"https://api.geoip.network/v1.0/cidr/{ip.compressed}", headers={"Authorization": f"Bearer {auth}"})
    else:
        raise ValueError("invalid Authentication type, please supply bearer token or use the class")
    if raise_on_missing:
        result.raise_for_status()
    if result.status_code not in [requests.codes.ok, requests.codes.not_found]:
        result.raise_for_status()
    return Result.from_dict(result.json())


def lookup_cidr(
        cidr: Union[str, IPv4Network, IPv6Network],
        auth: Optional[str] = None,
        raise_on_missing: bool = False
) -> Result:
    '''
    :param cidr: The CIDR that you wish to lookup
    :param auth: Optional Authentication (Bearer token only)
    :param raise_on_missing: Optional raise error if not found
    :return: A Result object containing the result of the lookup
    '''
    if isinstance(cidr, str):
        cidr = ip_network(cidr)
    if auth is None:
        result = requests.get(f"https://api.geoip.network/v1.0/cidr/{cidr.compressed}")
    elif isinstance(auth, str):
        result = requests.get(f"https://api.geoip.network/v1.0/cidr/{cidr.compressed}", headers={"Authorization": f"Bearer {auth}"})
    else:
        raise ValueError("invalid Authentication type, please supply bearer token or use the class")
    if raise_on_missing:
        result.raise_for_status()
    if result.status_code not in [requests.codes.ok, requests.codes.not_found]:
        result.raise_for_status()
    return Result.from_dict(result.json())


def lookup_bulk(
        targets: List[Union[str, IPv4Address, IPv6Address, IPv4Network, IPv6Network]],
        auth: Optional[str] = None,
        raise_on_missing: bool = False,
) -> Generator[Result, None, None]:
    '''
    :param targets: A list of CIDRs and/or IPs that you wish to lookup
    :param auth: Optional Authentication (Bearer token only)
    :param raise_on_missing: Optional raise error if not found
    :return: A Result object containing the result of the lookup
    '''
    clean_targets = []
    for cidr in targets:
        if isinstance(cidr, str):
            clean_targets.append(ip_network(cidr).compressed)
        elif isinstance(cidr, IPv4Network) or isinstance(cidr, IPv6Network):
            clean_targets.append(cidr.compressed)
        elif isinstance(cidr, IPv4Address) or isinstance(cidr, IPv6Address):
            clean_targets.append(cidr.compressed)
        else:
            raise ValueError("invalid target - must be either IP or CIDR")
    if auth is None:
        result = requests.post(f"https://api.geoip.network/v1.0/cidrs", json=clean_targets)
    elif isinstance(auth, str):
        result = requests.post(f"https://api.geoip.network/v1.0/cidrs", headers={"Authorization": f"Bearer {auth}"}, json=clean_targets)
    else:
        raise ValueError("invalid Authentication type, please supply bearer token or use the class")
    if raise_on_missing:
        result.raise_for_status()
    if result.status_code not in [requests.codes.ok, requests.codes.not_found]:
        result.raise_for_status()
    for row in result.json():
        yield Result.from_dict(row)


class GeoIP:

    def __init__(self, username: str, password: str):
        self.session = Session()
        request_time = datetime.now()
        result = self.session.post("https://auth.geoip.network/v1.0/login", auth=(username, password))
        result.raise_for_status()
        self.refresh = request_time + timedelta(seconds=result.json().get("ttl")-5)
        self._key = result.json().get("refresh")
        self._username = username
        self._password = password

    def lookup_ip(
            self,
            ip: Union[str, IPv4Address, IPv6Address],
            raise_on_missing: bool = False
    ) -> Result:
        '''
        :param ip: The IP address that you wish to lookup
        :param auth: Optional Authentication (Bearer token only)
        :param raise_on_missing: Optional raise error if not found
        :return: A Result object containing the result of the lookup
        '''
        if isinstance(ip, str):
            ip = ip_address(ip)
        result = self._request(ip)
        if raise_on_missing:
            result.raise_for_status()
        if result.status_code not in [requests.codes.ok, requests.codes.not_found]:
            result.raise_for_status()
        return Result.from_dict(result.json())

    def lookup_cidr(
            self,
            cidr: Union[str, IPv4Network, IPv6Network],
            raise_on_missing: bool = False
    ) -> Result:
        '''
        :param cidr: The CIDR that you wish to lookup
        :param auth: Optional Authentication (Bearer token only)
        :param raise_on_missing: Optional raise error if not found
        :return: A Result object containing the result of the lookup
        '''
        if isinstance(cidr, str):
            cidr = ip_network(cidr)
        result = self._request(cidr)
        if raise_on_missing:
            result.raise_for_status()
        if result.status_code not in [requests.codes.ok, requests.codes.not_found]:
            result.raise_for_status()
        return Result.from_dict(result.json())

    def lookup_bulk(
            self,
            targets: List[Union[str, IPv4Address, IPv6Address, IPv4Network, IPv6Network]],
            raise_on_missing: bool = False
    ) -> Generator[Result, None, None]:
        '''
        :param targets: A list of CIDRs and/or IPs that you wish to lookup
        :param raise_on_missing: Optional raise error if not found
        :return: A Result object containing the result of the lookup
        '''
        clean_targets = []
        for cidr in targets:
            if isinstance(cidr, str):
                clean_targets.append(ip_network(cidr).compressed)
            elif isinstance(cidr, IPv4Network) or isinstance(cidr, IPv6Network):
                clean_targets.append(cidr.compressed)
            elif isinstance(cidr, IPv4Address) or isinstance(cidr, IPv6Address):
                clean_targets.append(cidr.compressed)
            else:
                raise ValueError("invalid target - must be either IP or CIDR")
        result = self._request_bulk(clean_targets)
        if raise_on_missing:
            result.raise_for_status()
        if result.status_code not in [requests.codes.ok, requests.codes.not_found]:
            result.raise_for_status()
        for row in result.json():
                yield Result.from_dict(row)

    def _request(self, cidr: Union[IPv4Network, IPv6Network, IPv4Address, IPv6Address]) -> requests.Response:
        if datetime.now() > self.refresh:
            self._reauth()
        result = self.session.get(f"https://api.geoip.network/v1.0/cidr/{cidr.compressed}")
        if result.status_code == requests.codes.unauthorized:
            self._reauth()
            result = self.session.get(f"https://api.geoip.network/v1.0/cidr/{cidr.compressed}")
        return result

    def _request_bulk(self, cidrs: List[Union[IPv4Network, IPv6Network, IPv4Address, IPv6Address]]) -> requests.Response:
        if datetime.now() > self.refresh:
            self._reauth()
        result = self.session.post(f"https://api.geoip.network/v1.0/cidrs", json=cidrs)
        if result.status_code == requests.codes.unauthorized:
            self._reauth()
            result = self.session.get(f"https://api.geoip.network/v1.0/cidrs", json=cidrs)
        return result

    def _reauth(self):
        if datetime.now() > self.refresh+timedelta(seconds=5):
            request_time = datetime.now()
            result = self.session.post("https://auth.geoip.network/v1.0/login", auth=(self._username, self._password))
            result.raise_for_status()
            self.refresh = request_time + timedelta(seconds=result.json().get("ttl") - 5)
            self._key = result.json().get("refresh")
        else:
            request_time = datetime.now()
            result = self.session.post("https://auth.geoip.network/v1.0/login", headers={
                "X-RENEW-KEY": self._key
            })
            if result.status_code != requests.codes.ok:
                result = self.session.post("https://auth.geoip.network/v1.0/login",
                                           auth=(self._username, self._password))
                result.raise_for_status()
            self.refresh = request_time + timedelta(seconds=result.json().get("ttl") - 5)
            self._key = result.json().get("refresh")

