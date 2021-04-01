from .config import BankOperation


def test_bank_operation_mapping_1():
    row = {
        'timestamp': 'Oct 1 2019',
        'type': 'remove',
        'amount': '99.20',
        'from': '198', 'to': '182'
    }
    expected_result = BankOperation(
        date='2019-10-01',
        transaction='remove',
        amount=99.2,
        o_from='198',
        o_to='182'
    )

    assert BankOperation.mapping_type_1(row) == expected_result


def test_bank_operation_mapping_2():
    row = {
        'date': '03-10-2019',
        'transaction': 'remove',
        'amounts': '99.40',
        'from': '198',
        'to': '182'
    }
    expected_result = BankOperation(
        date='2019-10-03',
        transaction='remove',
        amount=99.4,
        o_from='198',
        o_to='182'
    )

    assert BankOperation.mapping_type_2(row) == expected_result


def test_bank_operation_mapping_3():
    row = {
        'date_readable': '5 Oct 2019',
        'type': 'remove',
        'euro': '5',
        'cents': '7',
        'from': '198',
        'to': '182'
    }
    expected_result = BankOperation(
        date='2019-10-05',
        transaction='remove',
        amount=5.07,
        o_from='198',
        o_to='182'
    )

    assert BankOperation.mapping_type_3(row) == expected_result
