from backend.rewards import (
    calculate_trustpilot_reward,
    calculate_cvc_reward,
    calculate_referral_reward,
    calculate_long_service_reward,
    get_scorecard_stars,
    calculate_together_bonus,
    check_together_bonus_gateways,
    calculate_final_together_bonus,
)


# -------------------------
# Trustpilot tests
# -------------------------

# Test 5 stars
def test_trustpilot_five_stars():
    result = calculate_trustpilot_reward(5)
    assert result == 10


# Test 4 stars
def test_trustpilot_four_stars():
    result = calculate_trustpilot_reward(4)
    assert result == 0


# Test 1 star
def test_trustpilot_one_star():
    result = calculate_trustpilot_reward(1)
    assert result == 0


# -------------------------
# CVC tests
# -------------------------

# Test 10/10 with technician named
def test_cvc_ten_named():
    result = calculate_cvc_reward(10, True)
    assert result == 50


# Test 10/10 without technician named
def test_cvc_ten_not_named():
    result = calculate_cvc_reward(10, False)
    assert result == 10


# Test score below 10
def test_cvc_below_ten():
    result = calculate_cvc_reward(9, True)
    assert result == 0


# -------------------------
# Referral tests
# -------------------------

# Test referral before 6 months
def test_referral_before_six_months():
    result = calculate_referral_reward(5)
    assert result == 0


# Test referral at 6 months
def test_referral_six_months():
    result = calculate_referral_reward(6)
    assert result == 1000


# Test referral after 6 months
def test_referral_after_six_months():
    result = calculate_referral_reward(12)
    assert result == 1000


# -------------------------
# Long Service tests
# -------------------------

# Test before 5 years
def test_long_service_before_five_years():
    result = calculate_long_service_reward(4)
    assert result == 0


# Test at 5 years
def test_long_service_five_years():
    result = calculate_long_service_reward(5)
    assert result == 5


# Test after 5 years
def test_long_service_ten_years():
    result = calculate_long_service_reward(10)
    assert result == 5


# -------------------------
# Scorecard star tests
# -------------------------

# Test 10 points = 1 star
def test_scorecard_ten_points():
    result = get_scorecard_stars(10)
    assert result == 1


# Test 14 points = 2 stars
def test_scorecard_fourteen_points():
    result = get_scorecard_stars(14)
    assert result == 2


# Test 19 points = 3 stars
def test_scorecard_nineteen_points():
    result = get_scorecard_stars(19)
    assert result == 3


# Test 23 points = 4 stars
def test_scorecard_twenty_three_points():
    result = get_scorecard_stars(23)
    assert result == 4


# Test 25 points = 5 stars
def test_scorecard_twenty_five_points():
    result = get_scorecard_stars(25)
    assert result == 5


# -------------------------
# Together Bonus tests
# -------------------------

# Test 3 stars
def test_together_bonus_three_stars():
    result = calculate_together_bonus(3)
    assert result == 975


# Test 1 star
def test_together_bonus_one_star():
    result = calculate_together_bonus(1)
    assert result == 682.5


# Test 2 stars
def test_together_bonus_two_stars():
    result = calculate_together_bonus(2)
    assert result == 828.75


# Test 4 stars
def test_together_bonus_four_stars():
    result = calculate_together_bonus(4)
    assert result == 1121.25


# Test 5 stars
def test_together_bonus_five_stars():
    result = calculate_together_bonus(5)
    assert result == 1267.5


# -------------------------
# Together Bonus gateway tests
# ------------------------- 

# Test both gateways pass
def test_together_bonus_gateways_pass():
    result = check_together_bonus_gateways(0.98, 0.95)
    assert result is True


# Test revenue gateway fails
def test_together_bonus_revenue_fails():
    result = check_together_bonus_gateways(0.97, 0.95)
    assert result is False


# Test SOS gateway fails
def test_together_bonus_sos_fails():
    result = check_together_bonus_gateways(0.98, 0.94)
    assert result is False


# Test both gateways fail
def test_together_bonus_both_gateways_fail():
    result = check_together_bonus_gateways(0.97, 0.94)
    assert result is False


# -------------------------
# Final Together Bonus tests
# -------------------------

# Test 5 stars when both gateways pass
def test_final_together_bonus_five_stars_gateways_pass():
    result = calculate_final_together_bonus(5, 0.98, 0.95)
    assert result == 1267.5


# Test 5 stars when a gateway fails
def test_final_together_bonus_five_stars_gateway_fails():
    result = calculate_final_together_bonus(5, 0.97, 0.95)
    assert result == 300

