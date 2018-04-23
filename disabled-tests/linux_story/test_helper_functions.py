# test_helper_functions.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# Test helper functions

import pytest
from test.test_support import EnvironmentVarGuard

from linux_story.helper_functions import wrap_in_box, get_language_dirs


@pytest.yield_fixture
def test_env():
    with EnvironmentVarGuard() as env:
        yield env


def test_wrap_in_box():
    output = wrap_in_box([
        '{{gb:This is a long string}}',
        'Short {{lb:string}}',
    ])

    assert output == [
        " ----------------------- ",
        "| {{gb:This is a long string}} |",
        "| Short {{lb:string}}          |",
        " ----------------------- \n",
    ]


def test_get_language_dirs(test_env):
    test_env['LANG'] = 'en_GB.UTF-8'

    language_dirs = get_language_dirs()

    assert language_dirs == [
        'en_GB.UTF-8',
        'en_GB',
        'en.UTF-8',
        'en',
    ]
