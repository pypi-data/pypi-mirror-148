from enum import Enum


class Reason(Enum):
    DID_NOT_MEET_INCLUSION_CRITERIA = 'Did not meet inclusion criteria'
    PROCEDURAL_EXPERIMENTER_ERROR = 'Procedural/experimenter error'
    WITHDREW_FUSSY_TIRED = 'Withdrew/fussy/tired'
    OUTLIER = 'Outlier'

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_

    @classmethod
    def get_name(cls, value):
        if not cls.has_value(value):
            return None

        return cls._value2member_map_[value]
