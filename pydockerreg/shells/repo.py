import json
import click
from tabulate import tabulate
from .base import Base
from ..utils import opt_manager, gather_opts, set_completer_var
from .tag import Tag


@gather_opts
class Repo(Base):

    def __init__(self, session, repo):
        self.repo = repo
        super(Repo, self).__init__(session)

    @opt_manager()
    def ls(self):
        """ show all tags for this repo """
        tags = self.get_tags(self.repo) or []
        details = []
        for i in tags:
            details.append(
                self.filte_details(
                    self.get_tag_detail(self.repo, i),
                    limit=20))
        headers = ["tag", "name", "id", "author", "docker version"]
        click.echo(tabulate(details, headers=headers))

    @opt_manager("tag", help="repo tag to cd into")
    def cd(self):
        """ cd into a tagged repo and check."""
        self.get_digest(self.repo, self.args.tag)
        t = Tag(self.session, self.repo, self.args.tag)
        t.run()

    def get_prompt(self):
        return self.repo + "> "

    @opt_manager("tag", help="image with tag to delete")
    def rm(self):
        """remove/delete a image by tag"""
        digest = self.get_digest(self.repo, self.args.tag)
        res = self.delete_image(self.repo, digest)
        if res.status_code != 202:
            raise Exception(
                "Deletion failed, server returned {}\n{}".format(
                    res.status_code,
                    res.text))
        else:
            click.echo("Image deleted")

    @set_completer_var("tag")
    def get_tags(self, repo):
        res = self.session.get("{}/tags/list".format(repo))
        if res.status_code != 200:
            raise Exception(
                "Can not find any tags, server returned {}".format(res.status_code))
        tags = res.json()['tags']
        return tags

    def delete_image(self, image, digest):
        res = self.session.delete("{}/manifests/{}".format(image, digest))
        return res

    def get_digest(self, repo, tag):
        res = self.session.head("{}/manifests/{}".format(repo, tag))
        if res.status_code != 200:
            raise Exception(
                "Can not find digest, server returned {}".format(res.status_code))
        else:
            return res.headers["Docker-Content-Digest"]

    def get_tag_detail(self, repo, tag):
        res = self.session.get("{}/manifests/{}".format(repo, tag))
        if res.status_code != 200:
            raise Exception(
                "Can not find tag {}, server returned {}".format(tag, res.status_code))
        return res.json()

    def filte_details(self, detail, limit=200):
        x = [detail.get(i, "")[:limit] for i in ["tag", "name"]]

        his = json.loads(detail["history"][0]["v1Compatibility"])
        x.extend([his.get(i, "")[:limit] for i in ["id", "author", "docker_version"]])
        return x

    @opt_manager("tag", help="cat tag to see details")
    def cat(self):
        tag = self.args.tag
        detail = self.filte_details(self.get_tag_detail(self.repo, tag))
        headers = ["tag", "name", "id", "author", "docker version"]
        click.echo(tabulate(zip(headers, detail)))
