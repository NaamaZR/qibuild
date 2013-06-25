import qidoc.project

class SphinxProject(qidoc.project.DocProject):
    """ A doc projet using Sphinx """
    def __init__(self, doc_worktree, project, name,
                 depends=None, dest=None):
        self.doc_type = "sphinx"
        super(SphinxProject, self).__init__(doc_worktree, project, name,
                                            depends=depends,
                                            dest=dest)

    def configure(self):
        pass

    def build(self):
        pass

    def install(self, destdir):
        pass
