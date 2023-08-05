from enum import Enum


class Gender(Enum):
    FEMALE = 'Female'
    MALE = 'Male'

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_

    @classmethod
    def get_name(cls, value):
        if not cls.has_value(value):
            return None

        return cls._value2member_map_[value]
