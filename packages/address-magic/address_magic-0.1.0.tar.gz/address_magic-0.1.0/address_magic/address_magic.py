#!/usr/bin/env python3
from enum import Enum
from postal.parser import parse_address
from enum import Enum

class PostalLabel(Enum):
    """Enumerations for Parser labels"""
    HOUSE = "house"
    CATEGORY = "category"
    NEAR = "near"
    HOUSE_NUMBER = "house_number"
    ROAD = "road"
    UNIT = "unit"
    LEVEL = "level"
    STAIRCASE = "staircase"
    ENTRANCE = "entrance"
    PO_BOX = "po_box"
    POSTCODE = "postcode"
    SUBURB = "suburb"
    CITY_DISTRICT = "city_distric"
    CITY = "city"
    ISLAND = "island"
    STATE_DISTRICT = "state_district"
    STATE = "state"
    COUNTRY_REGION = "country_region"
    COUNTRY = "country"
    WORLD_REGION = "world_region"


class Address:
    """Adress object"""
    def __init__(self, address):
        self.address = address
        data = parse_address(address)
        self.house = None
        self.category = None
        self.near = None
        self.category = None
        self.near = None
        self.road = None
        self.unit = None
        self.house_number = None
        self.level = None
        self.entrance = None
        self.po_box = None
        self.postcode = None
        self.suburb = None
        self.city_district = None
        self.city = None
        self.island = None
        self.state = None
        self.state_district = None
        self.country_region = None
        self.country = None
        self.world_region = None
        for value, ptype in data:
             if PostalLabel(ptype) == PostalLabel.HOUSE:
                self.house = value
             elif PostalLabel(ptype) == PostalLabel.CATEGORY:
                self.category = value
             elif PostalLabel(ptype) == PostalLabel.NEAR:
                self.near = value
             elif PostalLabel(ptype) == PostalLabel.HOUSE_NUMBER:
                self.house_number = value
             elif PostalLabel(ptype) == PostalLabel.ROAD:
                self.road = value
             elif PostalLabel(ptype) == PostalLabel.UNIT:
                self.unit = value
             elif PostalLabel(ptype) == PostalLabel.ENTRANCE:
                self.entrance = value
             elif PostalLabel(ptype) == PostalLabel.LEVEL:
                self.level = value
             elif PostalLabel(ptype) == PostalLabel.PO_BOX:
                self.po_box = value
             elif PostalLabel(ptype) == PostalLabel.POSTCODE:
                self.postcode = value
             elif PostalLabel(ptype) == PostalLabel.SUBURB:
                self.suburb = value
             elif PostalLabel(ptype) == PostalLabel.CITY_DISTRICT:
                self.city_district = value
             elif PostalLabel(ptype) == PostalLabel.CITY:
                self.city = value
             elif PostalLabel(ptype) == PostalLabel.ISLAND:
                self.island = value
             elif PostalLabel(ptype) == PostalLabel.STATE:
                self.state = value
             elif PostalLabel(ptype) == PostalLabel.STATE_DISTRICT:
                self.state_district = value
             elif PostalLabel(ptype) == PostalLabel.COUNTRY:
                self.country = value
             elif PostalLabel(ptype) == PostalLabel.COUNTRY_REGION:
                self.country_region = value
             elif PostalLabel(ptype) == PostalLabel.WORLD_REGION:
                self.world_region = value
    def validate(self, need_postal=False):
        """Returns True if the address is valid. set `need_postal=True` if you require zip codes"""
        if need_postal == True:
            if self.house_number is not None and self.road is not None and self.city is not None and self.state is not None and self.postcode is not None:
                return True
            else:
                return False
        if self.house_number is not None and self.road is not None and self.city is not None and self.state is not None:
            return True
        else:
            return False
