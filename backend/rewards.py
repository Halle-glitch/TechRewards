from backend.rules import (
    TRUSTPILOT_REWARD,
    CVC_REWARD,
    CVC_NAMED_TECHNICIAN_REWARD,
    REFERRAL_REWARD,
    REFERRAL_REQUIRED_MONTHS,
    LONG_SERVICE_YEARS,
    LONG_SERVICE_EXTRA_DAYS,
    SCORECARD_STAR_RANGES,
    SCORECARD_MODIFIERS,
    TOGETHER_BONUS_MAX,
    TOGETHER_REVENUE_GATE,
    TOGETHER_SOS_GATE,
    TOGETHER_FIVE_STAR_GATE_FAILURE,
    )


# Calculate Trustpilot reward
def calculate_trustpilot_reward(stars):

    # Give the reward only for 5 stars
    if stars == 5:
        return TRUSTPILOT_REWARD

    # No reward for other ratings
    return 0


# Calculate CVC reward
def calculate_cvc_reward(score, technician_named):

    # Give £50 if the customer gave 10/10 and named the technician
    if score == 10 and technician_named:
        return CVC_NAMED_TECHNICIAN_REWARD

    # Give £10 for a normal 10/10 score
    if score == 10:
        return CVC_REWARD

    # No reward for other scores
    return 0


# Calculate referral reward
def calculate_referral_reward(months_employed):

    # Give the reward after the referred person stays 6 months
    if months_employed >= REFERRAL_REQUIRED_MONTHS:
        return REFERRAL_REWARD

    # No reward before 6 months
    return 0


# Calculate long service reward
def calculate_long_service_reward(years_employed):

    # Give the extra days after 5 years
    if years_employed >= LONG_SERVICE_YEARS:
        return LONG_SERVICE_EXTRA_DAYS

    # No extra days before 5 years
    return 0


# Calculate scorecard stars
def get_scorecard_stars(points):

    # Check each star range
    for minimum_points, maximum_points, stars in SCORECARD_STAR_RANGES:

        # Check if the points are inside this range
        if minimum_points <= points <= maximum_points:
            return stars

    # Return no stars if the points are outside the valid range
    return 0


# Calculate the Together Bonus
def calculate_together_bonus(stars):

    # Get the modifier for the number of stars
    modifier = SCORECARD_MODIFIERS[stars]

    # Calculate the bonus
    bonus = TOGETHER_BONUS_MAX * (1 + modifier)

    # Return the bonus
    return bonus


# Check if the branch passed the Together Bonus gateways
def check_together_bonus_gateways(revenue_vs_budget, sos_ytd):

    # Check if both branch gateways were passed
    if revenue_vs_budget >= TOGETHER_REVENUE_GATE and sos_ytd >= TOGETHER_SOS_GATE:
        return True

    # At least one gateway was missed
    return False


# Calculate the final Together Bonus
def calculate_final_together_bonus(stars, revenue_vs_budget, sos_ytd):

    # Check if the branch passed both gateways
    gateways_passed = check_together_bonus_gateways(
        revenue_vs_budget,
        sos_ytd
    )

    # Give £300 to 5 star technicians if the branch failed a gateway
    if not gateways_passed and stars == 5:
        return TOGETHER_FIVE_STAR_GATE_FAILURE

    # Calculate the normal bonus
    return calculate_together_bonus(stars)