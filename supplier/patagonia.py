from .base import BaseSupplier

from data_models import Location, Hotel, Amenities, Images, Image


class Patagonia(BaseSupplier):

    def endpoint(self):
        return 'https://5f2be0b4ffc88500167b85a0.mockapi.io/suppliers/patagonia'

    def parse(self, obj: dict) -> Hotel:
        return Hotel(
            id=obj['id'],
            destination_id=obj['destination'],
            name=obj['name'],
            description=obj["info"],
            location=Location(
                lat=obj["lat"],
                lng=obj["lng"],
                address=obj["address"],
                city='',
                country='',
            ),
            amenities=Amenities(
                general=obj["amenities"],
                room=[],
            ),
            images=Images(
                rooms=[
                    Image(
                        link=entity["url"],
                        description=entity["description"],
                    ) for entity in obj["images"]["rooms"]
                ],
                site=[],
                amenities=[
                    Image(
                        link=entity["url"],
                        description=entity["description"],
                    ) for entity in obj["images"]["amenities"]
                ],
            ),
            booking_conditions=[],
        )
