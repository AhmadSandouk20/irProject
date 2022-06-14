from dateutil import parser
# r for escaping \ and f for escaping {}
from datetime import datetime
import re

months = re.compile(r"\s(October|February|December|May|June|July|August|March|January|Septemper|November|April)")
year = re.compile(r"\s*19\d{2}\s*")
day = re.compile(r"(\s*\d,\s*)|(\s*\d{2},\s*)")
hour = re.compile(r"(\s*\d\s*):|(\s*\d{2}\s*):")
minute = re.compile(r":(\s*\d\s*)|:(\s*\d{2}\s*)")

# January 20, 1978  10:56 AM
date_format_one = re.compile(rf"{months.pattern}"r"\s*\d{2}\s*,?\s*\d{4}\s*\d*\s*:\s*\d{2}\s*(AM|PM)\s*")

# October 31, 1969
date_format_two = re.compile(rf"{months.pattern}"r"\s*\d{2}\s*,\s*\d{4}\s*")
# January, 1972 || January 1972
date_format_three = re.compile(rf"{months.pattern}"r"\s*,?\s*\d{4}")

date_format = re.compile(
    rf"{date_format_one.pattern}|"
    rf"{date_format_two.pattern}|"
    rf"{date_format_three.pattern}|"
    r"(\s*\d{4}\s*)"
)


# def date_to_timestamp(date):
#     parsed_date = parser.parse(date)
#     print("parsed_date ", parsed_date)
#     stamped_date = parsed_date.timestamp()
#     print("stamp ", stamped_date)
#     return stamped_date


def extract_and_stamp_date(text_with_date):
    stamped_date = []

    matches = date_format.finditer(text_with_date)
    if matches and matches is not None:
        for match in matches:
            # adding to the stamped_date
            matched_date = match.group()
            stamped_date.append(date_to_timestamp(matched_date))

            # deleting date from the text( we don't want it to enter the text_processing)
            text_with_date = text_with_date.replace(match.group(), "")

        # removing the none or the empty values
        stamped_date = [stamped for stamped in stamped_date if stamped]

    return stamped_date, text_with_date


def date_to_timestamp(date):
    # here i have single date format but the finditer returns a callable iterator so i have to loop

    matches = date_format_one.finditer(date)
    if matches:
        for match in matches:
            matched_date = str(match.group())
            print('date one ', matched_date)
            date_time_object_day = day.search(matched_date).group().strip().replace(',', '')
            date_time_object_year = year.search(matched_date).group().strip()
            # %B gets the month name as full , .month gets the month as integer
            date_time_object_month = datetime.strptime(months.match(matched_date).group().strip(), "%B").month
            date_time_object = datetime(int(date_time_object_year), date_time_object_month,
                                        int(date_time_object_day))
            # rolling on the timestamp before 1970 issue
            return (date_time_object - datetime(1970, 1, 1)).total_seconds()

    matches = date_format_two.finditer(date)
    if matches:
        for match in matches:
            matched_date = str(match.group())
            print('date two ', matched_date)
            date_time_object_day = day.search(matched_date).group().strip().replace(',', '')
            date_time_object_year = year.search(matched_date).group().strip()
            # %B gets the month name as full , .month gets the month as integer
            date_time_object_month = datetime.strptime(months.match(matched_date).group().strip(), "%B").month
            # print('full date ', date_time_object_year, " ", date_time_object_month, " ", date_time_object_day)
            date_time_object = datetime(int(date_time_object_year), date_time_object_month,
                                        int(date_time_object_day))
            # print('date_time_object ', date_time_object)
            return (date_time_object - datetime(1970, 1, 1)).total_seconds()

    matches = date_format_three.finditer(date)
    if matches:
        for match in matches:
            matched_date = str(match.group())
            print('date three ', matched_date)
            # %B gets the month name as full , .month gets the month as integer
            date_time_object_month = datetime.strptime(months.match(matched_date).group().strip(), "%B").month
            date_time_object_year = year.search(matched_date).group().strip()
            # print('full date ', date_time_object_year)
            date_time_object = datetime(int(date_time_object_year), date_time_object_month, 1)
            # print('date_time_object ', date_time_object)
            return (date_time_object - datetime(1970, 1, 1)).total_seconds()

    matches = year.finditer(date)
    if matches:
        for match in matches:
            matched_date = str(match.group())
            print('just year ', matched_date)
            date_time_object_year = year.search(matched_date).group().strip()
            # print('full date ', date_time_object_year)
            date_time_object = datetime(int(date_time_object_year), 1, 1)
            # print('date_time_object ', date_time_object)
            return (date_time_object - datetime(1970, 1, 1)).total_seconds()

# matches = date_format_two.finditer(date)
# for match in matches:
#     datetime_object = datetime.strptime(months.match(match.group()).group(), "%B")
#     print(datetime_object)
#
# print(do_thing(date))

# Libbey and Zaltman, 1967, || Paisley, 1968; || Storer, 1968,
# date_format_seven = re.compile(r"[A-Z][a-z]+\s*(and [A-Z][a-z]+)?,\s+\d{4}")

# 1965 and 1966 || 1965-1966
# date_format_eight = re.compile(r"\d{4}\s*(-|and)\s*\d{4}")


# August-November 1969 || October and November 1959
# date_format_two = re.compile(rf"{months.pattern}"r"\s*(-|and)\s*"rf"{months.pattern}"r"\s*\d{4}")

# July 1969-June 1970 || November 1969 - April 1970
# date_format_three = re.compile(rf"{months.pattern}"r"\s+\d{4}\s*(-|and)\s*"rf"{months.pattern}" + r"\s+\d{4}")

# April 1970 and 1555
# date_format_four = re.compile(rf"{months.pattern}"r"\s+\d{4}\s+and\s+\d{4}")

# March 15 to June 31, 1971 || (November 19 -December 18, 1970)
# date_format_five = re.compile(
# rf"{months.pattern}"r"\s+\d{2}\s+(to|and|-)\s*"rf"{months.pattern}"r"\s*\d{2}\s*,\s*\d{4}")
