from ._internal import SubCommand, RootCommand, parameter


class Go(RootCommand):
    globals = globals()


@Go.subcommand
class Mod(SubCommand):
    """项目和包管理"""
    subcmd = "mod"

    @parameter
    def init(self):
        """在当前目录初始化"""


@Go.subcommand
class Run(SubCommand):
    """编译和运行go代码"""


go = Go()
go_run: Run = globals().get("go_run")

