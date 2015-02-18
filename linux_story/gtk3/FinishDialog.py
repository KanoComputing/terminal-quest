#!/usr/bin/env python
#
# Copyright (C) 2014, 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# FinishDialog.py
# This is the dialog that's shown when the final challenge is completed


from kano.gtk3.kano_dialog import KanoDialog


class FinishDialog(KanoDialog):

    def __init__(self):

        title_text = 'You\'ve completed Terminal Quest'
        description_text = (
            'We are working on the next Chapter. '
            'In the meantime, would you like to send us any feedback?'
        )

        KanoDialog.__init__(
            self,
            title_text=title_text,
            description_text=description_text,
            button_dict={
                'LAUNCH FEEDBACK':
                {
                    'color': 'blue',
                    'return_value': 'feedback'
                },
                'CLOSE APPLICATION':
                {
                    'color': 'orange',
                    'return_value': 'close'
                }
            }
        )
