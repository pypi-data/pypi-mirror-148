# Python Databrary API Wrapper
This is a Python wrapper around [databrary](https://www.databrary.org) API

## Installation 
Run the following to install:
```bash
pip install pydatabrary
```

## Usage

### Databrary API
```python
from pybrary import Pybrary

# Start a Databrary session
pb = Pybrary.get_instance('USERNAME', 'PASSWORD')
# You need to have permissions to the volume, to interact with it
volume_info = pb.get_volume_info(1)
print(volume_info)
```

### Databrary Curation
#### Generate templates
This will generate for you template files where you can curate your new volume
```python
from pybrary import Curation

# The number of records that you need for your ingest
payload = {
    'participant': 0,
    'pilot': 0,
    'exclusion': 0,
    'condition': 0,
    'group': 0,
    'task': 0,
    'context': 0,
}
records = Curation.generate_records(categories=payload, output='/PATH/TO/OUTPUT/CSV')

# Generate an asset csv file from a local folder
assets = Curation.generate_assets('PATH/TO/FOLDER/', output='/PATH/TO/OUTPUT/CSV')

# Value is the number of containers you wish to generate
containers = Curation.generate_containers(value=2, output='/PATH/TO/OUTPUT/CSV')
```

#### Read CSV files
After you edit your CSV files you will have to pass them to ```Curation``` to validate them and
generate the JSON file needed for your ingest

Only the containers file is required. if you provide assets and records files,```Curation``` will populate
asset and record ids found in the container from the provided files.

Note: ```pybrary``` will ignore duplicate keys, so make sure to have unique ids for your rows
```python
from pybrary import Curation

volume = Curation.from_files(
    volume_name="TEST", 
    containers_file='PATH/TO/CONTAINER/FILE',
    assets_file='PATH/TO/ASSET/FILE',
    records_file='PATH/TO/RECORD/FILE'
)
```
Generate the ingest file
```python
from pybrary import Curation

volume = Curation.from_files(
    volume_name="TEST", 
    containers_file='PATH/TO/CONTAINER/FILE',
    assets_file='PATH/TO/ASSET/FILE',
    records_file='PATH/TO/RECORD/FILE'
)
Curation.to_json(volume, '/PATH/TO/JSON/OUTPUT')
```

### Duplicate existing volume
Get your volume from databrary
```python
from pybrary import Curation

volume = Curation.from_databrary(
    volume_id=1,
    username='YOUR_USERNAME',
    password='YOUR_PASSWORD'
)

# You can edit your volume programmatically or dump your volume in
# csv files that you can edit with your text editor
Curation.to_files(
    volume, 
    containers_output='PATH/TO/CONTAINER/FILE',
    assets_output='PATH/TO/ASSET/FILE',
    records_output='PATH/TO/RECORD/FILE'
)
# once your are done you can import your files
```
Generate the SQL query to execute on the server (Please contact Databray admin)
```python
from pybrary import Curation
# Source is the source volume
# Target is the target volume
Curation.generate_sql_query(volume_id=1)
```
The SQL query will create a script in ```/tmp/volume_id.sh``` that need to be executed prior
to the ingest, it will copy the volume's asset into a staging folder.

**Note:** The staging folder on the server (where files are copied) and the path
of the file in the final ingest file must match

## Development
Test
```shell
pytest
```

Install Locally
```shell
pip install -e .
```

Build
```shell
python -m build
```

Publish
```shell
twine upload dist/*
```

## TODOs
* Generate documentation and add examples.
* Check for duplicate records and asset id.
* check if the record measures are valid.
* Fix utils methods.



