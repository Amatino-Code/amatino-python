"""
Amatino API Python Bindings
Test Module
Author: hugh@amatino.io

Base class for tests or, when executed as __main__, the entrypoint for the test
sequence.
"""
from typing import Optional
from typing import Any
from os import environ
import traceback


class Test:
    """
    Abstract class offering base-level functionality to tests.
    """
    def __init__(self, test_name: str) -> None:

        if not isinstance(test_name, str):
            raise TypeError('test_name must be of type `str`')

        raw_user_id: Optional[str] = environ['AMATINO_TEST_USER_ID']
        email: Optional[str] = environ['AMATINO_TEST_EMAIL']
        secret: Optional[str] = environ['AMATINO_TEST_SECRET']

        if raw_user_id is None:
            raise RuntimeError('AMATINO_TEST_USER_ID env variable required')

        try:
            user_id = int(raw_user_id)
        except Exception as error:
            raise RuntimeError('AMATINO_TEST_USER_ID string must hold integer')

        if email is None:
            raise RuntimeError('AMATINO_TEST_EMAIL env variable required')

        if secret is None:
            raise RuntimeError('AMATINO_TEST_SECRET env variable required')

        self.user_id: int = user_id
        self.email: str = email
        self.secret: str = secret

        self._name = test_name
        self._note: Optional[Any] = None
        self._passed: Optional[bool] = None

        return

    def execute(self) -> None:
        """
        Run this test, recording a fail() or pass() for all possible execution
        paths such that pass or fail result is recorded at test conclusion.
        """
        raise NotImplementedError

    def record_success(self, note: str = None) -> None:
        """
        Assert that the test has finished and its conditions were met
        """
        self._record_result(True, note)
        return

    def record_failure(self, note: Optional[Any] = None) -> None:
        """
        Assert that the test has finished and its conditions were not met
        """
        self._record_result(False, note)
        return

    def _record_result(self, result: bool, note: Optional[str]) -> None:
        """
        Record an assertion of pass or failure
        """
        assert isinstance(result, bool)

        if self._passed is not None:
            raise RuntimeError('Attempt to pass/fail a completed test')
        self._passed = result

        if isinstance(note, Exception):
            self._note = traceback.format_exc()
            return

        self._note = note

        return

    def report(self) -> str:
        """
        Return a string describing the outcome of this test.
        """
        if self._passed is None:
            raise RuntimeError('Cannot report on incomplete test')

        report = '[FAIL] '
        if self._passed:
            report = '[PASS] '
        report += self._name

        if self._note is not None:
            report += '\n       ' + str(self._note)

        return report
