from backend.rules import (TRUSTPILOT_REWARD,CVC_REWARD,CVC_NAMED_TECHNICIAN_REWARD,
                           REFERRAL_REWARD,REFERRAL_REQUIRED_MONTHS,LONG_SERVICE_YEARS, LONG_SERVICE_EXTRA_DAYS)


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