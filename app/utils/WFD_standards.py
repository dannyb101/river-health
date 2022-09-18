# All standards can be found on page 16 of: http://www.fwr.org/UPM3/Section2.pdf

from app.Connections.db_standards import DB_WFD_STANDARDS

class WFD_Standards:
    """
    Standards class which models the BOD and NH3 99 Percentile standards for WFD status based on river type
    Keyword arguments required to avoid developer mistakes
    """
    def __init__(self, *,is_1_2_4_6: bool, is_bod: bool):

        connection = DB_WFD_STANDARDS()
      
        if is_1_2_4_6 and is_bod:
            self.high = connection.get_latest_standard("1_2_4_6", "high", "bod")
            self.good = connection.get_latest_standard("1_2_4_6", "good", "bod")
            self.moderate = connection.get_latest_standard("1_2_4_6", "moderate", "bod")
            self.poor = connection.get_latest_standard("1_2_4_6", "poor", "bod")
        elif is_1_2_4_6 and not is_bod:
            self.high = connection.get_latest_standard("1_2_4_6", "high", "nh3")
            self.good = connection.get_latest_standard("1_2_4_6", "good", "nh3")
            self.moderate = connection.get_latest_standard("1_2_4_6", "moderate", "nh3")
            self.poor = connection.get_latest_standard("1_2_4_6", "poor", "nh3")
        elif not is_1_2_4_6 and is_bod:
            self.high = connection.get_latest_standard("3_5_7", "high", "bod")
            self.good = connection.get_latest_standard("3_5_7", "good", "bod")
            self.moderate = connection.get_latest_standard("3_5_7", "moderate", "bod")
            self.poor = connection.get_latest_standard("3_5_7", "poor", "bod")
        else:
            self.high = connection.get_latest_standard("3_5_7", "high", "nh3")
            self.good = connection.get_latest_standard("3_5_7", "good", "nh3")
            self.moderate = connection.get_latest_standard("3_5_7", "moderate", "nh3")
            self.poor = connection.get_latest_standard("3_5_7", "poor", "nh3")
    """
    Function which takes in the 99th Percentile value
    and compares it against the WFD standards for river type (3/5/7 or 1/2/4/6) given when class was initalised
    Returns a String containing the rating based on those the standards
    """
    def check_wfd_standard_attained(self, value: float):

        if value <= self.high:
            return "High"
        elif value <= self.good:
            return "Good"
        elif value <= self.moderate:
            return "Moderate"
        elif value <= self.poor:
            return "Poor"
        else:
            return "Bad"
    
    """
    Function which takes the 99 percentile concentration before the spill and the 
    99 percentile concentration after the spill and gives an impact score of the
    spill event. The highest impact score is 45 and the lowest impact score is 5.
    The lower the impact score, the less of an impact the CSO is having on the
    river health. See table 7 of SOAF guide for reference.
    """
    def score_and_stds_attained(self, pre_spill_99: float, post_spill_99: float):

        pre_spill_std_attained = self.check_wfd_standard_attained(pre_spill_99)
        post_spill_std_attained = self.check_wfd_standard_attained(post_spill_99)

        if pre_spill_std_attained != post_spill_std_attained:
            in_class_percentage_deteriotation = 100
        elif pre_spill_std_attained == "High":
            # Upper bound of high std is std.high and lower bound of high std is water with no pollutants
            # i.e. a 99 percentile of zero. Therefore the range is std.high - 0 = std.high
            in_class_percentage_deteriotation = 100 * (post_spill_99 - pre_spill_99)/self.high
        elif pre_spill_std_attained == "Good":
            in_class_percentage_deteriotation = 100 * (post_spill_99 - pre_spill_99)/(self.good - self.high)
        elif pre_spill_std_attained == "Moderate":
            in_class_percentage_deteriotation = 100 * (post_spill_99 - pre_spill_99)/(self.moderate - self.good)
        elif pre_spill_std_attained == "Poor":
            # calculate deterioration within poor class
            in_class_percentage_deteriotation = 100 * (post_spill_99 - pre_spill_99)/(self.poor - self.moderate)
        else:
            # If river quality is so poor as to recieve a bad rating before before a spill, 
            # we will assume that the impact of the cso on it is 0
            in_class_percentage_deteriotation = 0

        score = self.calc_impact_score(in_class_percentage_deteriotation)

        return pre_spill_std_attained, post_spill_std_attained, round(in_class_percentage_deteriotation, 2), score

    """
    Function which uses the in class percentage deterioration to calculate the impact score of a
    CSO. The highest impact score is 45 and the lowest impact score is 5. The lower the impact score,
    the less of an impact the CSO is having on the river health. See table 7 of SOAF guide for reference.
    """
    def calc_impact_score(self, percent_deterioration: float):
        if 0 <= percent_deterioration <= 10:
            impact_score = 5
        elif 10 < percent_deterioration <= 25:
            impact_score = 15
        elif 25 < percent_deterioration <= 50:
            impact_score = 25
        elif 50 < percent_deterioration <= 75:
            impact_score = 35
        else:
            impact_score = 45
        return impact_score