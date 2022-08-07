"""Get Classes From Duckweb

AUTHOR: Cameron Cunningham

DESCRIPTION: Uses webscraping techniques and the BeautifulSoup module to get a
list of classes and associated information from duckweb (duckweb.uoregon.edu).

Note that only fall, winter, and spring terms are supported -- summer gets
weird.

Defines the class UniClass for storing scheduling information.
"""

from datetime import date
from datetime import datetime
from datetime import timedelta
from getpass import getpass

import requests
from bs4 import BeautifulSoup

months = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
          "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}
DAYS = {"M": "MO", "T": "TU", "W": "WE", "R": "TH", "F": "FR"}
DAYSOFFSET = {
    "M": timedelta(days=0),
    "T": timedelta(days=1),
    "W": timedelta(days=2),
    "R": timedelta(days=3),
    "F": timedelta(days=4)
}


class UniClass:
    """A class used to store scheduling information regarding a university course

        ...


    Attributes
    ----------
    course : str
        the field and number of the course (e.g. CIS 410)
    description : str
        the title of the class (e.g. Multi-Agent Systems)
    days : str
        the days of the week on which the course will be held
    startTime : datetime
        the time of the first class (start day and time)
    endTime : datetime
        the ending time of the last class (on the last day)
    year : str
    Methods
    -------
    genEnd()
        Generates a string representing the last hour of the first day
    generateRecurrence(frequency="WEEKLY")
        Returns a string encoding how the class repeats; see google calendar's
        documentation for more info
    """

    def __init__(self, course, title, startDate, endDate, year, days, times):
        """

        Args:
            course : str
                the course code, e.g. "CIS 410"
            title : str
                course title, e.g. "Multi-Agent Systems"
            startDate : str
                start date of the class in <month> <date>, <year> format,
                e.g. "Sep 27, 2022"
            endDate : str
                end date of class in same format as startDate
            year : str
                the year the class will take place
            days : str
                days of the week the course will be held following duckweb
                format, e.g. "MW" for Monday and Wednesday
            times : str
                times the course will be held, in the format
                "<start time>am/pm - <end time>am/pm", e.g. "3:30pm - 4:30pm"
        """
        # Add course title
        self.course = course
        if title == "+ Dis":
            self.course += " discussion/lab"
            self.description = self.course
        else:
            self.description = title

        # parse times
        start = startDate.split()
        end = endDate.split()
        times = times.split()
        startT = times[0].split(":")
        startHour = int(startT[0])
        startMinute = int(startT[1][:2])
        startTOD = startT[1][-2:]
        if startTOD == "pm" and startHour != 12:
            startHour += 12
        endT = times[2].split(":")
        endHour = int(endT[0])
        endMinute = int(endT[1][:2])
        endTOD = endT[1][-2:]
        if endTOD == "pm" and endHour != 12:
            endHour += 12

        startDate = date(int(start[2]), months[start[0]], int(start[1].strip(",")))
        endDate = date(int(end[2]), months[end[0]], int(end[1].strip(",")))

        # set the rest of the object attributes
        self.days = days
        self.startTime = datetime(startDate.year, startDate.month,
                                  startDate.day, hour=startHour, minute=startMinute)
        self.startTime += DAYSOFFSET[self.days[0]]
        self.endTime = datetime(endDate.year, endDate.month, endDate.day,
                                hour=endHour, minute=endMinute)
        self.year = year

    def __str__(self):
        return f"course: {self.course}\nfrom {self.startTime} to " \
               f"{self.endTime}\nfrom {self.startTime} to " \
               f"{self.endTime}\ndays: {self.days}"

    def genEnd(self):
        return f"{self.startTime.date()}T{self.endTime.time()}"

    def generateRecurrence(self, frequency="WEEKLY"):
        """
        Generates recurrence code for adding the class to Google Calendars

        :param frequency: Default value = "WEEKLY"

        """
        rv = "RRULE:FREQ=" + frequency
        rv += ";UNTIL=" + self.year
        monthStr = str(self.endTime.month)
        if len(monthStr) == 1:
            monthStr = "0" + monthStr
        dayStr = str(self.endTime.day)
        if len(dayStr) == 1:
            dayStr = "0" + dayStr
        rv += monthStr + dayStr
        rv += "T080000Z"
        rv += ";INTERVAL=1"
        rv += ";BYDAY="
        count = len(self.days)
        days = self.days
        while count > 1:
            rv += DAYS[days[0]] + ","
            days = days[1:]
            count -= 1
        rv += DAYS[days[0]]
        return rv


"""Uncomment the following lines for a test/example UniClass instance"""
# x = UniClass("CIS 314",
#              "+ Dis", "Sep 29, 2020", "Dec 06, 2020", "2020", "M", "3:30pm - 4:30pm")
# print(x.__dir__())
# print(x.endTime)
# print(x.startTime.isoformat())
# print(f"{x.startTime.date()}T{x.startTime.time()}")
# print(x.endTime.isoformat())
# print(x.genEnd())

def get_classes():
    """ """
    cookies = {
        'TESTID': 'set',
    }

    # prompt user for term (only quarter system supported, no semesters)
    while 1:
        term = input("Enter term in the format <term> <year> (e.g. 'spring 2022'): ")
        rawTerm = term.split(" ")
        if len(rawTerm) == 2:
            season = rawTerm[0].lower()
            year = rawTerm[1]
            break
        else:
            print("invalid format, please try again")
    termID = None
    if season == "fall":
        termID = year + "01"
    elif season == "winter":
        termID = str(int(year) - 1) + "02"
    elif season == "spring":
        termID = str(int(year) - 1) + "03"
    elif season == "summer":
        raise NotImplementedError("Summer not supported yet, sorry!")
    else:
        print("Input not recognized, please try again")
        quit()
    post_params = {"term_in": termID}

    # prompt user for login info
    id_num = input("please enter your duck ID number: ")
    PIN = getpass(prompt="please enter your duckweb PIN: ")
    duckweb_login = {
        'sid': id_num,
        'PIN': PIN
    }

    # attempt to log in to duckweb
    url = "https://duckweb.uoregon.edu/duckweb/twbkwbis.P_ValLogin"
    ses = requests.Session()
    response = ses.post(url, data=duckweb_login, cookies=cookies)

    # load course scheule page using prompted term
    page = ses.post("https://duckweb.uoregon.edu/duckweb/bwskcrse.P_CrseSchdDetl",
                    data=post_params)
    soup = BeautifulSoup(page.content, 'html.parser')

    courses = []

    if page:
        print("Login successful!")
        # we want the table with courses, so we get all tables from the page
        # and search through them for the one we want
        result = soup.find(class_="pagebodydiv")
        tables = result.find_all('table', class_='datadisplaytable')
        class_table = None
        for table in tables:
            if table.find('th', class_='ddheader'):
                class_table = table
        if class_table is None:
            raise Exception("ERROR: table not found")
        # now we have found the table we want, so get classes from it and add
        # them to the course list
        lines = class_table.find_all('tr')
        print("Finding classes...")
        for line in lines:
            cells = line.find_all('td')
            datas = []
            for cell in cells:
                datas.append(cell.text.strip())
            if len(datas) > 0 and datas[0] != '':
                courses.append(UniClass(
                    datas[1],
                    datas[2],
                    datas[6],
                    datas[7],
                    year,
                    datas[8],
                    datas[9]))
                print(f"Found course {datas[2]}")
        return courses
    else:
        print("Page not found, please try again.")
        return None


if __name__ == "__main__":
    courses = get_classes()
