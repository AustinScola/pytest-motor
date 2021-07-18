"""Test pytest_motor.mongod_binary."""
import tempfile
from pathlib import Path

from pytest import MonkeyPatch, mark, raises

from pytest_motor.mongod_binary import MongodBinary

# Archives imitate direcotry structure of real ones
# but do NOT contain real mongod binaries
# P.S. Linux and MacOS structure is the same
MONGODB_MACOS_TAR = Path(__file__).parent.parent / "test_data" / \
    "mongodb-macos-x86_64-4.4.6.tgz"
MONGODB_WINDOWS_ZIP = Path(__file__).parent.parent / "test_data" / \
    "mongodb-windows-x86_64-4.4.6.zip"


@mark.filterwarnings("ignore::Warning")
def test_mongo_platform(monkeypatch: MonkeyPatch) -> None:
    """Test mongodb platform selection."""

    # UNSUPPORTED OS

    monkeypatch.setattr("platform.system", lambda: "Java")
    with raises(OSError) as excinfo:
        MongodBinary.mongo_running_os()
    assert "Your platform is unsupported." in str(excinfo.value)

    # LINUX DISTROS

    monkeypatch.setattr("platform.system", lambda: "Linux")

    # UBUNTU

    monkeypatch.setattr("distro.id", lambda: "ubuntu")

    monkeypatch.setattr("distro.major_version", lambda: "14")
    with raises(OSError) as excinfo:
        MongodBinary.mongo_platform()
    assert "Your Ubuntu version is too old. Upgrade at least to 16." in str(excinfo.value)

    monkeypatch.setattr("distro.version", lambda: "16.04")
    monkeypatch.setattr("distro.major_version", lambda: "16")
    assert MongodBinary.mongo_platform() == 'linux-x86_64-ubuntu1604'

    monkeypatch.setattr("distro.version", lambda: "18.04")
    monkeypatch.setattr("distro.major_version", lambda: "18")
    assert MongodBinary.mongo_platform() == 'linux-x86_64-ubuntu1804'

    monkeypatch.setattr("distro.version", lambda: "20.04")
    monkeypatch.setattr("distro.major_version", lambda: "20")
    assert MongodBinary.mongo_platform() == 'linux-x86_64-ubuntu2004'

    monkeypatch.setattr("distro.version", lambda: "19.10")
    monkeypatch.setattr("distro.major_version", lambda: "19")
    assert MongodBinary.mongo_platform() == 'linux-x86_64-ubuntu1804'

    # DEBIAN

    monkeypatch.setattr("distro.id", lambda: "debian")

    monkeypatch.setattr("distro.major_version", lambda: "8")
    with raises(OSError) as excinfo:
        MongodBinary.mongo_platform()
    assert "Your Debian version is too old. Upgrade at least to 9." in str(excinfo.value)

    monkeypatch.setattr("distro.version", lambda: "9.2")
    monkeypatch.setattr("distro.major_version", lambda: "9")
    assert MongodBinary.mongo_platform() == 'linux-x86_64-debian92'

    monkeypatch.setattr("distro.version", lambda: "10.0")
    monkeypatch.setattr("distro.major_version", lambda: "10")
    assert MongodBinary.mongo_platform() == 'linux-x86_64-debian10'

    monkeypatch.setattr("distro.version", lambda: "9.0")
    monkeypatch.setattr("distro.major_version", lambda: "9")
    assert MongodBinary.mongo_platform() == 'linux-x86_64-debian92'

    # UNSUPPORTED DISTROS

    monkeypatch.setattr("distro.id", lambda: "opensuse")
    with raises(OSError) as excinfo:
        MongodBinary.mongo_platform()
    assert "Your distro (opensuse) is unsupported." in str(excinfo.value)

    # MACOS

    monkeypatch.setattr("platform.system", lambda: "Darwin")
    assert MongodBinary.mongo_platform() == 'macos-x86_64'

    # WINDOWS

    monkeypatch.setattr("platform.system", lambda: "Windows")
    assert MongodBinary.mongo_platform() == 'windows-x86_64'


def test_mongod_url(monkeypatch: MonkeyPatch) -> None:
    """Test mongo version based on platform system."""
    monkeypatch.setattr("platform.system", lambda: "Darwin")
    assert MongodBinary(Path(__file__).parent).url == \
        "https://fastdl.mongodb.org/osx/mongodb-macos-x86_64-4.4.6.tgz"

    monkeypatch.setattr("platform.system", lambda: "Linux")
    monkeypatch.setattr("distro.id", lambda: "ubuntu")
    monkeypatch.setattr("distro.version", lambda: "18.04")
    monkeypatch.setattr("distro.major_version", lambda: "18")
    assert MongodBinary(Path(__file__).parent).url == \
        "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-ubuntu1804-4.4.6.tgz"

    monkeypatch.setattr("platform.system", lambda: "Windows")
    assert MongodBinary(Path(__file__).parent).url == \
        "https://fastdl.mongodb.org/windows/mongodb-windows-x86_64-4.4.6.zip"


def test_unpack(monkeypatch: MonkeyPatch) -> None:
    """Test unpacking mechanism based on archive format."""
    # pylint: disable=protected-access
    directory: Path = Path(tempfile.gettempdir())

    monkeypatch.setattr("platform.system", lambda: "Darwin")
    binary_test = MongodBinary(directory)
    assert binary_test.url.endswith('.tgz')
    mongod_path = directory / "mongod"
    with open(MONGODB_MACOS_TAR, 'rb') as test_file:
        binary_test._MongodBinary__unpack(test_file)
    assert mongod_path.exists()
    mongod_path.unlink()

    monkeypatch.setattr("platform.system", lambda: "Windows")
    binary_test = MongodBinary(directory)
    assert binary_test.url.endswith('.zip')
    mongod_path = directory / "mongod.exe"
    with open(MONGODB_WINDOWS_ZIP, 'rb') as test_file:
        binary_test._MongodBinary__unpack(test_file)
    assert mongod_path.exists()
    mongod_path.unlink()
    # pylint: enable=protected-access
