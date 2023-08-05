import os
import warnings

from ..databrary.recordFactory import RecordFactory
from ..databrary.asset import Asset
from ..databrary.volume import Volume

from ..utils import utils
from ..databrary.container import Container
from ..databrary.types.category import Category
from ..api.pybrary import Pybrary
from .. import constants


class Curation:
    @staticmethod
    def from_databrary(volume_id, username=None, password=None, superuser=False):
        pb = Pybrary.get_instance(username, password, superuser)
        volume_data = pb.get_volume_info(volume_id)

        return Volume.from_databrary(volume_data)

    @staticmethod
    def from_files(volume_name, containers_file, assets_file=None, records_file=None):
        if volume_name is None:
            raise Exception('You must provide a valid volume name.')

        if containers_file is None:
            raise Exception('Containers file is required')

        containers = Curation.from_csv(containers_file)

        assets = dict()
        if assets_file is None:
            warnings.warn('Assets found in the containers file will be ignored. PLease provide an assets file')
        else:
            assets = Curation.from_csv(assets_file, 'id')

        records = dict()
        if records_file is None:
            warnings.warn('Records found in the containers file will be ignored. PLease provide a records file')
        else:
            records = Curation.from_csv(records_file)

        for key, container_dict in containers.items():
            asset_ids = container_dict.get('assets')
            assets_map = dict()
            for idx, asset_id in enumerate(asset_ids):
                if asset_id not in assets:
                    warnings.warn("Asset id {} not find in asset file, it will be ignored".format(asset_id))
                    continue

                assets_map[asset_id] = assets.get(asset_id)

            container_dict['assets'] = list(assets_map.values())

            record_ids = container_dict.get('records')
            records_map = dict()
            for idx, record_id in enumerate(record_ids):
                if record_id not in records:
                    warnings.warn("record id {} not find in record file, it will be ignored".format(record_id))
                    continue

                records_map[record_id] = records.get(record_id)

            container_dict['records'] = list(records_map.values())
            containers[key] = Container.from_dict(container_dict)

        return Volume(volume_name, containers)

    @staticmethod
    def to_files(volume, containers_output, assets_output, records_output):
        assets = volume.get_assets()
        Curation.map_to_csv(assets, assets_output)

        records = volume.get_records()
        Curation.map_to_csv(records, records_output)

        containers = volume.get_containers()
        container_list = []
        for container in containers.values():
            container_dict = container.to_dict()
            container_dict["assets"] = list(map(lambda asset: asset.get('id'), container_dict.get('assets')))
            container_dict["records"] = list(map(lambda record: record.get('key'), container_dict.get('records')))
            container_list.append(container_dict)

        Curation.list_to_csv(container_list, containers_output)

    @staticmethod
    def to_json(volume, output):
        if output is None:
            raise Exception('Please provide an output path')

        if utils.get_file_extension(output) != 'json':
            raise Exception('Ingest files must be in JSON format, ingest file cannot be saved in {}'
                            .format(output))

        utils.dump_into_json(volume.to_dict(), output)

    @staticmethod
    def generate_assets(folder, output=None):
        """
        Find all supported files in a folder (recursively) adds clips for video files.
        return the following structure
            [
                {
                    "key": 1
                    "release": null,
                    "position": "auto",
                    "name": "FILE_NAME,
                    "file": "FILE_PATH_IN_DATABRARY_STAGING_FOLDER"
                }
            ]
        :param output: dump assets list into a csv file
        :param folder: Folder path where to lookup for assets
        :return: a List of dict with supported assets found in folder
        """
        if not os.path.isdir(folder):
            raise Exception('{} is not a directory'.format(folder))

        print('Parsing {}'.format(os.path.abspath(folder)))

        assets = dict()
        idx = 0
        for root, dirs, files in os.walk(folder):
            for file in files:
                try:
                    assets[idx] = Asset(file_path=os.path.join(root, file), asset_id=idx)
                    idx += 1
                except Exception as e:
                    warnings.warn("Error while generating asset list: {} ".format(e))

        if output is not None:
            Curation.map_to_csv(assets, output, template=True)
            print('Assets printed in {}'.format(os.path.abspath(output)))

        return assets

    @staticmethod
    def generate_records(categories=None, output=None):
        records = dict()

        idx = 0
        for category, value in categories.items():
            if not Category.has_value(category):
                raise Exception('Category {} is not valid, it will be ignored'.format(category))

            if int(value) < 1:
                raise Exception('The value {} for {} is not valid, it must be > 0'.format(value, category))

            for i in range(value):
                records[idx] = RecordFactory.from_dict({
                        "category": category,
                        "key": idx
                    })
                idx = idx + 1

        if output is not None:
            Curation.map_to_csv(records, output, template=True)
            print('Records printed in {}'.format(os.path.abspath(output)))

        return records

    @staticmethod
    def generate_containers(value=1, output=None):
        if int(value) < 1:
            raise Exception('The value {} is not valid, it must be > 0'.format(value))

        containers = {i: Container(container_key=i, container_id=i) for i in range(value)}

        if output is not None:
            Curation.map_to_csv(containers, output, template=True)
            print('Containers printed in {}'.format(os.path.abspath(output)))

        return containers

    @staticmethod
    def map_to_csv(data_map, output, template=False):
        data_list = [data.get_template() if template else data.to_dict() for data in data_map.values()]
        Curation.list_to_csv(data_list, output)

    @staticmethod
    def list_to_csv(data_list, output):
        utils.dump_into_csv(data_list, output)

    @staticmethod
    def from_csv(file_path, id_name="key"):
        data = dict()

        for data_dict in utils.read_csv(file_path):
            data_id = data_dict.get(id_name)
            if data_id in data:
                raise Exception('Found duplicate key {} in {}, the container {} will be ignored'
                                .format(data_id, file_path, data_dict.get('name')))

            if data_dict.get('assets'):
                assets_str = data_dict.get('assets')
                assets_splits = assets_str.replace('[', '').replace(']', '').split(',')
                assets_list = list(
                    map(
                        lambda s: int(s.strip()) if len(s.strip()) > 0 else None,
                        assets_splits
                    )
                )
                data_dict['assets'] = assets_list

            if data_dict.get('records'):
                records_str = data_dict.get('records')
                records_splits = records_str.replace('\'', '').replace('[', '').replace(']', '').split(',')
                records_list = list(
                    map(
                        lambda s: int(s.strip()) if len(s.strip()) > 0 else None,
                        records_splits
                    )
                )
                data_dict['records'] = records_list

            data[data_id] = data_dict

        return data

    @staticmethod
    def generate_sql_query(volume_id, suffix_path=constants.DEFAULT_SERVER_PREFIX):
        """
        Generate Databrary DB query that
        :param suffix_path:
        :param volume_id: Volume ID
        :return:
        """
        return "COPY (" \
               "select 'mkdir -p {}/{}/' || sa.container || ' && ' || E'cp \"/nyu/store/' || substr(cast(sha1 as varchar(80)), 3, 2) || '/' || right(cast(sha1 as varchar(80)), -4) || '\" \"' || '/nyu/stage/reda/{}/' || sa.container || '/' || CASE WHEN a.name LIKE '%.___' IS FALSE THEN a.name || '.' || f.extension[1] || '\"' ELSE a.name || '\"' END from slot_asset sa inner join asset a on sa.asset = a.id inner join format f on a.format = f.id where a.volume = {}) TO '/tmp/volume_{}.sh';".format(suffix_path, volume_id, volume_id, volume_id)
