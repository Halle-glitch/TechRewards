from backend.rules import LEAD_COMMISSION_BRACKETS


# Get the current commission rate
def get_commission_rate(total_converted):

    # Start with the lowest commission rate
    commission_rate = 0

    # Check each commission bracket
    for minimum_value, rate in LEAD_COMMISSION_BRACKETS:

        # If the total is high enough, use this rate
        if total_converted >= minimum_value:
            commission_rate = rate

    # Return the highest rate reached
    return commission_rate


# Calculate commission for a sale
def calculate_commission(sale_value, commission_rate):

    # Calculate the commission
    commission = sale_value * commission_rate

    # Return the commission
    return commission

# Check if the values are valid
def validate_commission_values(total_converted, sale_value):

    # Total converted cannot be negative
    if total_converted < 0:
        raise ValueError("Total converted cannot be negative")

    # Sale value must be greater than zero
    if sale_value <= 0:
        raise ValueError("Sale value must be greater than zero")

    # Values are valid
    return True


# Calculate commission for a new lead sale
def calculate_lead_commission(total_converted, sale_value):

    validate_commission_values(total_converted, sale_value)

    # Start with no commission
    total_commission = 0

    # Track how much of the sale we have calculated
    remaining_sale = sale_value

    # Check each commission bracket
    for i in range(len(LEAD_COMMISSION_BRACKETS)):

        # Get the current bracket
        current_threshold, current_rate = LEAD_COMMISSION_BRACKETS[i]

        # If this is the last bracket, all remaining sale uses this rate
        if i == len(LEAD_COMMISSION_BRACKETS) - 1:
            total_commission += remaining_sale * current_rate
            break

        # Get the next threshold
        next_threshold = LEAD_COMMISSION_BRACKETS[i + 1][0]

        # If we are already above this bracket, move to the next one
        if total_converted >= next_threshold:
            continue

        # Work out where the sale starts
        sale_start = max(total_converted, current_threshold)

        # Work out how much space is left in this bracket
        bracket_space = next_threshold - sale_start

        # Work out how much of the sale belongs to this bracket
        sale_in_bracket = min(remaining_sale, bracket_space)

        # Add the commission for this part
        total_commission += sale_in_bracket * current_rate

        # Remove this part from the remaining sale
        remaining_sale -= sale_in_bracket

        # Move the total forward
        total_converted += sale_in_bracket

        # Stop when the whole sale has been calculated
        if remaining_sale <= 0:
            break

    # Return the total commission
    return total_commission


