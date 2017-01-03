from linux_story.StepTemplate import StepTemplate
from linux_story.story.new_terminals.terminal_mkdir import TerminalMkdir
from linux_story.story.new_terminals.terminal_nano import TerminalNano

bernard_text = _("Bernard stopped you looking in the basement!")


def bernard_autocomplete(completions):
    if "photocopier.sh" in completions:
        print "\n" + bernard_text
        return []
    else:
        return completions


class TerminalMkdirBernard(TerminalMkdir):
    def _autocomplete_files(self, text, line, begidx, endidx, only_dirs=False, only_exe=False):
        completions = TerminalMkdir._autocomplete_files(self, text, line, begidx, endidx, only_dirs, only_exe)
        return bernard_autocomplete(completions)


class TerminalNanoBernard(TerminalNano):
    def _autocomplete_files(self, text, line, begidx, endidx, only_dirs=False, only_exe=False):
        completions = TerminalNano._autocomplete_files(self, text, line, begidx, endidx, only_dirs, only_exe)
        return bernard_autocomplete(completions)


class StepTemplateEleanorBernard(StepTemplate):
    companion_command = "cat Eleanor"

    def check_command(self, last_user_input):
        spoke = self._companion_speaks(last_user_input)
        if not spoke:
            return self._default_check_command(last_user_input)

    def block_command(self, line):
        if "basement" in line and ("ls" in line or "cat" in line):
            print bernard_text
            return True
        else:
            return StepTemplate.block_command(self, line)


class StepTemplateMkdir(StepTemplateEleanorBernard):
    TerminalClass = TerminalMkdirBernard


class StepTemplateNano(StepTemplateEleanorBernard):
    TerminalClass = TerminalNanoBernard
