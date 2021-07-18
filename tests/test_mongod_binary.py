"""Test pytest_motor.mongod_binary."""
import tempfile
from pathlib import Path

from pytest import MonkeyPatch, mark, param

from pytest_motor.mongod_binary import MongodBinary

# Archives imitate direcotry structure of real ones
# but do NOT contain real mongod binaries
# P.S. Linux and MacOS structure is the same
MONGODB_MACOS_TAR = Path(__file__).parent.parent / "test_data" / \
    "mongodb-macos-x86_64-4.4.6.tgz"
MONGODB_WINDOWS_ZIP = Path(__file__).parent.parent / "test_data" / \
    "mongodb-windows-x86_64-4.4.6.zip"


# yapf: disable
@mark.parametrize(
    'platform_name, distro_name, distro_version, result', [
    param('Java', '', '', 'Java',
        marks=mark.xfail(raises=OSError ,strict=True)),
    param('Linux', 'ubuntu', '14.04', 'linux-x86_64-ubuntu1404',
        marks=mark.xfail(raises=OSError ,strict=True)),
    ('Linux', 'ubuntu', '16.04', 'linux-x86_64-ubuntu1604'),
    ('Linux', 'ubuntu', '18.04', 'linux-x86_64-ubuntu1804'),
    ('Linux', 'ubuntu', '20.04', 'linux-x86_64-ubuntu2004'),
    ('Linux', 'ubuntu', '19.04', 'linux-x86_64-ubuntu1804'),
    param('Linux', 'Debian', '8.0', 'linux-x86_64-debian80',
        marks=mark.xfail(raises=OSError ,strict=True)),
    ('Linux', 'debian', '9.2', 'linux-x86_64-debian92'),
    ('Linux', 'debian', '10.0', 'linux-x86_64-debian10'),
    ('Linux', 'debian', '9.0', 'linux-x86_64-debian92'),
    param('Linux', 'opensuse', '8.0', 'linux-x86_64-opensuse80',
        marks=mark.xfail(raises=OSError ,strict=True)),
    ('Darwin', '', '', 'macos-x86_64'),
    ('Windows', '', '', 'windows-x86_64'),
    ]
)
@mark.filterwarnings("ignore::Warning")
def test_mongo_platform(monkeypatch: MonkeyPatch,
                        platform_name: str,
                        distro_name: str,
                        distro_version: str,
                        result: str) -> None:
    # yapf: enable
    """Test mongodb platform selection."""

    path = Path(tempfile.gettempdir())

    monkeypatch.setattr("platform.system", lambda: platform_name)
    monkeypatch.setattr("distro.id", lambda: distro_name)
    monkeypatch.setattr("distro.version", lambda: distro_version)
    monkeypatch.setattr("distro.major_version", lambda: distro_version.split('.')[0])
    assert MongodBinary(path).current_platform == result


# yapf: disable
@mark.parametrize(
    'platform_name, distro_name, distro_version, true_url', [
    ('Darwin', '', '',
        "https://fastdl.mongodb.org/osx/mongodb-macos-x86_64-4.4.6.tgz"),
    ('Linux', 'ubuntu', '18.04',
        "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-ubuntu1804-4.4.6.tgz"),
    ('Windows', '', '',
        "https://fastdl.mongodb.org/windows/mongodb-windows-x86_64-4.4.6.zip")
    ]
)
def test_mongod_url(monkeypatch: MonkeyPatch,
                    platform_name: str,
                    distro_name: str,
                    distro_version: str,
                    true_url: str) -> None:
    # yapf: enable
    """Test mongo version based on platform system."""
    monkeypatch.setattr("platform.system", lambda: platform_name)
    monkeypatch.setattr("distro.id", lambda: distro_name)
    monkeypatch.setattr("distro.version", lambda: distro_version)
    monkeypatch.setattr("distro.major_version", lambda: distro_version.split('.')[0])
    assert MongodBinary(Path(tempfile.gettempdir())).url == true_url


@mark.parametrize('platform_name, archive_path', [('Darwin', MONGODB_MACOS_TAR),
                                                  ('Windows', MONGODB_WINDOWS_ZIP)])
def test_unpack(monkeypatch: MonkeyPatch, platform_name: str, archive_path: Path) -> None:
    """Test unpacking mechanism based on archive format."""

    directory: Path = Path(tempfile.gettempdir())

    monkeypatch.setattr("platform.system", lambda: platform_name)
    binary_test = MongodBinary(directory)
    mongod_path = directory / binary_test.binary_name
    with open(archive_path, 'rb') as test_file:
        # pylint: disable=protected-access
        binary_test._MongodBinary__unpack(test_file)  # type: ignore[attr-defined]
    assert mongod_path.exists()
    mongod_path.unlink()
