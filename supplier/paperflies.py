from .base import BaseSupplier

from data_models import Location, Hotel, Amenities, Images, Image


class Paperflies(BaseSupplier):

    def endpoint(self) -> str:
        return 'https://5f2be0b4ffc88500167b85a0.mockapi.io/suppliers/paperflies'

    def parse(self, obj: dict) -> Hotel:

        return Hotel(
            id=obj['hotel_id'],
            destination_id=obj['destination_id'],
            name=obj['hotel_name'],
            description=obj["details"],
            location=Location(
                lat=float('nan'),
                lng=float('nan'),
                address=obj["location"]["address"],
                city='',
                country=obj["location"]["country"],
            ),
            amenities=Amenities(
                general=obj['amenities']['general'],
                room=obj['amenities']['room'],
            ),
            images=Images(
                rooms=[
                    Image(
                        link=entity["link"],
                        description=entity["caption"],
                    ) for entity in obj["images"]["rooms"]
                ],
                site=[
                    Image(
                        link=entity["link"],
                        description=entity["caption"],
                    ) for entity in obj["images"]["site"]
                ],
                amenities=[],
            ),
            booking_conditions=obj["booking_conditions"],
        )
