import logging
from pathlib import Path
import re
import pkg_resources
from pkg_resources import Requirement

from .package_docker import PackageDocker

logger = logging.getLogger()
REQUIREMENTS_TXT = 'requirements.txt'
MANAGED_MESSAGE = """
# ServicefoundryManaged
# Below this line dependencies are managed by servicefoundry.
# Any package mentioned after this will get auto updated from installed packages.
# If you install a new package, that would also be auto added.
# If you uninstall a package, u have to remove them manually.
"""

NOT_INSTALLED_MESSAGE = """
# Below package are not installed. You can safely remove these.
"""


class SfPackage:

    def __init__(self, package_name, package_version, is_installed=False):
        self.package_name = package_name
        self.package_version = package_version
        self.is_installed = is_installed

    def update_version(self, version):
        self.is_installed = True
        self.package_version = version

    def to_str(self):
        return f"{self.package_name}=={self.package_version}\n"


class PackagePython(PackageDocker):
    def package(self):
        if self.build_pack.dependency.auto_update:
            self._update_requirements_txt()
        super().package()

    def _update_requirements_txt(self):
        user_lines = []
        user_packages = set()
        sf_packages = {}
        is_managed_block = False
        if Path(REQUIREMENTS_TXT).is_file():
            with open(REQUIREMENTS_TXT) as file:
                for line in file.readlines():
                    if re.match("^\s*#\s*ServicefoundryManaged\s*$", line):
                        is_managed_block = True
                    if not is_managed_block:
                        user_lines.append(line)
                    sline = line.strip()
                    if sline.strip() != "" and re.match("^\s*#", line) is None:
                        requirement = Requirement(line)
                        package_name = requirement.key.lower()
                        if not is_managed_block:
                            user_packages.add(package_name)
                        else:
                            sf_packages[package_name] = SfPackage(package_name, requirement.specs[0][1])
        installed_packages = {d.project_name.lower(): d.version for d in pkg_resources.working_set}
        for package_name, package_version in installed_packages.items():
            if package_name not in user_packages:
                if package_name in sf_packages:
                    sf_packages[package_name].update_version(package_version)
                else:
                    sf_packages[package_name] = SfPackage(package_name, package_version, is_installed=True)
        with open(REQUIREMENTS_TXT, "w") as file:
            for line in user_lines:
                file.write(line)
            file.write(MANAGED_MESSAGE)
            for package_name, package in sorted(sf_packages.items()):
                if package.is_installed:
                    file.write(package.to_str())
            file.write(NOT_INSTALLED_MESSAGE)
            for package_name, package in sorted(sf_packages.items()):
                if not package.is_installed:
                    file.write(package.to_str())
