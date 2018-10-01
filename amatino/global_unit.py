"""
Amatino API Python Bindings
Global Unit Module
Author: hugh@amatino.io
"""
from amatino.session import Session
from amatino.denomination import Denomination
from typing import TypeVar

T = TypeVar('T', bound='GlobalUnit')


class GlobalUnit(Denomination):
    """
    Global Units are standardised units of account available across
    all Amatino Entities. For example, many major currencies are available
    as Global Units.

    Global Units cannot be modified by Amatino users.
    """
    def __init__(
        self,
        session: Session,
        code: str,
        id_: int,
        name: str
    ) -> None:

        assert isinstance(session, Session)
        self._session = session
        super().__init__(code, id_, name)

        return

    @classmethod
    def retrieve(self, id_: int) -> T:
        raise NotImplementedError
