"""
Amatino API Python Bindings
Account Test Module
Author: hugh@amatino.io
"""
from amatino import Account
from amatino import Entity
from amatino import AMType
from amatino import GlobalUnit
from amatino.tests.primary.entity import EntityTest

USD_UNIT_ID = 5


class AccountTest(EntityTest):
    """Test the Account primary object"""

    def __init__(self, name='Create, retrieve, update Account') -> None:

        self.usd = None
        super().__init__(name)
        self.create_entity()
        if not isinstance(self.entity, Entity):
            raise RuntimeError(
                'Entity creation failed. Consider running Entity tests'
            )
        return

    def create_account(self, amt=AMType.asset, name='Test account') -> Account:

        if self.usd is None:
            self.usd = GlobalUnit.retrieve(self.session, USD_UNIT_ID)

        account = Account.create(
            self.session,
            self.entity,
            name,
            amt,
            self.usd,
            'A test Account created by the Python test suite'
        )

        self.account = account

        return account

    def execute(self) -> None:

        try:
            account = self.create_account()
        except Exception as error:
            self.record_failure(error)
            return

        assert isinstance(account, Account)

        try:
            account = Account.retrieve(
                self.session,
                self.entity,
                account.id_
            )
        except Exception as error:
            self.record_failure(error)
            return

        if account.id_ != self.account.id_:
            self.record_failure('Account IDs do not match')
            return

        new_name = 'Updated account name'

        try:
            updated_account = account.update(name=new_name)
        except Exception as error:
            self.record_failure(error)
            return

        if updated_account.name != new_name:
            self.record_failure('Account name was not updated')
            return

        self.record_success()
        return