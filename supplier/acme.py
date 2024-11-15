from .base import BaseSupplier

from data_models import Hotel, Location, Amenities, Images


class Acme(BaseSupplier):

    def endpoint(self):
        return 'https://5f2be0b4ffc88500167b85a0.mockapi.io/suppliers/acme'

    def parse(self, obj: dict) -> Hotel:

        return Hotel(
            id=obj['Id'],
            destination_id=obj['DestinationId'],
            name=obj['Name'],
            description=obj["Description"],
            location=Location(
                lat=obj["Latitude"],
                lng=obj["Longitude"],
                address=obj["Address"],
                city=obj["City"],
                country=obj["Country"],
            ),
            amenities=Amenities(
                general=obj["Facilities"],
                room=[],
            ),
            images=Images(
                rooms=[],
                site=[],
                amenities=[],
            ),
            booking_conditions=[],
        )
