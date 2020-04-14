
from .SetupJob import SetupJob
from .DeployJob import DeployJob
from .CompileJob import CompileJob

from .Profile import Profile

class JobFactory:
    _is_setup = False
    _is_compile = False
    _is_deploy = False

    def __init__(self):
        return

    def create(self, profile):
        print(profile.section)

        if profile.section is None:
            return None
        elif profile.section == "setup":
            print('create setup job')
            self._is_setup = True
            return SetupJob()
        elif profile.section == "deploy":
            print('create deploy job')
            self._is_deploy = True
            return DeployJob()
        else:
            print('create compile job')
            self._is_compile = True
            return CompileJob()

    def isFine(self):
        if self._is_setup is False:
            print('setup section missing in profile')
        if self._is_compile is False:
            print('compile section missing in profile')
        if self._is_deploy is False:
            print('deploy section missing in profile')

        return self._is_setup and self._is_compile and self._is_deploy