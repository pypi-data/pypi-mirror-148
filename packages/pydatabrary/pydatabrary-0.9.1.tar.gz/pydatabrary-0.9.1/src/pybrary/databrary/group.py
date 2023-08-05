from .record import Record
from .types.category import Category


class Group(Record):
    GROUP_METRICS = {
        "26": "name",
        "27": "description",
        "28": "info"
    }

    def __init__(self, record_key, record_id, name=None, description=None, info=None, container=None):
        super().__init__(record_key, record_id, Category.GROUP, name=name, container=container)
        self.__description = description
        self.__info = info

    @staticmethod
    def from_dict(group_dict):
        record_id = group_dict.get('key')
        name = group_dict.get('name')
        info = group_dict.get('info')
        description = group_dict.get('description')

        return Group(
            record_key=record_id,
            record_id=record_id,
            name=name,
            description=description,
            info=info
        )

    @staticmethod
    def from_databrary(group_dict):
        record_id = group_dict.get('id')
        measures = group_dict.get('measures')

        if not measures:
            return Group(record_key=record_id, record_id=record_id)

        name = measures.get('26')
        info = measures.get('28')
        description = measures.get('27')

        return Group(
            record_key=record_id,
            record_id=record_id,
            name=name,
            description=description,
            info=info,
        )

    def get_template(self):
        return {
            "key": "{}".format(self.get_key()),
            "name": self.get_name(),
            "category": self.get_category().value,
            "info": "",
            "description": ""
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

    def get_info(self):
        return self.__info

    def get_description(self):
        return self.__description
