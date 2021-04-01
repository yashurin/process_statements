import os
import csv

from dataclasses import asdict

from typing import Generator

from config import (
    BankOperation, FIELDNAMES, OPERATION_MAPPING,
    OUTPUT_FILE, STATEMENTS_DIRECTORY,
)


def get_data_files() -> Generator[str, None, None]:
    """
    Get files with bank statements in the csv format from
    the statements directory.
    """
    os.chdir(STATEMENTS_DIRECTORY)
    return (
        os.path.join(os.getcwd(), f) for f in os.listdir(os.getcwd())
        if f.endswith('csv')
    )


def gather_data() -> Generator[BankOperation, None, None]:
    """
    Process files with bank statements from various banks
    and get a generator object with bank operations
    in the internal format.
    """
    for statement in get_data_files():
        with open(statement, 'r') as csv_file:
            csvreader = csv.DictReader(csv_file)
            fieldnames = csvreader.fieldnames or []
            headers = ','.join(fieldnames)

            yield from map(OPERATION_MAPPING[headers], csvreader)


def write_output(data) -> None:
    """
    Create an output files with the processed data of bank operations.
    """
    with open(OUTPUT_FILE, 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows([asdict(row) for row in data])


if __name__ == "__main__":

    bank_operations_data = gather_data()
    write_output(bank_operations_data)
