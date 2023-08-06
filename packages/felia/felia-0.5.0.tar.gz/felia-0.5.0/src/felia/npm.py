from ._internal import SubCommand, RootCommand, parameter

__all__ = ["npm",
           "npm_run",
           "npm_install",
           ]


class Npm(RootCommand):
    """https://docs.npmjs.com/about-npm"""
    globals = globals()


class Install(SubCommand):
    """https://docs.npmjs.com/cli/v8/commands/npm-install

    在中国地区使用官方源时, 下载速度会比较慢, 可以使用cnpm代替。
    """

    @parameter()
    def registry(self):
        """指定下载源"""

    @parameter(short="-g", long="--global")
    def _global(self):
        """全局安装"""

    def cnpm(self, *args):
        """https://github.com/cnpm/cnpm/issues/361

        https://registry.npmmirror.com
        """
        return self.registry("https://registry.npmmirror.com").execute(*args)


@Npm.subcommand
class Run(SubCommand):
    """https://docs.npmjs.com/cli/v8/commands/npm-run-script"""


npm = Npm()
npm_run: Run = getattr(npm, "run")
npm_install: Install = getattr(npm, "install")