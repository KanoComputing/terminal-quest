# test_helper_functions.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# Test helper functions

from linux_story.helper_functions import wrap_in_box


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
