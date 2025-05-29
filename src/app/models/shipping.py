from enum import Enum


class Shipping(str, Enum):
    truck = "truck"
    ship = "ship"
    plane = "plane"
