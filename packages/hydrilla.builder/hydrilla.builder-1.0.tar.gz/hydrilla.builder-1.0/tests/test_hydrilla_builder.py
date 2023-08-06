# SPDX-License-Identifier: CC0-1.0

# Copyright (C) 2022 Wojtek Kosior <koszko@koszko.org>
#
# Available under the terms of Creative Commons Zero v1.0 Universal.

# Enable using with Python 3.7.
from __future__ import annotations

import pytest
import json
import shutil

from tempfile import TemporaryDirectory
from pathlib import Path
from hashlib import sha256, sha1
from zipfile import ZipFile
from typing import Callable, Optional, Iterable

from jsonschema import ValidationError

from hydrilla import util as hydrilla_util
from hydrilla.builder import build, _version

here = Path(__file__).resolve().parent

expected_generated_by = {
    'name': 'hydrilla.builder',
    'version': _version.version
}

default_srcdir = here / 'source-package-example'

default_js_filenames = ['bye.js', 'hello.js', 'message.js']
default_dist_filenames = [*default_js_filenames, 'LICENSES/CC0-1.0.txt']
default_src_filenames = [
    *default_dist_filenames,
    'README.txt', 'README.txt.license', '.reuse/dep5', 'index.json'
]

default_sha1_hashes   = {}
default_sha256_hashes = {}
default_contents      = {}

for fn in default_src_filenames:
    with open(default_srcdir / fn, 'rb') as file_handle:
        default_contents[fn]      = file_handle.read()
        default_sha256_hashes[fn] = sha256(default_contents[fn]).digest().hex()
        default_sha1_hashes[fn]   = sha1(default_contents[fn]).digest().hex()

class CaseSettings:
    """Gather parametrized values in a class."""
    def __init__(self):
        """Init CaseSettings with default values."""
        self.srcdir = default_srcdir
        self.index_json_path = Path('index.json')
        self.report_spdx_included = True

        self.js_filenames   = default_js_filenames.copy()
        self.dist_filenames = default_dist_filenames.copy()
        self.src_filenames  = default_src_filenames.copy()

        self.sha1_hashes   = default_sha1_hashes.copy()
        self.sha256_hashes = default_sha256_hashes.copy()
        self.contents      = default_contents.copy()

        self.expected_resources = [{
            '$schema': 'https://hydrilla.koszko.org/schemas/api_resource_description-1.schema.json',
            'source_name': 'hello',
            'source_copyright': [{
                'file': 'report.spdx',
                'sha256': '!!!!value to fill during test!!!!'
            }, {
                'file': 'LICENSES/CC0-1.0.txt',
                'sha256': self.sha256_hashes['LICENSES/CC0-1.0.txt']
            }],
            'type': 'resource',
            'identifier': 'helloapple',
            'long_name': 'Hello Apple',
            'uuid': 'a6754dcb-58d8-4b7a-a245-24fd7ad4cd68',
            'version': [2021, 11, 10],
            'revision': 1,
            'description': 'greets an apple',
            'dependencies': [{'identifier': 'hello-message'}],
            'scripts': [{
                'file': 'hello.js',
                'sha256': self.sha256_hashes['hello.js']
            }, {
                'file': 'bye.js',
                'sha256': self.sha256_hashes['bye.js']
            }],
            'generated_by': expected_generated_by
        }, {
            '$schema': 'https://hydrilla.koszko.org/schemas/api_resource_description-1.schema.json',
            'source_name': 'hello',
            'source_copyright': [{
                'file': 'report.spdx',
                'sha256': '!!!!value to fill during test!!!!'
            }, {
                'file': 'LICENSES/CC0-1.0.txt',
                'sha256': self.sha256_hashes['LICENSES/CC0-1.0.txt']
            }],
            'type': 'resource',
            'identifier': 'hello-message',
            'long_name': 'Hello Message',
            'uuid': '1ec36229-298c-4b35-8105-c4f2e1b9811e',
            'version': [2021, 11, 10],
            'revision': 2,
            'description': 'define messages for saying hello and bye',
            'dependencies': [],
            'scripts': [{
                'file': 'message.js',
                'sha256': self.sha256_hashes['message.js']
            }],
            'generated_by': expected_generated_by
        }]
        self.expected_mapping = {
            '$schema': 'https://hydrilla.koszko.org/schemas/api_mapping_description-1.schema.json',
            'source_name': 'hello',
            'source_copyright': [{
                'file': 'report.spdx',
                'sha256': '!!!!value to fill during test!!!!'
            }, {
                'file': 'LICENSES/CC0-1.0.txt',
                'sha256': self.sha256_hashes['LICENSES/CC0-1.0.txt']
            }],
            'type': 'mapping',
	    'identifier': 'helloapple',
	    'long_name': 'Hello Apple',
	    'uuid': '54d23bba-472e-42f5-9194-eaa24c0e3ee7',
	    'version': [2021, 11, 10],
	    'description': 'causes apple to get greeted on Hydrillabugs issue tracker',
	    'payloads': {
	        'https://hydrillabugs.koszko.org/***': {
		    'identifier': 'helloapple'
	        },
	        'https://hachettebugs.koszko.org/***': {
		    'identifier': 'helloapple'
                }
            },
            'generated_by': expected_generated_by
        }
        self.expected_source_description = {
            '$schema': 'https://hydrilla.koszko.org/schemas/api_source_description-1.schema.json',
            'source_name': 'hello',
            'source_copyright': [{
                'file': 'report.spdx',
                'sha256': '!!!!value to fill during test!!!!'
            }, {
                'file': 'LICENSES/CC0-1.0.txt',
                'sha256': self.sha256_hashes['LICENSES/CC0-1.0.txt']
            }],
            'source_archives': {
                'zip': {
                    'sha256': '!!!!value to fill during test!!!!',
                }
            },
            'upstream_url': 'https://git.koszko.org/hydrilla-source-package-example',
            'definitions': [{
                'type': 'resource',
                'identifier': 'helloapple',
                'long_name': 'Hello Apple',
                'version': [2021, 11, 10],
            }, {
                'type':       'resource',
                'identifier': 'hello-message',
                'long_name': 'Hello Message',
                'version':     [2021, 11, 10],
            }, {
                'type': 'mapping',
                'identifier': 'helloapple',
	        'long_name': 'Hello Apple',
                'version': [2021, 11, 10],
            }],
            'generated_by': expected_generated_by
        }

    def expected(self) -> list[dict]:
        """
        Convenience method to get a list of expected jsons of 2 resources,
        1 mapping and 1 source description we have.
        """
        return [
            *self.expected_resources,
            self.expected_mapping,
            self.expected_source_description
        ]

