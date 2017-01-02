# terminal_bernard.py
#
# Copyright (C) 2014-2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# A terminal for one of the challenges


from linux_story.story.terminals.terminal_eleanor import \
    TerminalNanoEleanor, TerminalMkdirEleanor

# Ideally put in the class, but otherwise have to repeat this across the
# different classes.
bernard_text = _("Bernard stopped you looking in the basement!")


class TerminalMkdirBernard(TerminalMkdirEleanor):

    # These functions are repeated across the two classes.
    def block_command(self):
        if "basement" in self.last_user_input and \
                (
                    "ls" in self.last_user_input or
                    "cat" in self.last_user_input
                ):
            print bernard_text
            return True
        else:
            return TerminalMkdirEleanor.block_command(self)

    def autocomplete_files(self, text, line, begidx, endidx, only_dirs=False, only_exe=False):
        # if the path we're checking is in Bernard's basement, we should
        # return the same text:
        # Bernard stopped you going in the basement.
        completions = TerminalMkdirEleanor.autocomplete_files(
            self, text, line, begidx, endidx, only_dirs,
            only_exe
        )
        if "photocopier.sh" in completions:
            print "\n" + bernard_text
            return []
        else:
            return completions


class TerminalNanoBernard(TerminalNanoEleanor):

    def block_command(self):
        if "basement" in self.last_user_input and \
                (
                    "ls" in self.last_user_input or
                    "cat" in self.last_user_input
                ):
            print bernard_text
            return True
        else:
            return TerminalNanoEleanor.block_command(self)

    def autocomplete_files(self, text, line, begidx, endidx, only_dirs=False, only_exe=False):
        completions = TerminalNanoEleanor.autocomplete_files(
            self, text, line, begidx, endidx, only_dirs,
            only_exe
        )
        if "photocopier.sh" in completions:
            print "\n" + bernard_text
            return []
        else:
            return completions
