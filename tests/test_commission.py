from backend.commission import calculate_lead_commission


# Test a normal commission calculation
def test_normal_commission():

    result = calculate_lead_commission(7000, 1000)

    assert result == 50


# Test when a sale crosses the £2,500 threshold
def test_crossing_2500_threshold():

    result = calculate_lead_commission(2400, 500)

    assert result == 18.5


# Test when a sale crosses the £6,000 threshold
def test_crossing_6000_threshold():

    result = calculate_lead_commission(5900, 500)

    assert result == 24