ModifyCb = Callable[[CaseSettings, dict], Optional[str]]

def prepare_modified(tmpdir: Path, modify_cb: ModifyCb) -> CaseSettings:
    """
    Use sample source package directory with an alternative, modified
    index.json.
    """
    settings = CaseSettings()

    for fn in settings.src_filenames:
        copy_path = tmpdir / 'srcdir_copy' / fn
        copy_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(settings.srcdir / fn, copy_path)

    settings.srcdir = tmpdir / 'srcdir_copy'

    with open(settings.srcdir / 'index.json', 'rt') as file_handle:
        obj = json.loads(hydrilla_util.strip_json_comments(file_handle.read()))

    contents = modify_cb(settings, obj)

    # Replace the other index.json with new one
    settings.index_json_path = tmpdir / 'replacement.json'

    if contents is None:
        contents = json.dumps(obj)

    contents = contents.encode()

    settings.contents['index.json'] = contents

    settings.sha256_hashes['index.json'] = sha256(contents).digest().hex()
    settings.sha1_hashes['index.json']   = sha1(contents).digest().hex()

    with open(settings.index_json_path, 'wb') as file_handle:
        file_handle.write(contents)

    return settings

@pytest.fixture()
def tmpdir() -> Iterable[str]:
    with TemporaryDirectory() as tmpdir:
        yield tmpdir

def prepare_default(tmpdir: Path) -> CaseSettings:
    """Use sample source package directory as exists in VCS."""
    return CaseSettings()

