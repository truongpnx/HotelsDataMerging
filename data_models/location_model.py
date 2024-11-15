from dataclasses import dataclass


@dataclass
class Location:
  lat: float
  lng: float
  address: str
  city: str
  country: str
