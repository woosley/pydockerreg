from .base import Base
from ..utils import opt_manager, gather_opts


@gather_opts
class Tag(Base):

    def __init__(self, session, repo, tag):
        self.tag = tag
        self.repo = repo
        super(Tag, self).__init__(session)

    def get_prompt(self):
        return "{}/{}> ".format(self.repo, self.tag)

    @opt_manager()
    def detail(self):
        pass
