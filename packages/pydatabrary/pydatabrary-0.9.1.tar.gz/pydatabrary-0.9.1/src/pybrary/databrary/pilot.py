from .record import Record
from .types.category import Category


class Pilot(Record):
    PILOT_METRICS = {
        "16": "pilot",
        "17": "name",
        "18": "description"
    }

    def __init__(self, record_key, record_id, name=None, pilot=None, description=None, container=None):
        super().__init__(record_key, record_id, Category.PILOT, name=name, container=container)
        self.__pilot = pilot
        self.__description = description

    @staticmethod
    def from_dict(pilot_dict):
        record_id = pilot_dict.get('key')
        name = pilot_dict.get('name')
        pilot = pilot_dict.get('pilot')
        description = pilot_dict.get('description')
        return Pilot(record_key=record_id, record_id=record_id, name=name, pilot=pilot, description=description)

    @staticmethod
    def from_databrary(pilot_dict):
        record_id = pilot_dict.get('id')
        measures = pilot_dict.get('measures')

        if not measures:
            return Pilot(record_key=record_id, record_id=record_id)

        name = measures.get('17')
        pilot = measures.get('16')
        description = measures.get('18')
        return Pilot(record_key=record_id, record_id=record_id, name=name, pilot=pilot, description=description)

    def get_template(self):
        return {
            "key": "{}".format(self.get_key()),
            "name": self.get_name(),
            "category": self.get_category().value,
            "pilot": "",
            "description": ""
        }

    def to_dict(self):
        result = {
            "key": "{}".format(self.get_key()),
            "name": self.get_name(),
            "category": self.get_category().value,
        }

        if self.get_pilot() is not None:
            result["pilot"] = self.get_pilot()

        if self.get_description() is not None:
            result["description"] = self.get_description()

        return result

    def get_pilot(self):
        return self.__pilot

    def get_description(self):
        return self.__description
