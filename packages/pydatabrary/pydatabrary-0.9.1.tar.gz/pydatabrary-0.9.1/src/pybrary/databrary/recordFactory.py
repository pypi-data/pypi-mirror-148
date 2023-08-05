from .types.category import Category
from ..utils import utils

from .participant import Participant
from .pilot import Pilot
from .group import Group
from .exclusion import Exclusion
from .context import Context
from .condition import Condition
from .task import Task


class RecordFactory:
    @staticmethod
    def from_dict(record_dict):
        category = Category.get_name(record_dict.get('category'))
        if category is None:
            raise Exception('A category key is required in the record dictionary')

        record = RecordFactory.get_record_class(category.value)
        return record.from_dict(record_dict)

    @staticmethod
    def from_databrary(record_dict):
        category = record_dict.get('category')
        if not isinstance(category, int):
            raise Exception("Databrary's record categories must be numeric")

        category = utils.get_category_from_category_id(category)

        if not Category.has_value(category):
            raise Exception('Cannot find category {}'.format(category))

        record = RecordFactory.get_record_class(category)
        return record.from_databrary(record_dict)

    @staticmethod
    def get_record_class(category: str):
        if category == "participant":
            return Participant
        elif category == "group":
            return Group
        elif category == "pilot":
            return Pilot
        elif category == "exclusion":
            return Exclusion
        elif category == "context":
            return Context
        elif category == "task":
            return Task
        elif category == "condition":
            return Condition
