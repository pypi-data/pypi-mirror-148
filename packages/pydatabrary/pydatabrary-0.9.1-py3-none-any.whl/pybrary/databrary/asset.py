from .types.release import Release
from ..utils import utils
from .. import constants


class Asset:
    def __init__(
            self,
            file_path,
            asset_id,
            container=None,
            name=None,
            position='auto',
            release=Release.PRIVATE,
            clips=None
    ):
        if asset_id is None:
            raise Exception('Asset id is required')

        if file_path is None:
            raise Exception('You must provide a file path to the asset {}.'.format(asset_id))

        self._file_ext = utils.get_file_extension(file_path)
        if not Asset.is_ext_supported(self._file_ext):
            raise Exception('Asset format {} not supported'.format(self._file_ext))

        if not Asset.is_media(self._file_ext) and clips is not None:
            raise Exception('Cannot add clips for {}. Clips are only supported for media types'.format(self._file_ext))

        self.__clips = clips
        self.__id = asset_id
        self.__file_path = file_path
        self.__name = utils.get_file_name(file_path) if name is None else name
        self.__position = position
        self.__release = release
        self.__container = container

    def get_container(self):
        return self.__container

    def set_container(self, container):
        self.__container = container

    def get_id(self) -> int:
        return self.__id

    def get_name(self) -> str:
        return self.__name

    def set_name(self, value: str):
        self.__name = value

    def get_release(self) -> Release:
        return self.__release

    def set_release(self, release: Release):
        self.__release = release

    @staticmethod
    def from_dict(asset_dict):
        file = asset_dict.get('file')
        asset_id = asset_dict.get('id')
        name = asset_dict.get('name')
        return Asset(asset_id=asset_id, file_path=file, name=name)

    @staticmethod
    def from_databrary(asset_dict, path_prefix=constants.DEFAULT_SERVER_PREFIX):
        """
        Building an Asset Object from Databrary Asset Dict fetched from the API.
        Important: Pybrary cannot know the file name, so it will build the file path
        from the Asset's name, Make sure that your file names and asset
        names are the same
        if not, please contact you Databrary Administrator
        Example: {
          "id": 12094,
          "format": -800,
          "duration": 1925035,
          "segment": [
            0,
            1925035
          ],
          "name": "InfantOHApS#74",
          "permission": 5,
          "size": 659371898
        }
        :param asset_dict:
        :param path_prefix:
        :return:
        """
        asset_id = asset_dict.get('id')

        file_name = utils.get_file_name_no_extension(asset_dict.get('name'))
        file_ext = utils.get_databrary_ext_from_format(asset_dict.get('format'))

        if not file_name:
            raise Exception("Asset {} does not contain a file name".format(asset_id))

        file_name = file_name

        if file_ext is None:
            raise Exception('Format {} of Asset id {} is not supported by Databrary'
                            .format(asset_dict.get('format'), asset_id))

        file_name_ext = "{}.{}".format(file_name, file_ext)

        file_path = "{}/{}".format(path_prefix, file_name_ext)
        return Asset(file_path=file_path, asset_id=asset_id, name=file_name)

    def get_template(self):
        return {
            "id": self.get_id(),
            "release": self.get_release().value,
            "position": self.__position,
            "name": self.get_name(),
            "file": self.__file_path,
            "clips": []
        }

    def to_dict(self):
        result = {
            "id": self.get_id(),
            "release": self.get_release().value,
            "position": self.__position,
            "name": self.get_name(),
            "file": self.__file_path
        }

        if self.__clips is not None:
            result['clip'] = self.__clips

        return result

    @staticmethod
    def is_media(file_ext: str) -> bool:
        if file_ext in constants.VIDEO_EXTENSIONS \
                or file_ext in constants.AUDIO_EXTENSIONS:
            return True

        return False

    @staticmethod
    def is_ext_supported(file_ext: str) -> bool:
        if file_ext in constants.SUPPORTED_FORMATS.values():
            return True

        return False

    def __eq__(self, other):
        return self.__id == other.get_id()
