from backend.rewards import (calculate_trustpilot_reward, 
                             calculate_cvc_reward, 
                             calculate_referral_reward,
                             calculate_long_service_reward)


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