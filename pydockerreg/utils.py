import click
import argparse
from argparse import SUPPRESS
from functools import wraps

from .exceptions import BadArgException


def classof(method):
    """get class of a bounded method"""

    return method.__self__.__class__


def gather_opts(cls):
    cls._opts_container = {}
    for name, method in cls.__dict__.items():
        if hasattr(method, "opts"):
            cls._opts_container[name] = method.opts
            if name == "cd":
                cls._opts_container[name]["opts"].append("..")
    return cls


class HelpAction(argparse.Action):
    """HelpAction, when -h is called, print help message and do not exit"""

    def __init__(self, option_strings,
                 dest=SUPPRESS, default=SUPPRESS, help=None):

            super(HelpAction, self).__init__(
                option_strings=option_strings,
                dest=dest,
                default=default,
                nargs=0,
                help=help)

    def __call__(self, parser, args, values, option_string=None):
        parser.print_help()
        raise BadArgException()


class MyParser(argparse.ArgumentParser):
    def error(self, msg):
        click.echo("error: {}".format(msg))
        self.print_help()
        raise BadArgException()


def opts_manipulator(func, *args, **kwargs):
    prog = func.__name__

    parser = getattr(func, "parser", None)
    if parser is None:
        parser = MyParser(description=func.__doc__,
                          add_help=False,
                          prog=prog)
        parser.add_argument("-h", "--help",
                            default=SUPPRESS,
                            action=HelpAction,
                            help="show this help message")
        func.parser = parser
        func.opts = {"opts": ["-h", "--help"],
                     "args": []}
    if args or kwargs:
        parser.add_argument(*args, **kwargs)
        # gather options start with -
        if args[0].startswith("-"):
            func.opts["opts"].extend(args)
        # gather arguments
        else:
            func.opts['args'].extend(args)


def opt_manager(*args, **kwargs):
    """ function decorator to add options for a command.

    opt_manage accepts same arguments with argparse.add_argument. Internally,
    it just pass all parameters to add_argument. With this decorator, in the
    method body, you can access all arguments using `self.args`

    eg:
    ```
        @opt_manager("name", help="name to display")
        def foo(self):
            print(self.args.name)
    ```

    This decorator also injects all the options into
    `func.__self__.__class__.opts_container`. it is mainly used for completion
    """

    def inner(func):

        opts_manipulator(func, *args, **kwargs)

        @wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                self.args = func.parser.parse_args()
            except BadArgException:
                return
            return func(self, *args, **kwargs)

        wrapper.parser = func.parser
        return wrapper
    return inner



def set_completer_var(name):
    """
    make the function result cached in class varaible so it can be used for
    completion
    """
    def inner(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            if not hasattr(self.__class__, "_completer_vars"):
                self.__class__._completer_vars = {}
            completer_vars = self.__class__._completer_vars
            completer_vars[name] = result
            return result
        return wrapper
    return inner
