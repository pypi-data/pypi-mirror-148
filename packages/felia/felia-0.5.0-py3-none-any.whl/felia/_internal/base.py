import logging

from .configuration import ConfMixin

logger = logging.getLogger(__name__)
h = logging.StreamHandler()
h.setFormatter(logging.Formatter("%(levelname)s $ %(message)s"))
logger.addHandler(h)
logger.setLevel(logging.INFO)


class BaseCommand:
    """
    cli.para1().para2()(run=False) # 只输出命令，不执行
    等价于
    cli --para1 --para2
    """

    def __init__(self):
        self.args = []
        self.__name__ = getattr(self, "__name__", self.__class__.__name__.lower())
        self.cmd = [self.__name__]

    def __call__(self, *args, **kwargs):
        pass

    def show_commands(self, *args):
        return self(*args)

    def clear_args(self):
        self.args.clear()

    def execute(self, *args):
        self(*args)

    def print_help(self):
        self("--help")


class RootCommand(BaseCommand, ConfMixin):
    subcommands: list
    globals: dict

    def __init__(self):
        super(RootCommand, self).__init__()
        if not hasattr(self, 'subcommands'):
            return

        while self.subcommands:
            CMD = self.subcommands.pop()
            obj = CMD(self)
            setattr(self, CMD.__name__, obj)
            obj_name = f"{self.__name__}_{getattr(CMD, '__name__', self.__name__.lower())}".lower()
            self.globals.setdefault(obj_name,
                                    obj)

            if _all := self.globals.get("__all__"):
                if obj_name not in _all:
                    _all.append(obj_name)

    def __call__(self, *args):
        _args = self.args + list(args)
        cmd = self.cmd + _args
        logger.info(" ".join(cmd))
        self.clear_args()
        return " ".join(cmd)

    @classmethod
    def subcommand(cls, sub_class):
        if not hasattr(cls, 'subcommands'):
            setattr(cls, 'subcommands', [])
        cls.subcommands.append(sub_class)
        return sub_class


class SubCommand(BaseCommand):

    def __init__(self, root):
        super(SubCommand, self).__init__()
        self.root = root

    def __call__(self, *args):
        _args = self.args + list(args)
        cmd = self.cmd + _args
        return self.root(*cmd)








