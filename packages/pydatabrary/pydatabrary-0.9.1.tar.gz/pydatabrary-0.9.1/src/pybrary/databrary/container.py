import warnings

from .. import constants

from .recordFactory import RecordFactory
from .record import Record
from .participant import Participant
from .asset import Asset
from .types.release import Release


class Container:
    def __init__(
            self,
            container_id,
            container_key,
            name=None,
            date='',
            top=False,
            release=Release.PRIVATE,
            assets=None,
            records=None,
            volume=None
    ):
        """
        :param container_id:
        :param container_key: 
        :param name: 
        :param date: 
        :param top: 
        :param release:
        :param assets: A hashmap of asset objects <Asset ID, Asset Object>
        :param records: A hashmap of record object<Record ID, Record Object>
        """
        if container_id is None:
            raise Exception('A valid id is required for containers')

        self.__id = container_id
        self.__key = container_key
        self.__top = top
        self.__name = name
        self.__release = release
        self.__date = date if len(date) > 0 else None
        self.__volume = volume
        self.__init_assets(assets)
        self.__init_records(records)

    def __init_records(self, records):
        self.__records = records if records is not None else {}
        for record in self.__records.values():
            record.set_container(self)

    def __init_assets(self, assets):
        self.__assets = assets if assets is not None else {}
        for asset in self.__assets.values():
            asset.set_container(self)

    def set_volume(self, volume):
        self.__volume = volume

    def get_volume(self):
        return self.__volume

    def get_key(self) -> int:
        return self.__key

    def get_id(self) -> int:
        return self.__id

    def get_assets(self) -> {int, Asset}:
        return self.__assets

    def set_assets(self, assets: {int, Asset}):
        """
        Set a hashmap of assets <Asset id, Asset Obj> to this container
        :param assets:
        :return:
        """
        self.__init_assets(assets)

    def get_records(self) -> {int, Record}:
        return self.__records

    def set_records(self, records: {int, Record}):
        self.__init_records(records)

    def add_asset(self, asset: Asset):
        """
        Add an Asset Object to the asset hashmap
        :param asset:
        :return:
        """
        asset_id = asset.get_id()
        if self.asset_id_exists(asset_id):
            raise Exception('Asset id {} already exists in container {}'.format(asset.get_id(), self.__id))

        self.__assets[asset_id] = asset
        asset.set_container(self)

    def add_record(self, record: Record):
        """
        Add a Record object to the records hashmap
        :param record:
        :return:
        """
        record_id = record.get_id()
        if self.record_id_exists(record_id):
            raise Exception('Record id {} already exists in container {}'
                            .format(record.get_id(), self.__id))

        if isinstance(record, Participant):
            if self.participant_id_exists(record.get_participant_id()):
                raise Exception('Participant id {} already exists in container {}'
                                .format(record.get_participant_id(), self.__id))

        self.__records[record_id] = record
        record.set_container(self)

    def record_id_exists(self, record_id: int):
        if record_id in self.__records:
            return True

        return False

    def participant_id_exists(self, participant_id: int):
        if self.get_participant(participant_id) is not None:
            return True

        return False

    def asset_id_exists(self, asset_id: int):
        if asset_id in self.__assets:
            return True

        return False

    def get_name(self) -> str:
        return self.__name

    def set_name(self, value: str):
        if value is None:
            raise Exception('You must provide a valid name for container {}'.format(self.__id))

        self.__name = value

    def get_asset(self, asset_id: int) -> Asset:
        return self.__assets.get(asset_id)

    def get_record(self, record_id: int) -> Record:
        return self.__records.get(record_id)

    def get_top(self) -> bool:
        return self.__top

    def set_release(self, release: Release):
        self.__release = release

    def get_release(self) -> Release:
        return self.__release

    def get_date(self) -> str:
        return self.__date

    def get_participants(self) -> {int, Participant}:
        participant_records = dict(
            filter(lambda elem: isinstance(elem[1], Participant),
                   self.__records.items()))
        participant_records = {participant.get_participant_id(): participant
                               for record_id, participant in participant_records.items()}
        return participant_records

    def get_participant(self, participant_id: str) -> Participant:
        return self.get_participants().get(participant_id)

    def remove_participant(self, participant_id: str):
        participant = self.get_participant(participant_id)
        if participant is not None:
            self.__records.pop(participant.get_id(), None)

    @staticmethod
    def from_dict(container_dict):
        container_id = container_dict.get('key')
        name = container_dict.get('name')
        assets = container_dict.get('assets')
        assets = {asset_dict.get('id'): Asset.from_dict(asset_dict) for asset_dict in assets}
        records = container_dict.get('records')
        records = {record_dict.get('key'): RecordFactory.from_dict(record_dict) for record_dict in records}
        release = Release[container_dict.get('release')]
        date = container_dict.get('date')
        top = container_dict.get('top')

        return Container(
            container_key=container_id,
            container_id=container_id,
            name=name,
            release=release,
            top=top,
            date=date,
            assets=assets,
            records=records
        )

    @staticmethod
    def from_databrary(container_dict):
        container_id = container_dict.get('id')
        date = container_dict.get('date')
        top = container_dict.get('top') is not None
        name = container_dict.get('name')

        records = dict()
        for record_dict in container_dict.get('records'):
            record_id = record_dict.get('id')
            try:
                records[record_id] = RecordFactory.from_databrary(record_dict)
            except Exception as e:
                warnings.warn('Container {} Error: {}'.format(container_id, e))

        assets = dict()
        for asset_dict in container_dict.get('assets'):
            asset_id = asset_dict.get('id')
            try:
                path_prefix = "{}/{}".format(constants.DEFAULT_SERVER_PREFIX, container_id)
                assets[asset_id] = Asset.from_databrary(asset_dict, path_prefix)
            except Exception as e:
                warnings.warn('Container {} Error: {}'.format(container_id, e))

        return Container(
            container_key=container_id,
            container_id=container_id,
            name=name,
            top=top,
            date=date,
            assets=assets,
            records=records
        )

    def get_template(self):
        return {
            "key": "{}".format(self.get_key()),
            "top": self.get_top(),
            "release": self.get_release().value,
            "name": "",
            "date": "",
            "assets": [],
            "records": []
        }

    def to_dict(self):
        result = {
            "key": "{}".format(self.get_key()),
            "top": self.get_top(),
            "release": self.get_release().value,
        }

        if self.get_name() is not None:
            result['name'] = self.get_name()

        if self.get_date() is not None:
            result['date'] = self.get_date()

        result['assets'] = list(map(lambda asset: asset.to_dict(), list(self.get_assets().values())))
        result['records'] = list(map(lambda record: record.to_dict(), list(self.get_records().values())))

        return result

    def __eq__(self, other):
        return self.__id == other.get_id()
