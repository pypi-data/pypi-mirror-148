# SPDX-License-Identifier: AGPL-3.0-or-later

# Building Hydrilla packages.
#
# This file is part of Hydrilla
#
# Copyright (C) 2022 Wojtek Kosior
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#
# I, Wojtek Kosior, thereby promise not to sue for violation of this
# file's license. Although I request that you do not make use this code
# in a proprietary program, I am not going to enforce this in court.

# Enable using with Python 3.7.
from __future__ import annotations

import json
import re
import zipfile
from pathlib import Path
from hashlib import sha256
from sys import stderr

import jsonschema
import click

from .. import util
from . import _version

here = Path(__file__).resolve().parent

_ = util.translation(here / 'locales').gettext

index_validator = util.validator_for('package_source-1.0.1.schema.json')

schemas_root = 'https://hydrilla.koszko.org/schemas'

generated_by = {
    'name': 'hydrilla.builder',
    'version': _version.version
}

class FileReferenceError(Exception):
    """
    Exception used to report various problems concerning files referenced from
    source package's index.json.
    """

class ReuseError(Exception):
    """
    Exception used to report various problems when calling the REUSE tool.
    """

class FileBuffer:
    """
    Implement a file-like object that buffers data written to it.
    """
    def __init__(self):
        """
        Initialize FileBuffer.
        """
        self.chunks = []

    def write(self, b):
        """
        Buffer 'b', return number of bytes buffered.

        'b' is expected to be an instance of 'bytes' or 'str', in which case it
        gets encoded as UTF-8.
        """
        if type(b) is str:
            b = b.encode()
        self.chunks.append(b)
        return len(b)

    def flush(self):
        """
        A no-op mock of file-like object's flush() method.
        """
        pass

    def get_bytes(self):
        """
        Return all data written so far concatenated into a single 'bytes'
        object.
        """
        return b''.join(self.chunks)

def generate_spdx_report(root):
    """
    Use REUSE tool to generate an SPDX report for sources under 'root' and
    return the report's contents as 'bytes'.

    'root' shall be an instance of pathlib.Path.

    In case the directory tree under 'root' does not constitute a
    REUSE-compliant package, linting report is printed to standard output and
    an exception is raised.

    In case the reuse package is not installed, an exception is also raised.
    """
    try:
        from reuse._main import main as reuse_main
    except ModuleNotFoundError:
        raise ReuseError(_('couldnt_import_reuse_is_it_installed'))

    mocked_output = FileBuffer()
    if reuse_main(args=['--root', str(root), 'lint'], out=mocked_output) != 0:
        stderr.write(mocked_output.get_bytes().decode())
        raise ReuseError(_('spdx_report_from_reuse_incompliant'))

    mocked_output = FileBuffer()
    if reuse_main(args=['--root', str(root), 'spdx'], out=mocked_output) != 0:
        stderr.write(mocked_output.get_bytes().decode())
        raise ReuseError("Couldn't generate an SPDX report for package.")

    return mocked_output.get_bytes()

class FileRef:
    """Represent reference to a file in the package."""
    def __init__(self, path: Path, contents: bytes):
        """Initialize FileRef."""
        self.include_in_distribution = False
        self.include_in_zipfile      = True
        self.path                    = path
        self.contents                = contents

        self.contents_hash = sha256(contents).digest().hex()

    def make_ref_dict(self, filename: str):
        """
        Represent the file reference through a dict that can be included in JSON
        defintions.
        """
        return {
            'file':   filename,
            'sha256': self.contents_hash
        }

