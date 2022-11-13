import calendar
import time


def parse_kickoff_string(start_date_socc_string):
    return calendar.timegm(time.strptime(start_date_socc_string, '%Y-%m-%dT%H:%M:%S'))
