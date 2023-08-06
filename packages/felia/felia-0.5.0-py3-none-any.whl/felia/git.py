from ._internal import SubCommand, RootCommand, parameter


class Git(RootCommand):
    globals = globals()


@Git.subcommand
class Clone(SubCommand):
    """克隆"""


__all__ = ["git",
           "git_clone",
           ]


git = Git()
git_clone: Clone = globals().get("git_clone")