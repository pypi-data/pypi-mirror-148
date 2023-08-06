import logging
from pathlib import Path

from .base_package import BasePackage
from ..util import create_file_from_content

logger = logging.getLogger()


class PackageDocker(BasePackage):
    def package(self):
        if Path(self.build_pack.docker.file_name).is_file() is False or self.build_pack.docker.overwrite:
            create_file_from_content(self.build_pack.docker.file_name,
                                     self.build_pack.docker.docker_file_content)
        super().package()
