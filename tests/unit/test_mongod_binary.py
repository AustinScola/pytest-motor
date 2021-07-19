"""Test pytest_motor.mongod_binary."""
import tarfile
import tempfile
from io import BytesIO
from pathlib import Path
from typing import IO, Iterator
from zipfile import ZIP_DEFLATED, ZipFile

from pytest import MonkeyPatch, fixture, mark, param
from pytest_lazyfixture import lazy_fixture
import pytest

from pytest_motor.mongod_binary import MongodBinary

pytestmark = pytest.mark.unit


@fixture(scope='session')
def mongodb_archive_windows() -> Iterator[IO]:
    """Yield a .zip archive with mongod located as in original Windows archive."""
    with tempfile.TemporaryDirectory() as tmpdir:
        myfile = Path(tmpdir) / "mongod.zip"
        with ZipFile(file=myfile, mode='w') as archive_zip:
            archive_zip.writestr("mongodb-win32-x86_64-windows-4.4.6/bin/mongod.exe", 'hello',
                                 ZIP_DEFLATED)
        yield myfile.open('rb')


@fixture(scope='session')
def mongodb_archive_macos() -> Iterator[IO]:
    """Yield a .tgz archive with mongod located as in original macOS archive."""
    with tempfile.TemporaryDirectory() as tmpdir:
        myfile = Path(tmpdir) / "mongod.tgz"
        with tarfile.open(myfile, mode="w:gz") as archive_tar:
            info = tarfile.TarInfo(name="mongodb-macos-x86_64-4.4.6/bin/mongod")
            archive_tar.addfile(info, BytesIO(b'hello'))
        yield myfile.open('rb')


@mark.parametrize('platform_name, distro_name, distro_version, result', [
    param('Java', '', '', 'Java', marks=mark.xfail(raises=OSError, strict=True)),
    param('Linux',
          'ubuntu',
          '14.04',
          'linux-x86_64-ubuntu1404',
          marks=mark.xfail(raises=OSError, strict=True)),
    ('Linux', 'ubuntu', '16.04', 'linux-x86_64-ubuntu1604'),
    ('Linux', 'ubuntu', '18.04', 'linux-x86_64-ubuntu1804'),
    ('Linux', 'ubuntu', '20.04', 'linux-x86_64-ubuntu2004'),
    ('Linux', 'ubuntu', '19.04', 'linux-x86_64-ubuntu1804'),
    param('Linux',
          'Debian',
          '8.0',
          'linux-x86_64-debian80',
          marks=mark.xfail(raises=OSError, strict=True)),
    ('Linux', 'debian', '9.2', 'linux-x86_64-debian92'),
    ('Linux', 'debian', '10.0', 'linux-x86_64-debian10'),
    ('Linux', 'debian', '9.0', 'linux-x86_64-debian92'),
    param('Linux',
          'opensuse',
          '8.0',
          'linux-x86_64-opensuse80',
          marks=mark.xfail(raises=OSError, strict=True)),
    ('Darwin', '', '', 'macos-x86_64'),
    ('Windows', '', '', 'windows-x86_64'),
])
@mark.filterwarnings("ignore::Warning")
def test_mongo_platform(monkeypatch: MonkeyPatch, platform_name: str, distro_name: str,
                        distro_version: str, result: str) -> None:
    """Test mongodb platform selection."""

    monkeypatch.setattr("platform.system", lambda: platform_name)
    monkeypatch.setattr("distro.id", lambda: distro_name)
    monkeypatch.setattr("distro.version", lambda: distro_version)
    monkeypatch.setattr("distro.major_version", lambda: distro_version.split('.')[0])
    assert MongodBinary(Path(tempfile.gettempdir())).current_platform == result


@mark.parametrize(
    'platform_name, distro_name, distro_version, true_url',
    [('Darwin', '', '', "https://fastdl.mongodb.org/osx/mongodb-macos-x86_64-4.4.6.tgz"),
     ('Linux', 'ubuntu', '18.04',
      "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-ubuntu1804-4.4.6.tgz"),
     ('Windows', '', '', "https://fastdl.mongodb.org/windows/mongodb-windows-x86_64-4.4.6.zip")])
def test_mongod_url(monkeypatch: MonkeyPatch, platform_name: str, distro_name: str,
                    distro_version: str, true_url: str) -> None:
    """Test mongo version based on platform system."""
    monkeypatch.setattr("platform.system", lambda: platform_name)
    monkeypatch.setattr("distro.id", lambda: distro_name)
    monkeypatch.setattr("distro.version", lambda: distro_version)
    monkeypatch.setattr("distro.major_version", lambda: distro_version.split('.')[0])
    assert MongodBinary(Path(tempfile.gettempdir())).url == true_url


@mark.parametrize('platform_name, archive', [('Darwin', lazy_fixture('mongodb_archive_macos')),
                                             ('Windows', lazy_fixture('mongodb_archive_windows'))])
def test_unpack(monkeypatch: MonkeyPatch, platform_name: str, archive: IO[bytes]) -> None:
    """Test unpacking mechanism based on archive format."""

    directory: Path = Path(tempfile.gettempdir())

    monkeypatch.setattr("platform.system", lambda: platform_name)
    binary_test = MongodBinary(directory)
    mongod_path = directory / binary_test.binary_name
    # pylint: disable=protected-access
    binary_test._MongodBinary__unpack(archive)  # type: ignore[attr-defined]
    assert mongod_path.exists()
    mongod_path.unlink()
