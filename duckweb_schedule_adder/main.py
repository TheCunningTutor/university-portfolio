""" Driver for Duckweb Class Schedule Automation
AUTHOR: Cameron Cunningham

DESCRIPTION: Uses get_classes.py and cal_setup.py to add a user's class
schedule from duckweb.uoregon.edu to their Google Calendar.

Simply run with python (e.g. python3 main.py) and the script prompts the user
for all relevant information and credentials.
"""
import sys

from cal_setup import get_calendar_service
from get_classes import get_classes


def main():
    # get classes from duckweb
    courses = get_classes()

    # set up google calendar API
    service = get_calendar_service()

    # get list of calendars
    calendars_result = service.calendarList().list().execute()
    calendars = calendars_result.get('items', [])
    if not calendars:
        sys.exit("Error: no calendars found")

    # find the calendar to add classes to
    calID = ""
    # get calendar name
    cal_name = input("Enter calendar name (or press enter for default): ")
    while calID == "":
        for calendar in calendars:
            # search existing calendars for entered name
            primary_cond = (cal_name == '' and calendar.get('primary'))
            if cal_name == calendar['summary'] or primary_cond:
                calID = calendar['id']
        if calID == '':
            cal_name = input("Calendar not found, please try again: ")
    print("Calendar found!")

    # get existing calendar events to avoid adding duplicates
    min_date = courses[0].startTime
    max_date = courses[0].endTime
    for course in courses:
        if course.startTime < min_date:
            min_date = course.startTime
        if course.endTime > max_date:
            max_date = course.endTime
    min_date = min_date.isoformat() + "-08:00"
    max_date = max_date.isoformat() + "-08:00"
    events = service.events().list(calendarId=calID,
                                   timeMax=max_date, timeMin=min_date).execute()
    # existing is a list of tuples of the form (summary, description)
    existing = []
    for event in events['items']:
        if ('summary' in event) and ('description' in event):
            existing.append((event['summary'], event['description']))

    print("Adding courses...")
    for course in courses:
        if (course.course, course.description) in existing:
            print(f"Course {course.course} - {course.description} already"
                  f" in calendar and won't be added")
        else:
            print(f"Adding course {course.course}...")
            event = {
                "summary": course.course,
                "description": course.description,
                "start": {"dateTime": course.startTime.isoformat(),
                          "timeZone": 'America/Los_Angeles'},
                "end": {"dateTime": course.genEnd(),
                        "timeZone": 'America/Los_Angeles'},
                "recurrence": [
                    course.generateRecurrence()
                ],
            }

            service.events().insert(calendarId=calID, body=event).execute()
    print("All courses added! Please check your calendar to ensure everything" \
                " was added correctly!")


if __name__ == '__main__':
    main()
