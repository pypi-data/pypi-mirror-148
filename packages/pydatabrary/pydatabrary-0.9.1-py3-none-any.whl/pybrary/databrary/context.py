from .record import Record

from .types.category import Category
from .types.setting import Setting


class Context(Record):
    CONTEXT_METRICS = {
        "32": "name",
        "33": "setting",
        "34": "language",
        "35": "country",
        "36": "state"
    }

    # TODO: Add State and country types
    def __init__(
            self,
            record_key,
            record_id,
            name=None,
            language=None,
            setting=None,
            country=None,
            state=None,
            container=None
    ):
        super().__init__(record_key, record_id, Category.CONTEXT, name=name, container=container)

        if setting and not isinstance(setting, Setting):
            raise Exception('setting arg for record {} must be an instance of Setting enum'
                            .format(record_key))

        self._setting = setting
        self._country = country
        self._state = state
        self._language = language

    @staticmethod
    def from_dict(context_dict):
        record_id = context_dict.get('key')
        setting = Setting.get_name(context_dict.get('setting'))
        country = context_dict.get('country')
        state = context_dict.get('state')
        name = context_dict.get('name')
        language = context_dict.get('language')

        return Context(
            record_key=record_id,
            record_id=record_id,
            name=name,
            language=language,
            setting=setting,
            country=country,
            state=state
        )

    @staticmethod
    def from_databrary(context_dict):
        rexord_id = context_dict.get('id')
        measures = context_dict.get('measures')

        if not measures:
            return Context(record_key=rexord_id, record_id=rexord_id)

        setting = Setting.get_name(measures.get('33'))
        country = measures.get('35')
        state = measures.get('36')
        name = measures.get('32')
        language = measures.get('34')

        return Context(
            record_key=rexord_id,
            record_id=rexord_id,
            name=name,
            language=language,
            setting=setting,
            country=country,
            state=state
        )

    def get_template(self):
        return {
            "key": "{}".format(self.get_key()),
            "name": self.get_name(),
            "category": self.get_category().value,
            "language": None,
            "setting": None,
            "state": None,
            "country": None
        }

    def to_dict(self):
        result = {
            "key": "{}".format(self.get_key()),
            "name": self.get_name(),
            "category": self.get_category().value,
        }

        if self.get_language() is not None:
            result["language"] = self.get_language()

        if self.get_setting() is not None:
            result["setting"] = self.get_setting().value

        if self.get_state() is not None:
            result["state"] = self.get_state()

        if self.get_country() is not None:
            result["country"] = self.get_country()

        return result

    def get_language(self):
        return self._language

    def get_setting(self):
        return self._setting

    def get_state(self):
        return self._state

    def get_country(self):
        return self._country
