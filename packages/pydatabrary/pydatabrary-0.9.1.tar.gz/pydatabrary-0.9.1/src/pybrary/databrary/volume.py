import warnings
import json

from jsonschema import validate, ValidationError

from .container import Container
from .. import constants


class Volume:
    """
    A volume is a set is a set of containers(aka Session), assets and record, A container might point to
    assets and records attached to it.
    The volume class is in charge to fetch the correct asset and record from assets and records list respectively
    and generate an ingest dictionary to be processed by the Curation class
    """
    def __init__(self, volume_name: str, containers=None):
        """
        Create and instance of a Databrary volume
        :param volume_name: Volume's name | Required
        :param containers: A hashmap of container <Container Id, container obj>
        """
        if volume_name is None or len(volume_name) < 1:
            raise AttributeError('You must provide a valid volume name.')

        self.__name = volume_name
        self.__containers = containers

    @staticmethod
    def from_dict(volume_name, containers_map):
        containers = dict()
        for key, container_dict in containers_map.items():
            containers[key] = Container.from_dict(container_dict)

        return Volume(volume_name, containers)

    @staticmethod
    def from_databrary(volume_dict):
        """
        Parse Volume dictionary and populate containers, assets and records (if Any)
        The method will link assets and records to the appropriate container as well
        :param volume_dict: Volume's JSON file
        :return:
        """
        containers = dict()

        # Databrary volume have records in a separate list
        # the record id is referenced in the container records list
        # We need to fetch records before creating our list of containers
        records = dict()
        for record_dict in volume_dict.get('records'):
            record_id = record_dict.get('id')

            if record_id in records:
                raise Exception('Duplicate Record id {}'.format(record_id))

            if record_id is not None:
                records[record_id] = record_dict

        for container_dict in volume_dict.get('containers'):
            container_records = []

            for container_record in container_dict.get('records'):
                record_id = container_record.get('id')
                record_dict = records.get(record_id)
                if record_dict is None:
                    warnings.warn("Cannot find record {} id in the volume's records list".format(record_id))
                else:
                    container_records.append(record_dict)

            container_dict['records'] = container_records
            try:
                container = Container.from_databrary(container_dict)
                containers[container.get_id()] = container
            except Exception as e:
                warnings.warn("Volume {} Error: {}".format(volume_dict.get('name'), e))

        return Volume(
            volume_name=volume_dict.get('name'),
            containers=containers
        )

    def get_containers(self) -> {int, Container}:
        return self.__containers

    def get_container(self, container_id: int) -> Container:
        return self.__containers.get(container_id)

    def remove_participant(self, participant_id: str):
        container = self.get_container_of_participant(participant_id)
        container.remove_participant(participant_id)

    def remove_container(self, container_id: int):
        self.__containers.pop(container_id, None)

    def to_dict(self):
        result = {
            "name": self.get_name(),
        }

        container_list = []
        for container in self.__containers.values():
            container_dict = container.to_dict()
            container_list.append(container_dict)

        result['containers'] = container_list
        # Volume.validate(result)

        return result

    def to_json(self, indent=4):
        return json.dumps(self.to_dict(), indent=indent)

    def get_container_of_record(self, record_id: int):
        for container in self.__containers.values():
            if record_id in container.get_records():
                return container

        return None

    def get_container_of_participant(self, participant_id: str):
        for container in self.__containers.values():
            if container.get_participant(participant_id) is not None:
                return container

        return None

    def get_container_of_asset(self, asset_id: int):
        for container in self.__containers.values():
            if asset_id in container.get_assets():
                return container

        return None

    def get_asset(self, asset_id: int):
        for container in self.__containers.values():
            asset = container.get_assets().get(asset_id)
            if asset is not None:
                return asset

        return None

    def get_record(self, record_id: int):
        for container in self.__containers.values():
            record = container.get_records().get(record_id)
            if record is not None:
                return record

        return None

    def get_name(self) -> str:
        return self.__name

    def get_assets(self):
        assets = dict()
        for container in self.__containers.values():
            for asset in container.get_assets().values():
                if asset.get_id() in assets:
                    raise Exception("Found duplicate asset id {} in volume".format(asset.get_id()))

                assets[asset.get_id()] = asset

        return assets

    def get_records(self):
        records = dict()
        for container in self.__containers.values():
            for record in container.get_records().values():
                if record.get_id() in records:
                    raise Exception("Found duplicate record id {} in volume".format(record.get_id()))

                records[record.get_id()] = record

        return records

    @staticmethod
    def validate(volume_data, schema_file=constants.VOLUME_SCHEMA_FILE):
        with open(schema_file) as f:
            schema = json.loads(f.read())
        try:
            validate(volume_data, schema)
        except ValidationError as e:
            raise Exception('Did not pass validation against volume.json schema - Errors: {}'.format(e))
