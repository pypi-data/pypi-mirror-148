from .types.category import Category

class Record:
    def __init__(
            self,
            record_key,
            record_id,
            category,
            name=None,
            container=None
    ):
        if record_key is None or record_id is None:
            raise Exception('A valid id and key are required for a Record')

        if category is None:
            raise Exception('A category is required for a Record')

        if not isinstance(category, Category):
            raise Exception('category arg for record {} must be an instance of Category enum'
                            .format(record_key))

        self.__key = int(record_key)
        self.__id = int(record_id)
        self.__category = category
        self.__name = "{} {}".format(category.value, record_key) if name is None else name
        self.__container = container

    def get_container(self):
        return self.__container

    def set_container(self, container):
        self.__container = container

    def get_id(self):
        return self.__id

    def get_key(self):
        return self.__key

    def get_name(self):
        return self.__name

    def get_category(self):
        return self.__category

    def __eq__(self, other):
        return self.get_id() == other.get_id()
