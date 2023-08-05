from .record import Record
from .types.category import Category
from .types.reason import Reason


class Exclusion(Record):
    EXCLUSION_METRICS = {
        "19": "excluded",
        "20": "name",
        "21": "reason",
        "22": "description"
    }

    def __init__(
            self,
            record_key,
            record_id,
            reason=None,
            excluded=None,
            name=None,
            description=None,
            container=None
    ):
        super().__init__(record_key, record_id, Category.EXCLUSION, name=name, container=container)

        if reason and not isinstance(reason, Reason):
            raise Exception('reason arg for record {} must be an instance of Reason enum'
                            .format(record_key))

        self._reason = reason
        self._excluded = excluded
        self._description = description

    @staticmethod
    def from_dict(exclusion_dict):
        record_id = exclusion_dict.get('key')
        excluded = exclusion_dict.get('excluded')
        name = exclusion_dict.get('name')
        description = exclusion_dict.get('description')
        reason = Reason.get_name(exclusion_dict.get('reason'))

        return Exclusion(
            record_key=record_id,
            record_id=record_id,
            reason=reason,
            excluded=excluded,
            name=name,
            description=description
        )

    @staticmethod
    def from_databrary(exclusion_dict):
        record_id = exclusion_dict.get('id')
        measures = exclusion_dict.get('measures')

        if not measures:
            return Exclusion(record_key=record_id, record_id=record_id)

        excluded = measures.get('19')
        name = measures.get('20')
        description = measures.get('22')
        reason = Reason.get_name(measures['21'])

        return Exclusion(
            record_key=record_id,
            record_id=record_id,
            reason=reason,
            excluded=excluded,
            name=name,
            description=description
        )

    def get_template(self):
        return {
            "key": "{}".format(self.get_key()),
            "name": self.get_name(),
            "category": self.get_category().value,
            "reason": "",
            "excluded": "",
            "description": ""
        }

    def to_dict(self):
        result = {
            "key": "{}".format(self.get_key()),
            "name": self.get_name(),
            "category": self.get_category().value,
        }

        if self.get_reason() is not None:
            result['reason'] = self.get_reason().value

        if self.get_excluded() is not None:
            result["excluded"] = self.get_excluded()

        if self.get_description() is not None:
            result["description"] = self.get_description()

        return result

    def get_reason(self):
        return self._reason

    def get_excluded(self):
        return self._excluded

    def get_description(self):
        return self._description
