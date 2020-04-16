from .DeployJob import DeployJob
from .CompileJob import CompileJob
from .SetupJob import SetupJob

from .Profile import Profile


class JobFactory:
    _is_setup = False
    _is_compile = False
    _is_deploy = False

    def __init__(self):
        return

    def create(self, section, config):
        print(section)

        if section is None:
            return None
        elif section == "setup":
            print('create setup job')
            self._is_setup = True
            return SetupJob(config)
        elif section == "deploy":
            print('create deploy job')
            self._is_deploy = True
            return DeployJob(config)
        else:
            print('create compile job')
            self._is_compile = True
            return CompileJob(section, config)

    def is_fine(self):
        if self._is_setup is False:
            print('setup section missing in profile')
        if self._is_compile is False:
            print('compile section missing in profile')
        if self._is_deploy is False:
            print('deploy section missing in profile')

        return self._is_setup and self._is_compile and self._is_deploy