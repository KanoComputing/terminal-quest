



from linux_story.story.terminals.terminal_sudo import TerminalSudo


class StepTemplateSudo(TerminalSudo):
    challenge_number = 50


class Step1(StepTemplateSudo):
    story = [
        "You are outside the rabbithole. Look more closely at the rabbithole, and then try and go inside."
    ]
    start_dir = "~/woods/thicket"
    end_dir = "~/woods/thicket"
    dirs_to_attempt = "~/woods/thicket/rabbithole"
    needs_sudo = True

    commands = [
        "sudo cd rabbithole",
        "sudo cd rabbithole/"
    ]
    story_dict = {
        "rabbithole": {
            "path": "~/woods/thicket",
            "permissions": 0000
        }
    }


    def next(self):
        Step2()