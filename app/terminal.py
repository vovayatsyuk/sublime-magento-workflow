import subprocess


class Terminal:
    def __init__(self, workdir):
        self.workdir = workdir

    def run(self, cmd):
        if self.workdir is None:
            return

        print('[MagentoWorkflow] {} [dir:{}]'.format(cmd, self.workdir))

        return subprocess.check_output(
            cmd,
            shell=True,
            cwd=self.workdir,
            stderr=subprocess.STDOUT
        )
