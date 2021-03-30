import os
import csv

from datetime import datetime

from dataclasses import dataclass, asdict

from typing import Dict, Generator


STATEMENTS_DIRECTORY = 'datafiles'

OUTPUT_FILE = 'result.csv'


FIELDNAMES = ['date', 'transaction', 'amount', 'o_from', 'o_to']


@dataclass
class BankOperation:
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


def get_data_files() -> Generator[str, None, None]:
    os.chdir(STATEMENTS_DIRECTORY)
    return (
        os.path.join(os.getcwd(), f) for f in os.listdir(os.getcwd())
        if f.endswith('csv')
    )


def gather_data() -> Generator[BankOperation, None, None]:
    for statement in get_data_files():
        with open(statement, 'r') as csv_file:
            csvreader = csv.DictReader(csv_file)
            fieldnames = csvreader.fieldnames or []
            headers = ','.join(fieldnames)

            yield from map(OPERATION_MAPPING[headers], csvreader)


def write_output(data) -> None:
    with open(OUTPUT_FILE, 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows([asdict(row) for row in data])


if __name__ == "__main__":

    bank_operations_data = gather_data()
    write_output(bank_operations_data)
