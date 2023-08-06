from .package_docker import PackageDocker
from .package_python import PackagePython
from ..model.build_pack import BuildPack
from ..util import DefinitionException


def package(build_dir, build_pack: BuildPack):
    if build_pack.type == "python":
        package = PackagePython(build_dir, build_pack)
    elif build_pack.type == "docker":
        package = PackageDocker(build_dir, build_pack)
    else:
        raise DefinitionException(f"{build_pack.type} not supported.")
    package.clean()
    package.package()
    return package.build_path
