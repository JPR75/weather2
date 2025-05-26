from datetime import datetime


#------------------------------------------------------------------------------
# Calculate the moon phase from a known new moon
#------------------------------------------------------------------------------
class moon_phase () :
    """Calculate the moon phase from a known new moon"""

    def __init__(self) :
        new_moon_year = 2025
        new_moon_month = 4
        new_moon_day = 27
        new_moon_date = datetime(new_moon_year, new_moon_month, new_moon_day)
        self.new_moon_julian_day = self.to_julian_day(new_moon_date)

    def to_julian_day (self, date) :
        """Convert the day to Julian"""
        a = (14 - date.month) // 12
        y = date.year + 4800 - a
        m = date.month + 12 * a - 3
        return (
            date.day + ((153 * m + 2) // 5) + 365 * y + y // 4 - y // 100 + y // 400 - 32045
        )

    def get_moon_phase (self) :
        """Get today moon phase"""
        julian_day = self.to_julian_day(datetime.now())
        delta_day = julian_day - self.new_moon_julian_day
        moon_phase = delta_day % 29.53059
        moon_section = 29.53059 / 16

        if moon_phase >= int(moon_section) and moon_phase < int(moon_section * 3) :
            moon_state = 0
        elif moon_phase >= int(moon_section * 3) and moon_phase < int(moon_section * 5) :
            # First quater
            moon_state = 1
        elif moon_phase >= int(moon_section * 5) and moon_phase < int(moon_section * 7) :
            moon_state = 2
        elif moon_phase >= int(moon_section * 7) and moon_phase < int(moon_section * 9) :
            # Full moon
            moon_state = 3
        elif moon_phase >= int(moon_section * 9) and moon_phase < int(moon_section * 11) :
            moon_state = 4
        elif moon_phase >= int(moon_section * 11) and moon_phase < int(moon_section * 13) :
            # Third quarter
            moon_state = 5
        elif moon_phase >= int(moon_section * 13) and moon_phase < int(moon_section * 15) :
            moon_state = 6
        elif moon_phase >= int(moon_section * 15) or moon_phase > 0 :
            # New moon
            moon_state = 7

        return moon_state
