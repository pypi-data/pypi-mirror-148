from .record import Record
from .types.category import Category


class Task(Record):
    TASK_METRICS = {
        "29": "name",
        "30": "description",
        "31": "info"
    }

    def __init__(self, record_key, record_id, name=None, info=None, description=None, container=None):
        super().__init__(record_key, record_id, Category.TASK, name=name, container=container)
        self.__info = info
        self.__description = description

    @staticmethod
    def from_dict(task_dict):
        record_id = task_dict.get('key')
        name = task_dict.get('name')
        info = task_dict.get('info')
        description = task_dict.get('description')

        return Task(record_key=record_id, record_id=record_id, name=name, info=info, description=description)

    @staticmethod
    def from_databrary(task_dict):
        record_id = task_dict.get('id')
        measures = task_dict.get('measures')

        if not measures:
            return Task(record_key=record_id, record_id=record_id)

        name = measures.get('29')
        info = measures.get('31')
        description = measures.get('30')

        return Task(
            record_key=record_id,
            record_id=record_id,
            name=name,
            info=info,
            description=description
        )

    def get_template(self):
        return {
            "key": '{}'.format(self.get_key()),
            "name": self.get_name(),
            "category": self.get_category().value,
            "info": "",
            "description": ""
        }

    def to_dict(self):
        result = {
            "key": '{}'.format(self.get_key()),
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
