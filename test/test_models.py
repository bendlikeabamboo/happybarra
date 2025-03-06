from happybarra.models import (
    CreditCard,
    DueDateType,
    WeekEndPolicy,
    CreditCardInstallment,
    InstallmentPolicy,
    InstallmentAmountType,
    weekend_check,
    this_day_next_month,
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
    actual = cc.statement_date(_input)
    assert expct == actual


def test_statement_for_purchase_on_statement(cc: CreditCard):
    # Bought something in March 2, 2025.
    # This is a Sunday.
    # My statement should've been given last Friday (Feb 28).
    # So this purchase should be placed on the next statement.
    expected = dt.date(2025, 4, 2)
    actual = cc.statement_date(dt.date(2025, 3, 2))
    assert expected == actual


def test_next_statement_aft_statement(cc: CreditCard):
    expected = dt.date(2025, 4, 2)
    actual = cc.statement_date(dt.date(2025, 3, 3))
    assert expected == actual


def test_weekend_check_prev_business_day(cc_swe_dwd: CreditCard):
    expected = dt.date(2025, 3, 7)
    actual = weekend_check(dt.date(2025, 3, 8), WeekEndPolicy.PREV_BANK_DAY)
    assert expected == actual


def test_weekend_check_next_business_day(cc_swe_dwd: CreditCard):
    expected = dt.date(2025, 3, 10)
    actual = weekend_check(dt.date(2025, 3, 8), WeekEndPolicy.NEXT_BANK_DAY)
    assert expected == actual


def test_weekend_check_prev_business_day_sunday(cc_swe_dwd: CreditCard):
    expected = dt.date(2025, 3, 7)
    actual = weekend_check(dt.date(2025, 3, 9), WeekEndPolicy.PREV_BANK_DAY)
    assert expected == actual


def test_weekend_check_next_business_day_sunday(cc_swe_dwd: CreditCard):
    expected = dt.date(2025, 3, 10)
    actual = weekend_check(dt.date(2025, 3, 9), WeekEndPolicy.NEXT_BANK_DAY)
    assert expected == actual


def test_due_date_for_purchase_made_before_statement(cc: CreditCard):
    expected = dt.date(2025, 4, 3)
    actual = cc.due_date(dt.date(2025, 4, 1))
    assert expected == actual


def test_due_date_for_purchase_made_on_stmnt(cc: CreditCard):
    expected = dt.date(2025, 4, 3)
    actual = cc.due_date(dt.date(2025, 4, 2))
    assert expected == actual


def test_next_payment_after_stmnt(cc: CreditCard):
    _input = dt.date(2025, 3, 3)
    expct = dt.date(2025, 4, 3)

    actual = cc.due_date(_input)
    assert expct == actual


def test_stmnt_falls_on_non_existent_day_next_month():
    cc = CreditCard("bank", "name", "idk", 1, 30)
    test_purchase_date = dt.date(2025, 1, 31)

    expc_statement_date = dt.date(2025, 2, 28)
    actual = cc.statement_date(test_purchase_date)
    assert expc_statement_date == actual


def test_dates_on_purchase(cc: CreditCard):
    first_month = {}
    first_month["amount"] = 100.0
    first_month["bill_post_date"] = dt.date(2025, 3, 2)
    # will not be included in 2025-03-02 because that cutoff will be moved to 2025-02-28
    # because it falls on a weekend
    first_month["statement_date"] = dt.date(2025, 4, 2)
    first_month["due_date"] = dt.date(2025, 4, 3)

    last_month = {}
    last_month["amount"] = 100.0
    last_month["bill_post_date"] = dt.date(2025, 6, 2)
    last_month["statement_date"] = dt.date(2025, 6, 2)
    last_month["due_date"] = dt.date(2025, 6, 3)

    installment = CreditCardInstallment(
        cc,
        3,
        dt.date(2025, 3, 2),
        InstallmentPolicy.ON_PURCHASE_DAY,
        100.00,
        InstallmentAmountType.MONTHLY_FIXED,
    )
    charge_dates = installment.get_charge_dates()

    assert charge_dates[0].amount == first_month["amount"]
    assert charge_dates[0].bill_post_date == first_month["bill_post_date"]
    assert charge_dates[0].statement_date == first_month["statement_date"]
    assert charge_dates[0].due_date == first_month["due_date"]

    assert charge_dates[2].amount == last_month["amount"]
    assert charge_dates[2].bill_post_date == last_month["bill_post_date"]
    assert charge_dates[2].statement_date == last_month["statement_date"]
    assert charge_dates[2].due_date == last_month["due_date"]

    first_month = {}
    first_month["amount"] = 100.0
    first_month["bill_post_date"] = dt.date(2025, 3, 2)
    # will not be included in 2025-03-02 because that cutoff will be moved to 2025-02-28
    # because it falls on a weekend
    first_month["statement_date"] = dt.date(2025, 4, 2)
    first_month["due_date"] = dt.date(2025, 4, 3)

    last_month = {}
    last_month["amount"] = 100.0
    last_month["bill_post_date"] = dt.date(2025, 6, 2)
    last_month["statement_date"] = dt.date(2025, 6, 2)
    last_month["due_date"] = dt.date(2025, 6, 3)

    installment = CreditCardInstallment(
        cc,
        3,
        dt.date(2025, 3, 2),
        InstallmentPolicy.ON_PURCHASE_DAY,
        300.00,
        InstallmentAmountType.TOTAL_FIXED,
    )
    charge_dates = installment.get_charge_dates()

    assert charge_dates[0].amount == first_month["amount"]
    assert charge_dates[0].bill_post_date == first_month["bill_post_date"]
    assert charge_dates[0].statement_date == first_month["statement_date"]
    assert charge_dates[0].due_date == first_month["due_date"]

    assert charge_dates[2].amount == last_month["amount"]
    assert charge_dates[2].bill_post_date == last_month["bill_post_date"]
    assert charge_dates[2].statement_date == last_month["statement_date"]
    assert charge_dates[2].due_date == last_month["due_date"]
