# Bank Statements Processing

This script processes statements from sereval banks from the `datafiles` folder and creates a unified csv.

## Running the Script

From the root directory, execute the command 

`python3 process.py`

It will create the `result.csv` file in the root directory.

## Tests

The code can be tested for errors by following commands executed from the root directory (providing that pytest, mypy and flake8 packages are installed):

`pytest`

`flake8 process.py`

`mypy process.py`

## Extendability

The code can be easily extended to process bank statements from more banks. There are two requirements:

1) To add a mapping type method to the `BankOperation` dataclass which will map bank's data to internal data.
2) To add a key/value pair to the `OPERATION_MAPPING` dictionary. The key consists of concatenated comma-separated headers. It allows to automatically select the method of mapping. 

The code can also be extended to process bank statements in JSON and XML by following the same pattern:

1) Separate methods to process `csv`, `json` and `xml` files can be created.
2) A mapping can be created to map a file extension to a method of processing a file with that file extension.

I haven't done it because of time constraints, and because there were no sample files in those formats.  

&copy; Andrey Yashurin, 2021 yashurin@gmail.com
