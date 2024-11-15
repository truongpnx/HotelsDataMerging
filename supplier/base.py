from abc import abstractmethod
import requests

from data_models import Hotel


class BaseSupplier:

  @abstractmethod
  def endpoint(self) -> str:
    """URL to fetch supplier data"""

  @abstractmethod
  def parse(self, obj: dict) -> Hotel:
    """Parse supplier-provided data into Hotel object"""

  def fetch(self):
    url = self.endpoint()
    resp = requests.get(url)
    return [self.parse(dto) for dto in resp.json()]
