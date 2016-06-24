import sys
import click
import shlex
from abc import ABCMeta, abstractmethod
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit import prompt
from pygments.token import Token
from pygments.style import Style
from pygments.styles.default import DefaultStyle
from .completion import OptLiveCompleter

class DocumentStyle(Style):
    styles = {
        Token.Menu.Completions.Completion.Current: 'bg:#00aaaa #000000',
        Token.Menu.Completions.Completion: 'bg:#008888 #ffffff',
        Token.Menu.Completions.ProgressButton: 'bg:#003333',
        Token.Menu.Completions.ProgressBar: 'bg:#00aaaa',
    }
    styles.update(DefaultStyle.styles)


class Base(object):

    __metaclass__ = ABCMeta

    def __init__(self, session):
        self.session = session

    def commands(self):
        opts = list(self.__class__._opts_container.keys())
        opts.append("help")
        return opts

    @abstractmethod
    def get_prompt(self):
        pass

    def help(self):
        click.echo(" ".join(self.commands()))

    def get_completer(self):
        opts = self.__class__._opts_container
        # this value can change dynamically
        completer_vars = getattr(self.__class__, "_completer_vars", {})
        completer = OptLiveCompleter(opts, completer_vars)
        return completer

    def validate_cmd(self, cmd, commands):
        # manipulate sys.argv so click can read
        sys.argv = shlex.split(cmd)
        if sys.argv[0] in commands:
            return sys.argv[0]

    def run(self):
        if not self.exists():
            return
        history = InMemoryHistory()
        commands = self.commands()
        my_prompt = self.get_prompt()
        if 'help' not in commands:
            commands.append("help")

        while True:
            try:
                command_to_run = prompt(my_prompt,
                                        history=history,
                                        style=DocumentStyle,
                                        completer=self.get_completer())
                if not command_to_run: continue
                if command_to_run in ["cd ..", "exit"]: break
                command_to_run = self.validate_cmd(command_to_run, commands)

                if not command_to_run:
                    click.echo("No such command")
                    continue

                cmd = getattr(self, command_to_run, None)
                if cmd is None:
                    click.echo("No such command")
                    continue
                cmd()

            except EOFError:
                break
            except KeyboardInterrupt:
                # ignore ctrl-c
                click.echo("KeyboardInterrupt")
                continue
            except Exception as e:
                click.echo(str(e))
                continue

    def exists(self):
        """This function will make sure run is called if return True"""
        return True