class Build:
    """
    Build a Hydrilla package.
    """
    def __init__(self, srcdir, index_json_path):
        """
        Initialize a build. All files to be included in a distribution package
        are loaded into memory, all data gets validated and all necessary
        computations (e.g. preparing of hashes) are performed.

        'srcdir' and 'index_json' are expected to be pathlib.Path objects.
        """
        self.srcdir          = srcdir.resolve()
        self.index_json_path = index_json_path
        self.files_by_path   = {}
        self.resource_list   = []
        self.mapping_list    = []

        if not index_json_path.is_absolute():
            self.index_json_path = (self.srcdir / self.index_json_path)

        self.index_json_path = self.index_json_path.resolve()

        with open(self.index_json_path, 'rt') as index_file:
            index_json_text = index_file.read()

        index_obj = json.loads(util.strip_json_comments(index_json_text))

        self.files_by_path[self.srcdir / 'index.json'] = \
            FileRef(self.srcdir / 'index.json', index_json_text.encode())

        self._process_index_json(index_obj)

    def _process_file(self, filename: str, include_in_distribution: bool=True):
        """
        Resolve 'filename' relative to srcdir, load it to memory (if not loaded
        before), compute its hash and store its information in
        'self.files_by_path'.

        'filename' shall represent a relative path using '/' as a separator.

        if 'include_in_distribution' is True it shall cause the file to not only
        be included in the source package's zipfile, but also written as one of
        built package's files.

        Return file's reference object that can be included in JSON defintions
        of various kinds.
        """
        path = self.srcdir
        for segment in filename.split('/'):
            path /= segment

        path = path.resolve()
        if not path.is_relative_to(self.srcdir):
            raise FileReferenceError(_('loading_{}_outside_package_dir')
                                     .format(filename))

        if str(path.relative_to(self.srcdir)) == 'index.json':
            raise FileReferenceError(_('loading_reserved_index_json'))

        file_ref = self.files_by_path.get(path)
        if file_ref is None:
            with open(path, 'rb') as file_handle:
                contents = file_handle.read()

            file_ref = FileRef(path, contents)
            self.files_by_path[path] = file_ref

        if include_in_distribution:
            file_ref.include_in_distribution = True

        return file_ref.make_ref_dict(filename)

    def _prepare_source_package_zip(self, root_dir_name: str):
        """
        Create and store in memory a .zip archive containing files needed to
        build this source package.

        'root_dir_name' shall not contain any slashes ('/').

        Return zipfile's sha256 sum's hexstring.
        """
        fb = FileBuffer()
        root_dir_path = Path(root_dir_name)

        def zippath(file_path):
            file_path = root_dir_path / file_path.relative_to(self.srcdir)
            return file_path.as_posix()

        with zipfile.ZipFile(fb, 'w') as xpi:
            for file_ref in self.files_by_path.values():
                if file_ref.include_in_zipfile:
                    xpi.writestr(zippath(file_ref.path), file_ref.contents)

        self.source_zip_contents = fb.get_bytes()

        return sha256(self.source_zip_contents).digest().hex()

    def _process_item(self, item_def: dict):
        """
        Process 'item_def' as definition of a resource/mapping and store in
        memory its processed form and files used by it.

        Return a minimal item reference suitable for using in source
        description.
        """
        copy_props = ['type', 'identifier', 'long_name', 'description']
        for prop in ('comment', 'uuid'):
            if prop in item_def:
                copy_props.append(prop)

        if item_def['type'] == 'resource':
            item_list = self.resource_list

            copy_props.append('revision')

            script_file_refs = [self._process_file(f['file'])
                                for f in item_def.get('scripts', [])]

            deps = [{'identifier': res_ref['identifier']}
                    for res_ref in item_def.get('dependencies', [])]

            new_item_obj = {
                'dependencies': deps,
                'scripts':      script_file_refs
            }
        else:
            item_list = self.mapping_list

            payloads = {}
            for pat, res_ref in item_def.get('payloads', {}).items():
                payloads[pat] = {'identifier': res_ref['identifier']}

            new_item_obj = {
                'payloads': payloads
            }

        new_item_obj.update([(p, item_def[p]) for p in copy_props])

        new_item_obj['version'] = util.normalize_version(item_def['version'])
        new_item_obj['$schema'] = f'{schemas_root}/api_{item_def["type"]}_description-1.schema.json'
        new_item_obj['source_copyright'] = self.copyright_file_refs
        new_item_obj['source_name'] = self.source_name
        new_item_obj['generated_by'] = generated_by

        item_list.append(new_item_obj)

        props_in_ref = ('type', 'identifier', 'version', 'long_name')
        return dict([(prop, new_item_obj[prop]) for prop in props_in_ref])

    def _process_index_json(self, index_obj: dict):
        """
        Process 'index_obj' as contents of source package's index.json and store
        in memory this source package's zipfile as well as package's individual
        files and computed definitions of the source package and items defined
        in it.
        """
        index_validator.validate(index_obj)

        schema = f'{schemas_root}/api_source_description-1.schema.json'

        self.source_name = index_obj['source_name']

        generate_spdx = index_obj.get('reuse_generate_spdx_report', False)
        if generate_spdx:
            contents  = generate_spdx_report(self.srcdir)
            spdx_path = (self.srcdir / 'report.spdx').resolve()
            spdx_ref  = FileRef(spdx_path, contents)

            spdx_ref.include_in_zipfile = False
            self.files_by_path[spdx_path] = spdx_ref

        self.copyright_file_refs = \
            [self._process_file(f['file']) for f in index_obj['copyright']]

        if generate_spdx and not spdx_ref.include_in_distribution:
            raise FileReferenceError(_('report_spdx_not_in_copyright_list'))

        item_refs = [self._process_item(d) for d in index_obj['definitions']]

        for file_ref in index_obj.get('additional_files', []):
            self._process_file(file_ref['file'], include_in_distribution=False)

        root_dir_path = Path(self.source_name)

        source_archives_obj = {
            'zip' : {
                'sha256': self._prepare_source_package_zip(root_dir_path)
            }
        }

        self.source_description = {
            '$schema':            schema,
            'source_name':        self.source_name,
            'source_copyright':   self.copyright_file_refs,
            'upstream_url':       index_obj['upstream_url'],
            'definitions':        item_refs,
            'source_archives':    source_archives_obj,
            'generated_by':       generated_by
        }

        if 'comment' in index_obj:
            self.source_description['comment'] = index_obj['comment']

    def write_source_package_zip(self, dstpath: Path):
        """
        Create a .zip archive containing files needed to build this source
        package and write it at 'dstpath'.
        """
        with open(dstpath, 'wb') as output:
            output.write(self.source_zip_contents)

    def write_package_files(self, dstpath: Path):
        """Write package files under 'dstpath' for distribution."""
        file_dir_path = (dstpath / 'file' / 'sha256').resolve()
        file_dir_path.mkdir(parents=True, exist_ok=True)

        for file_ref in self.files_by_path.values():
            if file_ref.include_in_distribution:
                file_path = file_dir_path / file_ref.contents_hash
                file_path.write_bytes(file_ref.contents)

        source_dir_path = (dstpath / 'source').resolve()
        source_dir_path.mkdir(parents=True, exist_ok=True)
        source_name = self.source_description["source_name"]

        with open(source_dir_path / f'{source_name}.json', 'wt') as output:
            json.dump(self.source_description, output)

        with open(source_dir_path / f'{source_name}.zip', 'wb') as output:
            output.write(self.source_zip_contents)

        for item_type, item_list in [
                ('resource', self.resource_list),
                ('mapping', self.mapping_list)
        ]:
            item_type_dir_path = (dstpath / item_type).resolve()

            for item_def in item_list:
                item_dir_path = item_type_dir_path / item_def['identifier']
                item_dir_path.mkdir(parents=True, exist_ok=True)

                version = '.'.join([str(n) for n in item_def['version']])
                with open(item_dir_path / version, 'wt') as output:
                    json.dump(item_def, output)

dir_type = click.Path(exists=True, file_okay=False, resolve_path=True)

@click.option('-s', '--srcdir', default='./', type=dir_type, show_default=True,
              help=_('source_directory_to_build_from'))
@click.option('-i', '--index-json', default='index.json', type=click.Path(),
              help=_('path_instead_of_index_json'))
@click.option('-d', '--dstdir', type=dir_type, required=True,
              help=_('built_package_files_destination'))
@click.version_option(version=_version.version, prog_name='Hydrilla builder',
                      message=_('%(prog)s_%(version)s_license'),
                      help=_('version_printing'))
def perform(srcdir, index_json, dstdir):
    """<this will be replaced by a localized docstring for Click to pick up>"""
    build = Build(Path(srcdir), Path(index_json))
    build.write_package_files(Path(dstdir))

perform.__doc__ = _('build_package_from_srcdir_to_dstdir')

perform = click.command()(perform)
