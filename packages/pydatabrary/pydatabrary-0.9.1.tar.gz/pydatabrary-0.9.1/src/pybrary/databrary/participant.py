from .record import Record
from .types.category import Category
from .types.gender import Gender
from .types.ethnicity import Ethnicity
from .types.race import Race


class Participant(Record):
    PARTICIPANT_METRICS = {
        "1": "ID",
        "2": "info",
        "3": "description",
        "4": "birthdate",
        "5": "gender",
        "6": "race",
        "7": "ethnicity",
        "8": "gestational age",
        "9": "pregnancy term",
        "10": "birth weight",
        "11": "disability",
        "12": "language",
        "13": "country",
        "14": "state",
        "15": "setting"
    }

    def __init__(
            self,
            record_key,
            record_id,
            participant_id=None,
            race=Race.UNKNOWN_OR_NOT_REPORTED,
            ethnicity=None,
            gender=None,
            birthdate=None,
            disability=None,
            language=None,
            gestational_age=None,
            birth_weight=None,
            container=None,
    ):
        super().__init__(record_key, record_id, Category.PARTICIPANT, container)

        if ethnicity and not isinstance(ethnicity, Ethnicity):
            raise Exception('ethnicity arg for record {} must be an instance of Ethnicity enum'
                            .format(record_key))

        if gender and not isinstance(gender, Gender):
            raise Exception('gender arg for record {} must be an instance of Gender enum'
                            .format(record_key))

        self.__participant_id = participant_id
        self.__race = race
        self.__ethnicity = ethnicity
        self.__gender = gender
        self.__birthdate = birthdate
        self.__disability = disability
        self.__language = language
        self.__gestational_age = gestational_age
        self.__birth_weight = birth_weight

    @staticmethod
    def from_dict(participant_dict):
        record_id = participant_dict.get('key')
        participant_id = participant_dict.get('ID')
        race = Race.get_name(participant_dict.get('race'))
        ethnicity = Ethnicity.get_name(participant_dict.get('ethnicity'))
        gender = Gender.get_name(participant_dict.get('gender'))
        birthdate = participant_dict.get('birthdate')
        disability = participant_dict.get('disability')
        language = participant_dict.get('language')
        gestational_age = participant_dict.get('gestational_age')
        birth_weight = participant_dict.get('birth_weight')

        return Participant(
            record_key=record_id,
            record_id=record_id,
            participant_id=participant_id,
            race=race,
            ethnicity=ethnicity,
            gender=gender,
            birthdate=birthdate,
            disability=disability,
            language=language,
            gestational_age=gestational_age,
            birth_weight=birth_weight
        )

    @staticmethod
    def from_databrary(participant_dict):
        # TODO: Get measures from the hash map
        record_id = participant_dict.get('id')
        measures = participant_dict.get('measures')

        if not measures:
            return Participant(record_key=record_id, record_id=record_id)

        race = Race.get_name(measures.get('6'))
        participant_id = int(measures.get('1'))
        ethnicity = Ethnicity.get_name(measures.get('7'))
        gender = Gender.get_name(measures.get('5'))
        birthdate = measures.get('4')
        disability = measures.get('11')
        language = measures.get('12')
        gestational_age = measures.get('8')
        birth_weight = measures.get('10')

        return Participant(
            record_key=record_id,
            record_id=record_id,
            participant_id=participant_id,
            race=race,
            ethnicity=ethnicity,
            gender=gender,
            birthdate=birthdate,
            disability=disability,
            language=language,
            gestational_age=gestational_age,
            birth_weight=birth_weight
        )

    def get_template(self):
        return {
            "key": "{}".format(self.get_key()),
            "ID":  "{}".format(self.get_participant_id() if self.get_participant_id() is not None else self.get_key()),
            "category": self.get_category().value,
            "birthdate": "YYYY-MM-DD",
            "language": "",
            "disability": "",
            "gender": "",
            "race": "",
            "ethnicity": ""
        }

    def to_dict(self):
        result = {
            "key": "{}".format(self.get_key()),
            "ID": "{}".format(self.get_participant_id() if self.get_participant_id() is not None else self.get_id()),
            "category": self.get_category().value,
        }

        if self.get_birthdate() is not None:
            result['birthdate'] = self.get_birthdate()
        if self.get_language() is not None:
            result['language'] = self.get_language()
        if self.get_disability() is not None:
            result['disability'] = self.get_disability()
        if self.get_gender() is not None:
            result['gender'] = self.get_gender().value
        if self.get_race() is not None:
            result['race'] = self.get_race().value
        if self.get_ethnicity() is not None:
            result['ethnicity'] = self.get_ethnicity().value

        return result

    def get_race(self):
        return self.__race

    def get_ethnicity(self):
        return self.__ethnicity

    def get_gender(self):
        return self.__gender

    def get_birthdate(self):
        return self.__birthdate

    def get_disability(self):
        return self.__disability

    def get_language(self):
        return self.__language

    def get_participant_id(self):
        return self.__participant_id

    def get_gestational_age(self):
        return self.__gestational_age

    def get_birth_weight(self):
        return self.__birth_weight

    def __eq__(self, other):
        return super().__eq__(other) or self.__participant_id == other.get_participant_id()
