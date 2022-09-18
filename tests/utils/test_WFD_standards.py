import pytest
from app.utils.WFD_standards import WFD_Standards

# Initialise all current standards for BOD and NH3 for both river types
@pytest.fixture(scope='session')
def standards_1_2_4_6_bod():
    return WFD_Standards(is_1_2_4_6=True, is_bod=True)

@pytest.fixture(scope='session')
def standards_1_2_4_6_nh3():
    return WFD_Standards(is_1_2_4_6=True, is_bod=False)

@pytest.fixture(scope='session')
def standards_3_5_7_bod():
    return WFD_Standards(is_1_2_4_6=False, is_bod=True)

@pytest.fixture(scope='session')
def standards_3_5_7_nh3():
    return WFD_Standards(is_1_2_4_6=False, is_bod=False)

# Current Standards for reference
# All standards have been taken from page 16 of: http://www.fwr.org/UPM3/Section2.pdf

# Standards_1_2_4_6
# BOD_high = 7
# BOD_good = 9
# BOD_moderate = 14
# BOD_poor = 16

# NH3_high = 0.5
# NH3_good = 0.7
# NH3_moderate = 1.8
# NH3_poor = 2.6

# Standards_3_5_7
# BOD_high = 9
# BOD_good = 11
# BOD_moderate = 14
# BOD_poor = 19

# NH3_high = 0.7
# NH3_good = 1.5
# NH3_moderate = 2.6
# NH3_poor = 6

# Tests for BOD Standards against river types 1,2,4,6 
def test_standards_1_2_4_6_BOD_High(standards_1_2_4_6_bod):
    assert standards_1_2_4_6_bod.check_wfd_standard_attained(6.0) == "High"

def test_standards_1_2_4_6_BOD_Poor(standards_1_2_4_6_bod):
    assert standards_1_2_4_6_bod.check_wfd_standard_attained(15) == "Poor"

# Tests for NH3 Standards against river types 1,2,4,6 
def test_standards_1_2_4_6_NH3_Moderate(standards_1_2_4_6_nh3):
    assert standards_1_2_4_6_nh3.check_wfd_standard_attained(1.2) == "Moderate"


# Tests for BOD Standards against river types 3,5,7
def test_standards_3_5_7_BOD_High(standards_3_5_7_bod):
    assert standards_3_5_7_bod.check_wfd_standard_attained(6.0) == "High"

def test_standards_3_5_7_BOD_Poor(standards_3_5_7_bod):
    assert standards_3_5_7_bod.check_wfd_standard_attained(19) == "Poor"

# Tests for NH3 Standards against river types 3,5,7
def test_standards_3_5_7_NH3_Moderate(standards_3_5_7_nh3):
    assert standards_3_5_7_nh3.check_wfd_standard_attained(2) == "Moderate"

def test_calc_impact_score(standards_1_2_4_6_bod):

    """
    GIVEN a WFD_Standards object
    WHEN providing a in class percentage deterioration
    THEN return the expected impact score in line with table 7 of SOAF guide
    """
    assert standards_1_2_4_6_bod.calc_impact_score(0) == 5
    standards_1_2_4_6_bod.calc_impact_score(10) == 5
    assert standards_1_2_4_6_bod.calc_impact_score(10.5) == 15
    assert standards_1_2_4_6_bod.calc_impact_score(25) == 15
    assert standards_1_2_4_6_bod.calc_impact_score(25.5) == 25
    assert standards_1_2_4_6_bod.calc_impact_score(50) == 25
    assert standards_1_2_4_6_bod.calc_impact_score(50.5) == 35
    assert standards_1_2_4_6_bod.calc_impact_score(75) == 35
    assert standards_1_2_4_6_bod.calc_impact_score(75.5) == 45


def test_score_and_stds_attained_3_5_7_BOD_High(standards_3_5_7_bod):

    """
    GIVEN a WFD_Standards object configured for BOD of a 3,5,7 river
    WHEN providing pre and post spill 99 percentiles of bod
    THEN return the expected pre and post spill standards, in class percentage deterioration and impact score
    in line with table 7 of SOAF guide
    """

    pre_spill_bod_wfd_std_attained, post_spill_bod_wfd_std_attained, in_class_bod_percentage_deteriotation, score = standards_3_5_7_bod.score_and_stds_attained(12.73, 12.77)

    assert pre_spill_bod_wfd_std_attained == "Moderate"
    assert post_spill_bod_wfd_std_attained == "Moderate"
    assert in_class_bod_percentage_deteriotation == 1.33
    assert score == 5
