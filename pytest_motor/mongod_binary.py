"""This module helps with mongodb binary."""
import platform
import shutil
import tarfile
import tempfile
import warnings
from pathlib import Path
from zipfile import ZipFile

import aiohttp
import distro


class MongodBinary:
    """This class helps with mongodb binary."""
    MONGO_VERSION: str = '4.4.6'  # FUTURE: mongod binary version selector via config

    def __init__(self, destination: Path):
        destination.mkdir(parents=True, exist_ok=True)
        self.path: Path = destination / f'mongod{".exe" if platform.system() == "Windows" else ""}'
        self.url: str = f'https://fastdl.mongodb.org/' \
                        f'{self.mongo_running_os()}/' \
                        f'mongodb-{self.mongo_platform()}-' \
                        f'{self.MONGO_VERSION}.' \
                        f'{"zip" if platform.system() == "Windows" else "tgz"}'

    async def download_and_unpack(self) -> Path:
        """Return path to downloaded and unpacked mongod binary."""
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url) as resp:
                with tempfile.TemporaryFile(mode='w+b') as binary_file:
                    # Read by chunks to avoid big RAM consumption
                    while True:
                        # read by 100 bytes
                        chunk = await resp.content.read(100)
                        if not chunk:
                            break
                        binary_file.write(chunk)
                    binary_file.flush()
                    binary_file.seek(0)
                    self.__unpack(binary_file)
                    return self.path

    def __unpack(self, binary_file: tempfile.TemporaryFile):
        """Unpack mongod binary from zip or tar."""
        # pylint: disable=consider-using-with
        if str(self.url).endswith('.tgz'):
            with tarfile.open(fileobj=binary_file) as archive:
                file_in_archive = archive.extractfile(
                    f'mongodb-{self.mongo_platform()}-{self.MONGO_VERSION}/bin/mongod')
                file_outside = self.path.open(mode="wb")
                with file_in_archive, file_outside:
                    shutil.copyfileobj(file_in_archive, file_outside)
                self.path.chmod(0o777)
            assert self.path.exists(), "Unsuccessful mongod binary extraction"
        elif str(self.url).endswith('.zip') and self.mongo_platform() == 'windows-x86_64':
            with ZipFile(file=binary_file) as archive:
                file_in_archive = archive.open(
                    f'mongodb-win32-x86_64-windows-{self.MONGO_VERSION}/bin/mongod.exe')
                file_outside = self.path.open(mode="wb")
                with file_in_archive, file_outside:
                    shutil.copyfileobj(file_in_archive, file_outside)
                self.path.chmod(0o777)
            assert self.path.exists(), "Unsuccessful mongod binary extraction"
        # pylint: enable=consider-using-with
        else:
            raise Exception("Unsupported archive format.")  # pragma: no cover

    @staticmethod
    def mongo_running_os() -> str:
        """Return OS as it spells in mongodb binary url."""
        system: str = platform.system()
        if system == 'Linux':
            return 'linux'
        if system == 'Darwin':
            return 'osx'
        if system == 'Windows':
            return 'windows'
        raise OSError("Your platform is unsupported.")

    @staticmethod
    def mongo_platform() -> str:
        """Return mongo platform as it spells in mongodb binary url."""
        # FUTURE: ARM support
        system = platform.system()
        if system == 'Linux':
            distro_name = distro.id()
            if distro_name == 'ubuntu':
                return 'linux-x86_64-' + MongodBinary.__select_ubuntu_version()
            if distro_name == 'debian':
                return 'linux-x86_64-' + MongodBinary.__select_debian_version()
            # FUTURE: distros that may be added: Amazon Linux, CentOS, SUSE
            raise OSError(f"Your distro ({distro_name}) is unsupported.")

        if system == 'Darwin':
            return 'macos-x86_64'

        if system == 'Windows':
            return 'windows-x86_64'

        raise OSError("Your platform is unsupported.")  # pragma: no cover

    @staticmethod
    def __select_ubuntu_version() -> str:
        if bool(distro.major_version()) and int(distro.major_version()) < 16:
            raise OSError("Your Ubuntu version is too old. Upgrade at least to 16.")

        if distro.version() == '16.04':
            warnings.warn("Your OS support was NOT properly tested.")
            return 'ubuntu1604'
        if distro.version() == '18.04':
            return 'ubuntu1804'
        if distro.version() == '20.04':
            return 'ubuntu2004'

        warnings.warn("Can't detect your Ubuntu version. Fallback to 18.04.")
        return 'ubuntu1804'

    @staticmethod
    def __select_debian_version() -> str:
        if bool(distro.major_version()) and int(distro.major_version()) < 9:
            raise OSError("Your Debian version is too old. Upgrade at least to 9.")

        if distro.version() == '9.2':
            warnings.warn("Your OS support was NOT properly tested.")
            return 'debian92'
        if distro.version() == '10.0':
            warnings.warn("Your OS support was NOT properly tested.")
            return 'debian10'

        warnings.warn("Can't detect your Debian version. Fallback to 9.2.")
        return 'debian92'
