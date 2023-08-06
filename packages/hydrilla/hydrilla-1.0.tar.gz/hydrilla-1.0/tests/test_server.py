# SPDX-License-Identifier: AGPL-3.0-or-later

# Repository tests
#
# This file is part of Hydrilla
#
# Copyright (C) 2021, 2022 Wojtek Kosior
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

import pytest
import sys
import shutil
import json

from pathlib import Path
from hashlib import sha256
from tempfile import TemporaryDirectory
from typing import Callable, Optional

from flask.testing import FlaskClient
from markupsafe import escape
from werkzeug import Response

from hydrilla import util as hydrilla_util
from hydrilla.builder import Build
from hydrilla.server import config, _version
from hydrilla.server.serve import HydrillaApp

here        = Path(__file__).resolve().parent
config_path = here / 'config.json'
source_path = here / 'source-package-example'

expected_generated_by = {
    'name': 'hydrilla.server',
    'version': _version.version
}

SetupMod = Optional[Callable['Setup', None]]

source_files = (
    'index.json', 'hello.js', 'bye.js', 'message.js', 'README.txt',
    'README.txt.license', '.reuse/dep5', 'LICENSES/CC0-1.0.txt'
)

class Setup:
    """
    Facilitate preparing test malcontent directory, Hydrilla config file and the
    actual Flask client. In a customizable way.
    """
    def __init__(self, modify_before_build: SetupMod=None,
                 modify_after_build: SetupMod=None) -> None:
        """Initialize Setup."""
        self._modify_before_build = modify_before_build
        self._modify_after_build = modify_after_build
        self._config = None
        self._client = None

    def _prepare(self) -> None:
        """Perform the build and call the callbacks as appropriate."""
        self.tmpdir = TemporaryDirectory()

        self.containing_dir = Path(self.tmpdir.name)
        self.malcontent_dir = self.containing_dir / 'sample_malcontent'
        self.index_json     = Path('index.json')

        self.source_dir = self.containing_dir / 'sample_source_package'
        for source_file in source_files:
            dst_path = self.source_dir / source_file
            dst_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source_path / source_file, dst_path)

        self.config_path = self.containing_dir / 'config.json'
        shutil.copyfile(config_path, self.config_path)

        if self._modify_before_build:
            self._modify_before_build(self)

        build = Build(self.source_dir, self.index_json)
        build.write_package_files(self.malcontent_dir)

        if self._modify_after_build:
            self._modify_after_build(self)

    def config(self) -> dict:
        """Provide the contents of JSON config file used."""
        if self._config is None:
            self._prepare()
            self._config = config.load([self.config_path])

        return self._config

    def client(self) -> FlaskClient:
        """
        Provide app client that serves the objects from built sample package.
        """
        if self._client is None:
            app = HydrillaApp(self.config(), flask_config={'TESTING': True})
            self._client = app.test_client()

        return self._client

def remove_all_uuids(setup: Setup) -> None:
    """Modify sample packages before build to contain no (optional) UUIDs"""
    index_json = (setup.source_dir / 'index.json').read_text()
    index_json = json.loads(hydrilla_util.strip_json_comments(index_json))

    for definition in index_json['definitions']:
        del definition['uuid']

    index_json = ("// SPDX-License-Identifier: CC0-1.0\n" +
                  "// Copyright (C) 2021, 2022 Wojtek Kosior\n" +
                  json.dumps(index_json))

    (setup.source_dir / 'index.json').write_text(index_json)

default_setup = Setup()
uuidless_setup = Setup(modify_before_build=remove_all_uuids)

def def_get(url: str) -> Response:
    """Convenience wrapper for def_get()"""
    return default_setup.client().get(url)

def test_project_url() -> None:
    """Fetch index.html and verify project URL from config is present there."""
    response = def_get('/')
    assert b'html' in response.data
    project_url = default_setup.config()['hydrilla_project_url']
    assert escape(project_url).encode() in response.data

