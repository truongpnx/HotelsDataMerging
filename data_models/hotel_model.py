from dataclasses import dataclass
from .amenites_model import Amenities
from .location_model import Location
from .images_model import Images


@dataclass
class Hotel:
  id: str
  destination_id: str
  name: str
  description: str
  location: Location
  amenities: Amenities
  images: Images
  booking_conditions: list[str]
