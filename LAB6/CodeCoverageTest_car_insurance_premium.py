import pytest
from car_insurance_premium import annual_premium, no_claim_bonus, claim_payout


# ---------- annual_premium ----------
def test_sedan_no_claims():
    assert annual_premium("sedan", 30, 0, False) == 9600


def test_unknown_car_type():
    with pytest.raises(ValueError):
        annual_premium("truck", 30, 0, False)


def test_driver_too_young():
    with pytest.raises(ValueError):
        annual_premium("sedan", 17, 0, False)


def test_young_driver_surcharge():
    # 8000 + 4000 = 12000, 1 claim -> no change
    assert annual_premium("hatchback", 20, 1, False) == 12000


def test_senior_driver_surcharge():
    # 15000 + 2000 = 17000, 0 claims -> -20% = 13600
    assert annual_premium("suv", 65, 0, False) == 13600


def test_many_claims_doubles_premium():
    # 12000 * 2 = 24000
    assert annual_premium("sedan", 30, 3, False) == 24000


def test_anti_theft_discount():
    # 12000 - 2400 = 9600, -500 = 9100
    assert annual_premium("sedan", 30, 0, True) == 9100


# ---------- no_claim_bonus ----------
def test_no_bonus():
    assert no_claim_bonus(0) == 0


def test_invalid_years():
    with pytest.raises(ValueError):
        no_claim_bonus(-1)


def test_bonus_five_years():
    assert no_claim_bonus(5) == 50


def test_bonus_three_years():
    assert no_claim_bonus(3) == 35


def test_bonus_one_year():
    assert no_claim_bonus(1) == 20


# ---------- claim_payout ----------
def test_invalid_amount():
    with pytest.raises(ValueError):
        claim_payout(-100, 50000, 1000, False)


def test_total_loss():
    assert claim_payout(80000, 50000, 1000, True) == 50000


def test_damage_below_deductible():
    assert claim_payout(500, 50000, 1000, False) == 0


def test_normal_payout():
    assert claim_payout(10000, 50000, 1000, False) == 9000


def test_payout_capped_at_insured_value():
    assert claim_payout(80000,50000, 1000, False) == 50000
