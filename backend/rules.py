# TechRewards 2026 rules

# Lead commission brackets
LEAD_COMMISSION_BRACKETS = [
    (0, 0.025),
    (2500, 0.04),
    (6000, 0.05),
    (12000, 0.06),
    (22000, 0.07),
]


# Customer feedback rewards
TRUSTPILOT_REWARD = 10
CVC_REWARD = 10
CVC_NAMED_TECHNICIAN_REWARD = 50


# Refer a Friend
REFERRAL_REWARD = 1000
REFERRAL_REQUIRED_MONTHS = 6


# Long Service
LONG_SERVICE_YEARS = 5
LONG_SERVICE_EXTRA_DAYS = 5


# Together Bonus scorecard
SCORECARD_MIN_POINTS = 10
SCORECARD_MAX_POINTS = 30


# Scorecard star ranges
SCORECARD_STAR_RANGES = [
    (10, 13, 1),
    (14, 18, 2),
    (19, 22, 3),
    (23, 24, 4),
    (25, 30, 5),
]


# Scorecard modifiers
SCORECARD_MODIFIERS = {
    1: -0.30,
    2: -0.15,
    3: 0.00,
    4: 0.15,
    5: 0.30,
}


# Together Bonus
# Together Bonus maximum quarterly payout
TOGETHER_BONUS_MAX = 750


# Together Bonus payout table for Revenue vs Budget and SOS
TOGETHER_BONUS_TABLE = {
    0.98: {
        0.95: 300,
        0.96: 325,
    },
    1.00: {
        0.95: 400,
        0.96: 425,
        0.97: 450,
    },
    1.05: {
        0.95: 500,
        0.96: 525,
        0.97: 550,
        0.98: 575,
    },
    1.10: {
        0.95: 650,
        0.96: 675,
        0.97: 700,
        0.98: 725,
        0.99: 750,
    },
}


# Together Bonus branch gateways
TOGETHER_REVENUE_GATE = 0.98
TOGETHER_SOS_GATE = 0.95


# Special payment for 5 star technicians
TOGETHER_FIVE_STAR_GATE_FAILURE = 300


# Lead Statuses
LEAD_STATUSES = [
    "Created",
    "Sent",
    "Received",
    "Survey",
    "Quote",
    "Won",
    "Lost",
]


# Lead status transitions
LEAD_STATUS_TRANSITIONS = {
    "Created": ["Sent"],
    "Sent": ["Received"],
    "Received": ["Survey"],
    "Survey": ["Quote"],
    "Quote": ["Won", "Lost"],
    "Won": [],
    "Lost": [],
}