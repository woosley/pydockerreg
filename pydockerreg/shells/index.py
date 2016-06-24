import click
from six.moves.urllib_parse import urlparse

from .base import Base
from ..utils import opt_manager, gather_opts, set_completer_var

from .repo import Repo


@gather_opts
class Index(Base):
    """index commands for dockerreg"""

    def get_prompt(self):
        host = urlparse(self.session.url).netloc
        return host + "> "

    @opt_manager()
    def ls(self):
        """list all repos on the registry"""
        repos = self.repos() or []
        for i in repos:
            click.echo(i)

    @opt_manager("repo", help="repo to browse")
    def cd(self):
        """cd to the target repo"""
        if self.args.repo not in self.repos():
            click.echo("No such repo")
        else:
            Repo(self.session, self.args.repo).run()

    @set_completer_var("repo")
    def repos(self):
        """get all repos."""
        res = self.session.get("_catalog").json()['repositories']
        return res
