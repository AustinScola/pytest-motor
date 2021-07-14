"""Test pytest_motor.plugin."""
from pathlib import Path

from pytest import Testdir


def test_motor_client(testdir: Testdir) -> None:
    """Test pytest_motor.plugin.motor_client."""
    testdir.makeconftest("""
    pytest_plugins=["pytest_asyncio", "pytest_motor.plugin"]
    """)

    test_files_directory = Path(__file__).parent.parent / 'test_data' / 'files'
    not_init_file = lambda path: path.name != '__init__.py'
    test_files = filter(not_init_file, test_files_directory.glob('*.py'))

    for test_file in test_files:
        testdir.makepyfile(test_file.read_text())

    result = testdir.runpytest()

    result.assert_outcomes(passed=2)
