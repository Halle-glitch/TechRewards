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


# Test a 5 star Trustpilot review
def test_five_star_reward():

    result = calculate_trustpilot_reward(5)

    assert result == 10


# Test that 4 stars gives no reward
def test_four_star_reward():

    result = calculate_trustpilot_reward(4)

    assert result == 0


# Test that 1 star gives no reward
def test_one_star_reward():

    result = calculate_trustpilot_reward(1)

    assert result == 0


# Test a normal 10/10 CVC score
def test_cvc_ten_score():

    result = calculate_cvc_reward(10, False)

    assert result == 10


# Test a 10/10 score when the technician is named
def test_cvc_named_technician():

    result = calculate_cvc_reward(10, True)

    assert result == 50


# Test that a score below 10 gives no reward
def test_cvc_below_ten():

    result = calculate_cvc_reward(9, True)

    assert result == 0


# Test that a referral before 6 months gives no reward
def test_referral_before_six_months():

    result = calculate_referral_reward(5)

    assert result == 0


# Test that a referral reaching 6 months gives £1,000
def test_referral_after_six_months():

    result = calculate_referral_reward(6)

    assert result == 1000


# Test that a referral staying longer than 6 months still gives £1,000
def test_referral_after_more_than_six_months():

    result = calculate_referral_reward(12)

    assert result == 1000


# Test that 4 years of service gives no extra days
def test_long_service_before_five_years():

    result = calculate_long_service_reward(4)

    assert result == 0


# Test that 5 years of service gives 5 extra days
def test_long_service_after_five_years():

    result = calculate_long_service_reward(5)

    assert result == 5


# Test that more than 5 years still gives 5 extra days
def test_long_service_more_than_five_years():

    result = calculate_long_service_reward(10)

    assert result == 5


# Test the lowest scorecard star range
def test_scorecard_one_star():
    result = get_scorecard_stars(10)
    assert result == 1


# Test the second star range
def test_scorecard_two_stars():
    result = get_scorecard_stars(14)
    assert result == 2


# Test the third star range
def test_scorecard_three_stars():
    result = get_scorecard_stars(19)
    assert result == 3


# Test the fourth star range
def test_scorecard_four_stars():
    result = get_scorecard_stars(23)
    assert result == 4


# Test the fifth star range
def test_scorecard_five_stars():
    result = get_scorecard_stars(25)
    assert result == 5


# Test the Together Bonus for 3 stars
def test_together_bonus_three_stars():
    result = calculate_together_bonus(3)
    assert result == 975


# Test the Together Bonus for 1 star
def test_together_bonus_one_star():
    result = calculate_together_bonus(1)
    assert result == 682.5


# Test the Together Bonus for 2 stars
def test_together_bonus_two_stars():
    result = calculate_together_bonus(2)
    assert result == 828.75


# Test the Together Bonus for 4 stars
def test_together_bonus_four_stars():
    result = calculate_together_bonus(4)
    assert result == 1121.25


# Test the Together Bonus for 5 stars
def test_together_bonus_five_stars():
    result = calculate_together_bonus(5)
    assert result == 1267.5


# Test that the branch passes both Together Bonus gateways
def test_together_bonus_gateways_pass():
    result = check_together_bonus_gateways(0.98, 0.95)
    assert result is True


# Test that the branch fails when revenue is below the gateway
def test_together_bonus_revenue_gateway_fails():
    result = check_together_bonus_gateways(0.97, 0.95)
    assert result is False


# Test that the branch fails when SOS is below the gateway
def test_together_bonus_sos_gateway_fails():
    result = check_together_bonus_gateways(0.98, 0.94)
    assert result is False


# Test that the branch fails when both gateways are below the minimum
def test_together_bonus_both_gateways_fail():
    result = check_together_bonus_gateways(0.97, 0.94)
    assert result is False


# Test the final Together Bonus when 5 stars and gateways pass
def test_final_together_bonus_five_stars_gateways_pass():
    result = calculate_final_together_bonus(5, 0.98, 0.95)
    assert result == 1267.5