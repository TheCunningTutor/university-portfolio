# DuckWeb Schedule Adder

A python script to add a student's class schedule (from [DuckWeb](https://duckweb.uoregon.edu/)) to their Google Calendar account.

## Usage
Simply run `main.py` (requires Python 3) and follow the prompts to log into duckweb and choose the term you'd like to add. Getting the classes from DuckWeb should work for you, but unfortunately Google's authorization system still has this project classified as a test project, so it may not work with your Google account; if this is the case you may contact me at [thecunningtutor@gmail.com](mailto:thecunningtutor@gmail.com) to ask me to add your email manually. I don't mind! Otherwise your classes probably won't be able to be added to your calendar.

## About
I created this project while studying at the University of Oregon. Along the way I learned a lot about web scraping (to get classes from DuckWeb's very outdated website) and APIs (to add classes to Google Calendar).

## Demonstration
Copied from a test run in my own Linux terminal (my one class wasn't added because it's already in my calendar):

```bash
python3 main.py 
Enter term in the format <term> <year> (e.g. 'spring 2022'): fall 2022
please enter your duck ID number: 951*******
please enter your duckweb PIN: 
Login successful!
Finding classes...
Found course Intro to Networks
Please visit this URL to authorize this application: https://accounts.google.com/o/oauth2/...
Enter calendar name (or press enter for default): classes
Calendar found!
Adding courses...
Course CS 432 - Intro to Networks already in calendar and won't be added
All courses added! Please check your calendar to ensure everything was added correctly!
```

