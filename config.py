from dataclasses import dataclass

from datetime import datetime

from typing import Dict


STATEMENTS_DIRECTORY = 'datafiles'

OUTPUT_FILE = 'result.csv'

FIELDNAMES = ['date', 'transaction', 'amount', 'o_from', 'o_to']


@dataclass
class BankOperation:
    """
    Class for encapsulating bank operation data and mapping operations
    from difrerent banks to the unifirmed internal format.

    Mapping type methods determine the way an operation is processed.
    """
    date: str
    transaction: str
    amount: float
    o_from: str
    o_to: str

    @classmethod
    def mapping_type_1(cls, row: Dict[str, str]) -> 'BankOperation':
        return cls(
            date=datetime.strptime(
                row['timestamp'], '%b %d %Y').date().strftime('%Y-%m-%d'),
            transaction=row['type'],
            amount=float(row['amount']),
            o_from=row['from'],
            o_to=row['to'],
        )

    @classmethod
    def mapping_type_2(cls, row: Dict[str, str]) -> 'BankOperation':
        return cls(
            date=datetime.strptime(
                row['date'], '%d-%m-%Y').strftime('%Y-%m-%d'),
            transaction=row['transaction'],
            amount=float(row['amounts']),
            o_from=row['from'],
            o_to=row['to'],
        )

    @classmethod
    def mapping_type_3(cls, row: Dict[str, str]) -> 'BankOperation':
        amount = int(row['euro']) + float(row['cents']) / 100
        return cls(
            date=datetime.strptime(
                row['date_readable'], '%d %b %Y').strftime('%Y-%m-%d'),
            transaction=row['type'],
            amount=amount,
            o_from=row['from'],
            o_to=row['to'],
        )


OPERATION_MAPPING = {
    'timestamp,type,amount,from,to': BankOperation.mapping_type_1,
    'date,transaction,amounts,to,from': BankOperation.mapping_type_2,
    'date_readable,type,euro,cents,to,from': BankOperation.mapping_type_3,
}
