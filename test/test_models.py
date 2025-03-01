from happybara.models import CreditCard, DueDateType, WeekendCheckPolicy
import pytest
import datetime as dt


@pytest.fixture(name="cc")
def fixture_cc():
    return CreditCard(
        bank="bankA",
        name="platinum",
        network="mastercard",
        due_date_type=DueDateType.X_DAYS_AFTER,
        due_date_reference=1,
        statement_day=2,
    )


@pytest.fixture(name="cc_swe_dwd")
def fixture_cc_swe_dwd():
    return CreditCard(
        bank="bankB",
        name="platinum",
        network="mastercard",
        due_date_type=DueDateType.X_DAYS_AFTER,
        due_date_reference=8,
        statement_day=2,
    )


def test_next_statement_before_statement(cc: CreditCard):
    _input = dt.date(2025, 3, 1)
    expct = dt.date(2025, 4, 2)
    actual = cc._next_statement(_input)
    assert expct == actual


def test_next_statement_on_statement(cc: CreditCard):
    expected = dt.date(2025, 3, 2)
    actual = cc._next_statement(dt.date(2025, 3, 2))
    assert expected == actual


def test_next_statement_aft_statement(cc: CreditCard):
    expected = dt.date(2025, 4, 2)
    actual = cc._next_statement(dt.date(2025, 3, 3))
    assert expected == actual


def test_weekend_check_prev_business_day(cc_swe_dwd: CreditCard):
    expected = dt.date(2025, 3, 7)
    actual = cc_swe_dwd._weekend_check(
        dt.date(2025, 3, 8), WeekendCheckPolicy.PREVIOUS_BUSINESS_DAY
    )
    assert expected == actual

def test_weekend_check_next_business_day(cc_swe_dwd: CreditCard):
    expected = dt.date(2025, 3, 10)
    actual = cc_swe_dwd._weekend_check(
        dt.date(2025, 3, 8), WeekendCheckPolicy.NEXT_BUSINESS_DAY
    )
    assert expected == actual

def test_weekend_check_prev_business_day_sunday(cc_swe_dwd: CreditCard):
    expected = dt.date(2025, 3, 7)
    actual = cc_swe_dwd._weekend_check(
        dt.date(2025, 3, 9), WeekendCheckPolicy.PREVIOUS_BUSINESS_DAY
    )
    assert expected == actual

def test_weekend_check_next_business_day_sunday(cc_swe_dwd: CreditCard):
    expected = dt.date(2025, 3, 10)
    actual = cc_swe_dwd._weekend_check(
        dt.date(2025, 3, 9), WeekendCheckPolicy.NEXT_BUSINESS_DAY
    )
    assert expected == actual

def test_next_payment_before_stmnt(cc: CreditCard):
    expected = dt.date(2025, 3, 3)
    actual = cc.next_payment(dt.date(2025, 3, 1))
    assert expected == actual


def test_next_payment_on_stmnt(cc: CreditCard):
    expected = dt.date(2025, 3, 3)
    actual = cc.next_payment(dt.date(2025, 3, 2))
    assert expected == actual


def test_next_payment_after_stmnt(cc: CreditCard):
    _input = dt.date(2025, 3, 3)
    expct = dt.date(2025, 4, 3)

    actual = cc.next_payment(_input)
    assert expct == actual