def modify_index_good(settings: CaseSettings, obj: dict) -> None:
    """
    Modify index.json object to make a slightly different but *also correct* one
    that can be used to test some different cases.
    """
    # Add comments that should be preserved.
    for dictionary in (obj, settings.expected_source_description):
        dictionary['comment'] = 'index_json comment'

    for i, dicts in enumerate(zip(obj['definitions'], settings.expected())):
        for dictionary in dicts:
            dictionary['comment'] = f'item {i}'

    # Remove spdx report generation
    del obj['reuse_generate_spdx_report']
    obj['copyright'].remove({'file': 'report.spdx'})

    settings.report_spdx_included = False

    for json_description in settings.expected():
        json_description['source_copyright'] = \
            [fr for fr in json_description['source_copyright']
             if fr['file'] != 'report.spdx']

    # Use default value ([]) for 'additionall_files' property
    del obj['additional_files']

    settings.src_filenames = [*settings.dist_filenames, 'index.json']

    # Use default value ([]) for 'scripts' property in one of the resources
    del obj['definitions'][1]['scripts']

    settings.expected_resources[1]['scripts'] = []

    for prefix in ('js', 'dist', 'src'):
        getattr(settings, f'{prefix}_filenames').remove('message.js')

    # Use default value ({}) for 'pyloads' property in mapping
    del obj['definitions'][2]['payloads']

    settings.expected_mapping['payloads'] = {}

    # Don't use UUIDs (they are optional)
    for definition in obj['definitions']:
        del definition['uuid']

    for description in settings.expected():
        if 'uuid' in description:
            del description['uuid']

    # Add some unrecognized properties that should be stripped
    to_process = [obj]
    while to_process:
        processed = to_process.pop()

        if type(processed) is list:
            to_process.extend(processed)
        elif type(processed) is dict and 'spurious_property' not in processed:
            to_process.extend(processed.values())
            processed['spurious_property'] = 'some value'

@pytest.mark.parametrize('prepare_source_example', [
    prepare_default,
    lambda tmpdir: prepare_modified(tmpdir, modify_index_good)
])
def test_build(tmpdir, prepare_source_example):
    """Build the sample source package and verify the produced files."""
    # First, build the package
    dstdir = Path(tmpdir) / 'dstdir'
    tmpdir = Path(tmpdir) / 'example'

    dstdir.mkdir(exist_ok=True)
    tmpdir.mkdir(exist_ok=True)

    settings = prepare_source_example(tmpdir)

    build.Build(settings.srcdir, settings.index_json_path)\
        .write_package_files(dstdir)

    # Verify directories under destination directory
    assert {'file', 'resource', 'mapping', 'source'} == \
        set([path.name for path in dstdir.iterdir()])

    # Verify files under 'file/'
    file_dir = dstdir / 'file' / 'sha256'

    for fn in settings.dist_filenames:
        dist_file_path = file_dir / settings.sha256_hashes[fn]
        assert dist_file_path.is_file()

        assert dist_file_path.read_bytes() == settings.contents[fn]

    sha256_hashes_set = set([settings.sha256_hashes[fn]
                             for fn in settings.dist_filenames])

    spdx_report_sha256 = None

    for path in file_dir.iterdir():
        if path.name in sha256_hashes_set:
            continue

        assert spdx_report_sha256 is None and settings.report_spdx_included

        with open(path, 'rt') as file_handle:
            spdx_contents = file_handle.read()

        spdx_report_sha256 = sha256(spdx_contents.encode()).digest().hex()
        assert spdx_report_sha256 == path.name

        for fn in settings.src_filenames:
            if not any([n in fn.lower() for n in ('license', 'reuse')]):
                assert settings.sha1_hashes[fn]

    if settings.report_spdx_included:
        assert spdx_report_sha256
        for obj in settings.expected():
            for file_ref in obj['source_copyright']:
                if file_ref['file'] == 'report.spdx':
                    file_ref['sha256'] = spdx_report_sha256

    # Verify files under 'resource/'
    resource_dir = dstdir / 'resource'

    assert set([rj['identifier'] for rj in settings.expected_resources]) == \
        set([path.name for path in resource_dir.iterdir()])

    for resource_json in settings.expected_resources:
        subdir = resource_dir / resource_json['identifier']
        assert ['2021.11.10'] == [path.name for path in subdir.iterdir()]

        with open(subdir / '2021.11.10', 'rt') as file_handle:
            assert json.load(file_handle) == resource_json

        hydrilla_util.validator_for('api_resource_description-1.0.1.schema.json')\
                     .validate(resource_json)

    # Verify files under 'mapping/'
    mapping_dir = dstdir / 'mapping'
    assert ['helloapple'] == [path.name for path in mapping_dir.iterdir()]

    subdir = mapping_dir / 'helloapple'
    assert ['2021.11.10'] == [path.name for path in subdir.iterdir()]

    with open(subdir / '2021.11.10', 'rt') as file_handle:
        assert json.load(file_handle) == settings.expected_mapping

    hydrilla_util.validator_for('api_mapping_description-1.0.1.schema.json')\
                 .validate(settings.expected_mapping)

    # Verify files under 'source/'
    source_dir = dstdir / 'source'
    assert {'hello.json', 'hello.zip'} == \
        set([path.name for path in source_dir.iterdir()])

    zip_filenames = [f'hello/{fn}' for fn in settings.src_filenames]

    with ZipFile(source_dir / 'hello.zip', 'r') as archive:
        assert set([f.filename for f in archive.filelist]) == set(zip_filenames)

        for zip_fn, src_fn in zip(zip_filenames, settings.src_filenames):
            with archive.open(zip_fn, 'r') as zip_file_handle:
                assert zip_file_handle.read() == settings.contents[src_fn]

    zip_ref = settings.expected_source_description['source_archives']['zip']
    with open(source_dir / 'hello.zip', 'rb') as file_handle:
        zip_ref['sha256'] = sha256(file_handle.read()).digest().hex()

    with open(source_dir / 'hello.json', 'rt') as file_handle:
        assert json.load(file_handle) == settings.expected_source_description

    hydrilla_util.validator_for('api_source_description-1.0.1.schema.json')\
                 .validate(settings.expected_source_description)