@pytest.mark.parametrize('setup', [default_setup, uuidless_setup])
@pytest.mark.parametrize('item_type', ['resource', 'mapping'])
def test_get_newest(setup: Setup, item_type: str) -> None:
    """
    Verify that
        GET '/{item_type}/{item_identifier}.json'
    returns proper definition that is also served at:
        GET '/{item_type}/{item_identifier}/{item_version}'
    """
    response = setup.client().get(f'/{item_type}/helloapple.json')
    assert response.status_code == 200
    definition = json.loads(response.data.decode())
    assert definition['type']        == item_type
    assert definition['identifier']  == 'helloapple'

    response = setup.client().get(f'/{item_type}/helloapple/2021.11.10')
    assert response.status_code == 200
    assert definition == json.loads(response.data.decode())

    assert ('uuid' in definition) == (setup is not uuidless_setup)

    hydrilla_util.validator_for(f'api_{item_type}_description-1.0.1.schema.json')\
                 .validate(definition)

@pytest.mark.parametrize('item_type', ['resource', 'mapping'])
def test_get_nonexistent(item_type: str) -> None:
    """
    Verify that attempts to GET a JSON definition of a nonexistent item or item
    version result in 404.
    """
    response = def_get(f'/{item_type}/nonexistentapple.json')
    assert response.status_code == 404
    response = def_get(f'/{item_type}/helloapple/1.2.3.999')
    assert response.status_code == 404

@pytest.mark.parametrize('item_type', ['resource', 'mapping'])
def test_file_refs(item_type: str) -> None:
    """
    Verify that files referenced by definitions are accessible under their
    proper URLs and that their hashes match.
    """
    response = def_get(f'/{item_type}/helloapple/2021.11.10')
    assert response.status_code == 200
    definition = json.loads(response.data.decode())

    for file_ref in [*definition.get('scripts', []),
                     *definition['source_copyright']]:
        hash_sum = file_ref["sha256"]
        response = def_get(f'/file/sha256/{hash_sum}')

        assert response.status_code == 200
        assert sha256(response.data).digest().hex() == hash_sum

def test_empty_query() -> None:
    """
    Verify that querying mappings for URL gives an empty list when there're no
    mathes.
    """
    response = def_get(f'/query?url=https://nonexiste.nt/example')
    assert response.status_code == 200

    response_object = json.loads(response.data.decode())

    assert response_object == {
        '$schema': 'https://hydrilla.koszko.org/schemas/api_query_result-1.schema.json',
        'mappings': [],
        'generated_by': expected_generated_by
    }

    hydrilla_util.validator_for('api_query_result-1.0.1.schema.json')\
                 .validate(response_object)

def test_query() -> None:
    """
    Verify that querying mappings for URL gives a list with reference(s) the the
    matching mapping(s).
    """
    response = def_get(f'/query?url=https://hydrillabugs.koszko.org/')
    assert response.status_code == 200

    response_object = json.loads(response.data.decode())

    assert response_object == {
        '$schema': 'https://hydrilla.koszko.org/schemas/api_query_result-1.schema.json',
        'mappings': [{
            'identifier': 'helloapple',
            'long_name': 'Hello Apple',
            'version': [2021, 11, 10]
        }],
        'generated_by': expected_generated_by
    }

    hydrilla_util.validator_for('api_query_result-1.0.1.schema.json')\
                 .validate(response_object)

def test_source() -> None:
    """Verify source descriptions are properly served."""
    response = def_get(f'/source/hello.json')
    assert response.status_code == 200

    description = json.loads(response.data.decode())
    assert description['source_name'] == 'hello'

    assert sorted([d['identifier'] for d in description['definitions']]) == \
        ['hello-message', 'helloapple', 'helloapple']

    zipfile_hash = description['source_archives']['zip']['sha256']
    response = def_get(f'/source/hello.zip')
    assert sha256(response.data).digest().hex() == zipfile_hash

    hydrilla_util.validator_for('api_source_description-1.0.1.schema.json')\
                 .validate(description)

def test_missing_source() -> None:
    """Verify requests for nonexistent sources result in 404."""
    response = def_get(f'/source/nonexistent.json')
    assert response.status_code == 404

    response = def_get(f'/source/nonexistent.zip')
    assert response.status_code == 404

def test_normalize_version():
    assert hydrilla_util.normalize_version([4, 5, 3, 0, 0]) == [4, 5, 3]
    assert hydrilla_util.normalize_version([1, 0, 5, 0])    == [1, 0, 5]
    assert hydrilla_util.normalize_version([3, 3])          == [3, 3]
