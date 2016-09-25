# FinishDialog.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# This is the dialog that's shown when the final challenge is completed


from kano.gtk3.kano_dialog import KanoDialog


class FinishDialog(KanoDialog):

    def __init__(self):

        title_text = _('You\'ve completed Terminal Quest!')
        description_text = \
            _('We are working on the next Chapter. ' +\
            'In the meantime, would you like to send us any feedback?')

        KanoDialog.__init__(
            self,
            title_text=title_text,
            description_text=description_text,
            button_dict={
                _('LAUNCH FEEDBACK'):
                {
                    'color': 'blue',
                    'return_value': 'feedback'
                },
                _('CLOSE APPLICATION'):
                {
                    'color': 'orange',
                    'return_value': 'close'
                }
            }
        )
