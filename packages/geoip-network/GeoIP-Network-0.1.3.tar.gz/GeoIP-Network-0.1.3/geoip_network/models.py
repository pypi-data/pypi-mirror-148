from dataclasses import dataclass, field
from ipaddress import IPv4Network, IPv6Network, ip_network
from typing import Union, Dict
from datetime import datetime


@dataclass
class Location:
    longitude: float
    latitude: float
    radius: float


@dataclass(init=False)
class Result:
    error: bool = field(default=False)
    allocated_cc: str = field(default="")
    as_name: str = field(default="")
    asn: str = field(default="")
    cidr: Union[IPv4Network, IPv6Network] = ip_network("::/0")
    rir: str = field(default="")
    timestamp: int = field(default=0)
    datetime: datetime = field(default_factory=datetime.now)
    location: Location = field(default_factory=Location)

    def __repr__(self):
        return f"Result.from_dict({self.to_dict()})"

    @classmethod
    def from_dict(cls, obj: Dict):
        if "error" in obj:
            new = cls()
            new.error = True
        else:
            loc = obj.get("geo", {}).get("geometry", {}).get("coordinates", [0, 0])
            radius = obj.get("geo", {}).get("properties", {}).get("radius", -1.0)
            new = cls()
            new.error = False
            new.allocated_cc = obj.get("allocated_cc", "")
            new.as_name = obj.get("as-name") or obj.get("as_name", "")
            new.asn = obj.get("asn", "")
            new.cidr = ip_network(obj.get("cidr", "::/0"))
            new.rir = obj.get("rir", "")
            new.timestamp = obj.get("timestamp", int(datetime.now().timestamp()))
            new.datetime = datetime.fromtimestamp(obj.get("timestamp", int(datetime.now().timestamp())))
            new.location = Location(loc[0], loc[1], radius)
        return new

    def to_dict(self):
        if not self.error:
            output = {
                "allocated_cc": self.allocated_cc,
                "as-name": self.as_name,
                "asn": self.asn,
                "cidr": self.cidr.compressed,
                "geo": {
                    "geometry": {
                        "coordinates": [
                            self.location.longitude,
                            self.location.latitude
                        ],
                        "type": "Point"
                    },
                    "properties": {
                        "radius": self.location.radius
                    },
                    "type": "Feature"
                },
                "rir": self.rir,
                "timestamp": self.timestamp
            }
        else:
            output = {
                "error": "no covering prefix found"
            }
        return output



