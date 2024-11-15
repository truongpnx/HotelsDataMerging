from dataclasses import dataclass


@dataclass
class Image:
  link: str
  description: str


@dataclass
class Images:
  rooms: list[Image]
  site: list[Image]
  amenities: list[Image]