def modify_index_missing_file(dummy: CaseSettings, obj: dict) -> None:
    """
    Modify index.json to expect missing report.spdx file and cause an error.
    """
    del obj['reuse_generate_spdx_report']

def modify_index_schema_error(dummy: CaseSettings, obj: dict) -> None:
    """Modify index.json to be incompliant with the schema."""
    del obj['definitions']

def modify_index_bad_comment(dummy: CaseSettings, obj: dict) -> str:
    """Modify index.json to have an invalid '/' in it."""
    return json.dumps(obj) + '/something\n'

def modify_index_bad_json(dummy: CaseSettings, obj: dict) -> str:
    """Modify index.json to not be valid json even after comment stripping."""
    return json.dumps(obj) + '???/\n'

def modify_index_missing_license(settings: CaseSettings, obj: dict) -> None:
    """Remove a file to make package REUSE-incompliant."""
    (settings.srcdir / 'README.txt.license').unlink()

def modify_index_file_outside(dummy: CaseSettings, obj: dict) -> None:
    """Make index.json illegally reference a file outside srcdir."""
    obj['copyright'].append({'file': '../abc'})

def modify_index_reference_itself(dummy: CaseSettings, obj: dict) -> None:
    """Make index.json illegally reference index.json."""
    obj['copyright'].append({'file': 'index.json'})

def modify_index_report_excluded(dummy: CaseSettings, obj: dict) -> None:
    """
    Make index.json require generation of index.json but not include it among
    copyright files.
    """
    obj['copyright'] = [fr for fr in obj['copyright']
                        if fr['file'] != 'report.spdx']

@pytest.mark.parametrize('break_index_json', [
    (modify_index_missing_file,     FileNotFoundError),
    (modify_index_schema_error,     ValidationError),
    (modify_index_bad_comment,      json.JSONDecodeError),
    (modify_index_bad_json,         json.JSONDecodeError),
    (modify_index_missing_license,  build.ReuseError),
    (modify_index_file_outside,     build.FileReferenceError),
    (modify_index_reference_itself, build.FileReferenceError),
    (modify_index_report_excluded,  build.FileReferenceError)
])
def test_build_error(tmpdir: str, break_index_json: tuple[ModifyCb, type]):
    """Build the sample source package and verify the produced files."""
    dstdir = Path(tmpdir) / 'dstdir'
    tmpdir = Path(tmpdir) / 'example'

    dstdir.mkdir(exist_ok=True)
    tmpdir.mkdir(exist_ok=True)

    modify_cb, error_type = break_index_json

    settings = prepare_modified(tmpdir, modify_cb)

    with pytest.raises(error_type):
        build.Build(settings.srcdir, settings.index_json_path)\
            .write_package_files(dstdir)
