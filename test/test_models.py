from happybara.models import (
    CreditCard,
    DueDateType,
    WeekEndPolicy,
    CreditCardInstallment,
    InstallmentPolicy,
    InstallmentAmountType,
)
import pytest
import datetime as dt


@pytest.fixture(name="cc")
def fixture_cc():
    return CreditCard(
        bank="bankA",
        name="platinum",
        network="mastercard",
        due_date_type=DueDateType.X_DAYS_AFTER,
        due_date_ref=1,
        statement_day=2,
    )


@pytest.fixture(name="cc_swe_dwd")
def fixture_cc_swe_dwd():
    return CreditCard(
        bank="bankB",
        name="platinum",
        network="mastercard",
        due_date_type=DueDateType.X_DAYS_AFTER,
        due_date_ref=8,
        statement_day=2,
    )


def test_next_statement_before_statement(cc: CreditCard):
    _input = dt.date(2025, 3, 1)
    expct = dt.date(2025, 4, 2)
    actual = cc.next_statement(_input)
    assert expct == actual


def test_next_statement_on_statement(cc: CreditCard):
    expected = dt.date(2025, 3, 2)
    actual = cc.next_statement(dt.date(2025, 3, 2))
    assert expected == actual


def test_next_statement_aft_statement(cc: CreditCard):
    expected = dt.date(2025, 4, 2)
    actual = cc.next_statement(dt.date(2025, 3, 3))
    assert expected == actual


def test_weekend_check_prev_business_day(cc_swe_dwd: CreditCard):
    expected = dt.date(2025, 3, 7)
    actual = cc_swe_dwd._weekend_check(dt.date(2025, 3, 8), WeekEndPolicy.PREV_BANK_DAY)
    assert expected == actual


def test_weekend_check_next_business_day(cc_swe_dwd: CreditCard):
    expected = dt.date(2025, 3, 10)
    actual = cc_swe_dwd._weekend_check(dt.date(2025, 3, 8), WeekEndPolicy.NEXT_BANK_DAY)
    assert expected == actual


def test_weekend_check_prev_business_day_sunday(cc_swe_dwd: CreditCard):
    expected = dt.date(2025, 3, 7)
    actual = cc_swe_dwd._weekend_check(dt.date(2025, 3, 9), WeekEndPolicy.PREV_BANK_DAY)
    assert expected == actual


def test_weekend_check_next_business_day_sunday(cc_swe_dwd: CreditCard):
    expected = dt.date(2025, 3, 10)
    actual = cc_swe_dwd._weekend_check(dt.date(2025, 3, 9), WeekEndPolicy.NEXT_BANK_DAY)
    assert expected == actual


def test_next_payment_before_stmnt(cc: CreditCard):
    expected = dt.date(2025, 3, 3)
    actual = cc.next_due_date(dt.date(2025, 3, 1))
    assert expected == actual


def test_next_payment_on_stmnt(cc: CreditCard):
    expected = dt.date(2025, 3, 3)
    actual = cc.next_due_date(dt.date(2025, 3, 2))
    assert expected == actual


def test_next_payment_after_stmnt(cc: CreditCard):
    _input = dt.date(2025, 3, 3)
    expct = dt.date(2025, 4, 3)

    actual = cc.next_due_date(_input)
    assert expct == actual


def test_stmnt_falls_on_non_existent_day_next_month():
    cc = CreditCard("bank", "name", "idk", 1, 30)
    test_purchase_date = dt.date(2025, 1, 31)

    expc_statement_date = dt.date(2025, 2, 28)
    actual = cc.next_statement(test_purchase_date)
    assert expc_statement_date == actual


def test_dates_on_purchase(cc: CreditCard):
    installment = CreditCardInstallment(
        cc,
        3,
        dt.date(2025, 3, 2),
        InstallmentPolicy.ON_PURCHASE_DAY,
        100.00,
        InstallmentAmountType.MONTHLY_FIXED,
    )
    charge_dates = installment.get_charge_dates()
    print("edi wow")
