from math import isnan

from data_models import Hotel, Amenities, Images, Location
from string_cleaner_builder import StringCleanerBuilder

class HotelsService(object):

    def __init__(self):
        self.hotels: list[Hotel] = []
        self.hotel_ids = set()
        self.destination_ids = set()

        # data cleaners
        self.string_cleaner = (
            StringCleanerBuilder()
            .escape_html(quote=False)
            .normalize_unicode()
            .strip_whitespace()
            .remove_special_characters(allowed_chars=",. -':()/")
            .build()
        )

        self.amenities_cleaner = (
            StringCleanerBuilder()
            .escape_html()
            .normalize_unicode()
            .strip_whitespace()
            .remove_special_characters(allowed_chars=' ')
            .to_camelcase()
            .remove_camelcase()
            .to_lowercase()
            .build()
        )

    def standardize(self, hotels: list[Hotel]) -> list[Hotel]:

        for hotel in hotels:
            hotel.name = self.__standardize_name__(hotel.name)

            hotel.location = self.__standardize_location__(hotel.location)

            hotel.description = self.__standardize_description__(hotel.description)

            hotel.amenities = self.__standarize_amenities__(hotel.amenities)

            hotel.images = self.__standarize_images__(hotel.images)

            hotel.booking_conditions = self.__standardize_booking_conditions__(
                hotel.booking_conditions
            )

        return hotels

    def merge_and_save(self, hotels: list[Hotel]):

        hotels = self.standardize(hotels)

        merged_hotels: dict[tuple[str, str], Hotel] = {}
        for hotel in hotels:
            key = (hotel.id, hotel.destination_id)
            if key not in merged_hotels.keys():
                merged_hotels[key] = hotel
                continue

            existing_hotel = merged_hotels[key]
            merged_hotels[key] = Hotel(
                id=hotel.id,
                destination_id=hotel.destination_id,
                name=self.__merge_name__(existing_hotel.name, hotel.name),
                description=self.__merge_description__(
                    existing_hotel.description, hotel.description
                ),
                location=self.__merge_location__(
                    existing_hotel.location, hotel.location
                ),
                amenities=self.__merge_amendities__(
                    existing_hotel.amenities, hotel.amenities
                ),
                images=self.__merge_images__(existing_hotel.images, hotel.images),
                booking_conditions=self.__merge_booking_conditions__(
                    existing_hotel.booking_conditions, hotel.booking_conditions
                ),
            )

        self.hotels = list(merged_hotels.values())

        self.hotel_ids = set([hotel.id for hotel in hotels])
        self.destination_ids = set([hotel.destination_id for hotel in hotels])

    def find(self, hotel_ids, destination_ids) -> list[Hotel]:
        if hotel_ids == "none" and destination_ids == "none":
            return self.hotels

        hotel_ids = set(hotel_ids.split(",")) if hotel_ids != "none" else self.hotel_ids
        destination_ids = (
            set(destination_ids.split(","))
            if destination_ids != "none"
            else self.destination_ids
        )

        hotel_id_order = {hotel_id: index for index, hotel_id in enumerate(hotel_ids)}

        destination_id_order = {
            destination_id: index
            for index, destination_id in enumerate(destination_ids)
        }

        filtered = sorted(
            (
                hotel
                for hotel in self.hotels
                if hotel.id in hotel_ids
                and str(hotel.destination_id) in destination_ids
            ),
            key=lambda hotel: (
                hotel_id_order.get(hotel.id, float("inf")),
                destination_id_order.get(hotel.destination_id, float("inf")),
            ),
        )

        return filtered

    def __standardize_name__(self, name: str) -> str:
        return self.string_cleaner(name) if name else ""

    def __standardize_location__(self, location: Location) -> Location:
        lat = location.lat if isinstance(location.lat, float) else float("nan")
        lng = location.lng if isinstance(location.lng, float) else float("nan")
        address = location.address.strip() if location.address else ""
        city = location.city.strip() if location.city else ""
        country = location.country.strip() if location.country else ""
        return Location(
            lat=lat,
            lng=lng,
            address=address,
            city=city,
            country=country,
        )

    def __standardize_description__(self, description: str) -> str:
        return self.string_cleaner(description) if description else ""

    def __standarize_amenities__(self, amenities: Amenities) -> Amenities:
        general = amenities.general if isinstance(amenities.general, list) else []
        room = amenities.room if isinstance(amenities.room, list) else []

        general = [self.amenities_cleaner(str(e)) for e in general]
        room = [self.amenities_cleaner(str(e)) for e in room]

        return Amenities(
            general=general,
            room=room,
        )

    def __standarize_images__(self, images: Images) -> Images:
        rooms = images.rooms if isinstance(images.rooms, list) else []
        site = images.site if isinstance(images.site, list) else []
        amenities = images.amenities if isinstance(images.amenities, list) else []
        return Images(
            rooms=rooms,
            site=site,
            amenities=amenities,
        )

    def __standardize_booking_conditions__(
        self, booking_conditions: list[str]
    ) -> list[str]:
        booking_conditions = (
            booking_conditions if isinstance(booking_conditions, list) else []
        )
        return [self.string_cleaner(str(s)) for s in booking_conditions]

    def __merge_name__(self, name1: str, name2: str) -> str:
        return name1 or name2

    def __merge_description__(self, des1: str, des2: str) -> str:
        return des1 or des2

    def __merge_location__(self, location1: Location, location2: Location) -> Location:
        return Location(
            lat=location1.lat if not isnan(location1.lat) else location2.lat,
            lng=location1.lng if not isnan(location1.lng) else location2.lng,
            address=location1.address or location2.address,
            city=location1.city or location2.city,
            country=location1.country or location2.country,
        )

    def __merge_amendities__(self, am1: Amenities, am2: Amenities) -> Amenities:
        merged_general = set(am1.general + am2.general)
        merged_room = set(am1.room + am2.room)

        unique_general = merged_general.difference(merged_room)

        return Amenities(
            general=list(unique_general),
            room=list(merged_room),
        )

    def __merge_images__(self, images1: Images, images2: Images) -> Images:
        return Images(
            rooms=list(
                {img.link: img for img in images1.rooms + images2.rooms}.values()
            ),
            site=list({img.link: img for img in images1.site + images2.site}.values()),
            amenities=list(
                {
                    img.link: img for img in images1.amenities + images2.amenities
                }.values()
            ),
        )

    def __merge_booking_conditions__(
        self, conditions_1: list[str], conditions_2: list[str]
    ) -> list[str]:
        return list(set(conditions_1 + conditions_2))
