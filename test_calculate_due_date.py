from calculate_due_date import calculate_due_date
from datetime import datetime
import pytest

# innput validation tests, invalids

def test_invalid_submit_date():
    with pytest.raises(ValueError, match="Submit date is not a valid input, try a datetime.datetime type."):
        calculate_due_date("String_input", 12)

def test_invalid_turnaround_time_negative_int():
    with pytest.raises(ValueError, match="Turnaround time is not a valid input, try a positive integer in hours."):
        calculate_due_date(datetime(2022,4,15,10,30), -10)

def test_invalid_turnaround_time_zero():
    with pytest.raises(ValueError, match="Turnaround time is not a valid input, try a positive integer in hours."):
        calculate_due_date(datetime(2022,4,15,10,30), 0)

def test_invalid_turnaround_time_not_int():
    with pytest.raises(ValueError, match="Turnaround time is not a valid input, try a positive integer in hours."):
        calculate_due_date(datetime(2022,4,15,10,30), "11")

def test_invalid_turnaround_time_not_int():
    with pytest.raises(ValueError, match="Turnaround time is not a valid input, try a positive integer in hours."):
        calculate_due_date(datetime(2022,4,15,10,30), 1.11)

def test_invalid_submit_date_saturday():
    with pytest.raises(ValueError, match="Invalid submit date, try weekdays:Mon-Fri."):
        calculate_due_date(datetime(2022,4,16,10,30), 2)

def test_invalid_submit_date_08_50():
    with pytest.raises(ValueError, match="Invalid submit date time, try working hours:9-17."):
        calculate_due_date(datetime(2022,4,15,8,50), 2)

def test_invalid_submit_date_17_01():
    with pytest.raises(ValueError, match="Invalid submit date time, try working hours:9-17."):
        calculate_due_date(datetime(2022,4,15,17,1), 2)

# input validation test, valid

def test_valid_submit_date_and_turnaround_time_valid_return_type():
    assert isinstance(calculate_due_date(datetime(2022,4,15,10,30), 12), datetime)

# calculation tests

# From friday 10:30 to same day 10:30
def test_valid_0_day():
    assert calculate_due_date(datetime(2022,4,15,10,30), 2) == datetime(2022,4,15,12,30)

# From friday 10:30 to monday 10:30
def test_valid_friday_to_monday():
    assert calculate_due_date(datetime(2022,4,15,10,30), 8) == datetime(2022,4,18,10,30)

# From last friday of month to next months
def test_go_to_next_month():
    assert calculate_due_date(datetime(2022,4,29,10,30), 8) == datetime(2022,5,2,10,30)

# From tuesday to friday
def test_valid_3_day_same_week():
    assert calculate_due_date(datetime(2022,4,12,10,30), 24) == datetime(2022,4,15,10,30)

# From thursday going into next day plus weekend
def test_valid_17_01():
    assert calculate_due_date(datetime(2022,4,14,12,1),13) == datetime(2022,4,18,9,1)

# From wednesday into thursday going into AM and setting due date to starting work hours
def test_valid_16_59():
    assert calculate_due_date(datetime(2022,4,13,16,59),7) == datetime(2022,4,14,15,59)

# From wednesday into thursday going into AM and setting due date to starting work hours
def test_valid_17_00():
    assert calculate_due_date(datetime(2022,4,13,17,0),7) == datetime(2022,4,14,16,00)

# From starting work hours to ending work hours
def test_valid_full_day():
    assert calculate_due_date(datetime(2022,4,14,9,0),8) == datetime(2022,4,15,9,0)