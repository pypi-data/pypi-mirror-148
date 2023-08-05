import json
from .record import Record
from .types.category import Category


class Condition(Record):
    CONDITION_METRICS = {
        "23": "name",
        "24": "description",
        "25": "info",
    }

    def __init__(self, record_key, record_id, name=None, info=None, description=None, container=None):
        super().__init__(record_key, record_id, Category.CONDITION, name=name, container=container)
        self.__info = info
        self.__description = description

    @staticmethod
    def from_dict(condition_dict):
        record_id = condition_dict.get('key')
        name = condition_dict.get('name')
        description = condition_dict.get('description')
        info = condition_dict.get('info')

        return Condition(
            record_key=record_id,
            record_id=record_id,
            name=name,
            description=description,
            info=info
        )

    @staticmethod
    def from_databrary(condition_dict):
        record_id = condition_dict.get('id')
        measures = condition_dict.get('measures')

        if not measures:
            return Condition(
                record_key=record_id,
                record_id=record_id
            )

        name = measures.get('23')
        description = measures.get('24')
        info = measures.get('25')

        return Condition(
            record_key=record_id,
            record_id=record_id,
            name=name,
            description=description,
            info=info
        )

    def get_template(self):
        return {
            "key": "{}".format(self.get_key()),
            "name": self.get_name(),
            "category": self.get_category().value,
            "info": None,
            "description": None
        }

    def to_dict(self):
        result = {
            "key": "{}".format(self.get_key()),
            "name": self.get_name(),
            "category": self.get_category().value,
        }

        if self.get_info() is not None:
            result["info"] = self.get_info()

        if self.get_description() is not None:
            result["description"] = self.get_description()

        return result

    def to_json(self):
        return json.dumps(self.to_dict())

    def get_info(self):
        return self.__info

    def get_description(self):
        return self.__description
