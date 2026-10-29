import pytest
from car_insurance_premium import annual_premium, no_claim_bonus, claim_payout


# ======================= annual_premium =======================
# if car_type not in BASE_PREMIUM -> True / False
def test_unknown_car_type():
    with pytest.raises(ValueError):
        annual_premium("truck", 30, 0, False)


@pytest.mark.parametrize("car_type, expected", [
    ("hatchback", 8000),
    ("sedan", 12000),
    ("suv", 15000),
])
def test_each_car_type_base(car_type, expected):
    # age 30 (no surcharge), 1 claim (no change), no anti-theft
    assert annual_premium(car_type, 30, 1, False) == expected


# if driver_age < 18 -> True / False (boundary 17 vs 18)
def test_driver_too_young():
    with pytest.raises(ValueError):
        annual_premium("sedan", 17, 0, False)


def test_driver_exactly_18():
    # 12000 + 4000 = 16000, 1 claim -> 16000
    assert annual_premium("sedan", 18, 1, False) == 16000


# if driver_age < 25 / elif driver_age >= 60 / neither
def test_young_driver_surcharge():
    assert annual_premium("hatchback", 24, 1, False) == 12000


def test_driver_exactly_25_no_surcharge():
    assert annual_premium("hatchback", 25, 1, False) == 8000


def test_driver_59_no_surcharge():
    assert annual_premium("hatchback", 59, 1, False) == 8000


def test_senior_driver_exactly_60():
    assert annual_premium("hatchback", 60, 1, False) == 10000


# if claims == 0 / elif claims > 2 / neither (1 or 2)
def test_sedan_no_claims():
    assert annual_premium("sedan", 30, 0, False) == 9600


def test_two_claims_no_change():
    assert annual_premium("sedan", 30, 2, False) == 12000


def test_three_claims_doubles():
    assert annual_premium("sedan", 30, 3, False) == 24000


# if has_anti_theft -> True / False
def test_anti_theft_discount():
    assert annual_premium("sedan", 30, 0, True) == 9100


def test_combined_young_many_claims_anti_theft():
    # (15000 + 4000) * 2 = 38000 - 500 = 37500
    assert annual_premium("suv", 20, 4, True) == 37500


def test_combined_senior_no_claims_anti_theft():
    # 8000 + 2000 = 10000 -> -2000 = 8000 -> -500 = 7500
    assert annual_premium("hatchback", 70, 0, True) == 7500


# ======================= no_claim_bonus =======================
def test_invalid_years():
    with pytest.raises(ValueError):
        no_claim_bonus(-1)


@pytest.mark.parametrize("years, expected", [
    (0, 0),
    (1, 20),
    (2, 20),
    (3, 35),
    (4, 35),
    (5, 50),
    (10, 50),
])
def test_bonus_all_bands(years, expected):
    assert no_claim_bonus(years) == expected


# ======================= claim_payout =======================
# damage_cost < 0 or deductible < 0 -> both sides of the `or`
def test_negative_damage():
    with pytest.raises(ValueError):
        claim_payout(-100, 50000, 1000, False)


def test_negative_deductible():
    with pytest.raises(ValueError):
        claim_payout(1000, 50000, -1, False)


def test_total_loss():
    assert claim_payout(80000, 50000, 1000, True) == 50000


def test_damage_below_deductible():
    assert claim_payout(500, 50000, 1000, False) == 0


def test_damage_equal_to_deductible():
    assert claim_payout(1000, 50000, 1000, False) == 0


def test_normal_payout():
    assert claim_payout(10000, 50000, 1000, False) == 9000


def test_payout_equal_to_insured_value():
    assert claim_payout(51000, 50000, 1000, False) == 50000


def test_payout_capped_at_insured_value():
    assert claim_payout(80000, 50000, 1000, False) == 50000
