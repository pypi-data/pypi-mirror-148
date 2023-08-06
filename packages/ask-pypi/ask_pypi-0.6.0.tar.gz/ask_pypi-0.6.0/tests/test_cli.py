import os
import sys
import pytest
from typing import Callable
from abc import ABC, abstractmethod


class AbstractCLIResult(ABC):

    @property
    @abstractmethod
    def exit_code(self) -> int:
        raise NotImplementedError

    @property
    @abstractmethod
    def stdout(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def stderr(self) -> str:
        raise NotImplementedError


# HELPERS
@pytest.fixture
def get_cli_invocation():
    import subprocess
    class CLIResult(AbstractCLIResult):
        exit_code: int
        stdout: str
        stderr: str
        def __init__(self, completed_process: subprocess.CompletedProcess):
            self._exit_code = int(completed_process.returncode)
            self._stdout = str(completed_process.stdout)
            self._stderr = str(completed_process.stderr)
        @property
        def exit_code(self) -> int:
            return self._exit_code
        @property
        def stdout(self) -> str:
            return self._stdout
        @property
        def stderr(self) -> str:
            return self._stderr
    def get_callable(executable: str, *args, **kwargs) -> Callable[[], AbstractCLIResult]:
        def _callable() -> AbstractCLIResult:
            completed_process = subprocess.run(
                [executable] + list(args),
                env=kwargs.get('env', {}),
            )
            return CLIResult(completed_process)
        return _callable
    
    return get_callable



def test_existing_package(get_cli_invocation):
    result = get_cli_invocation(
        os.path.join(os.path.dirname(sys.executable), 'is-pypi-package'),
        'so-magic',
        )()
    assert result.exit_code == 0
    assert result.stdout == 'None'
    assert result.stderr == 'None'


def test_non_existing_package(get_cli_invocation):
    result = get_cli_invocation(
        os.path.join(os.path.dirname(sys.executable), 'is-pypi-package'),
        'asbelfiuhbyywbefobaosf98234',
        )()
    assert result.exit_code == 1
    assert result.stdout == 'None'
    assert result.stderr == 'None'
