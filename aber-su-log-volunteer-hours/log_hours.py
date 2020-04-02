"""Aberystwyth University SU Volunteer Hours Automatic Time Logger.

This module provides an automated solution to logging volunteer hours to the 
Students Union system. Activities are defined in a CSV file and the program 
automatically submits these using the submission form.

Submitted hours are placed in a separate file for logging and the original file 
is overwritten. Spam prevention is integrated into the project through 
sleeping for a randomised user-defined time in seconds between form submissions.

Requirements:
	selenium
	chrome webdriver

Example:
	$ python3 log_hours.py
	
"""

import getpass, time, csv, datetime, random

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

# URL for entering hours
URL = 'https://c4esh253.caspio.com/dp/73335000e17d675c8ae147a4b7fc' 
# USERNAME to be used in the login form
USERNAME = ''

def login_if_required():
	"""Logs in to the log site if on the login page.

	Returns:
		bool: The status of the functions execution. True for success, False otherwise.
	
	"""
	try:
		username_field = browser.find_element_by_name('xip_UniID')
		password_field = browser.find_element_by_name('xip_Password')
		login_submit_button = browser.find_element_by_name('xip_datasrc_Volunteer_register')
	except NoSuchElementException:
		print("It doesn't appear that this is the login page. One or more fields could not be found on the page.")
		return False

	PASSWORD = getpass.getpass("Enter Form Password: ")

	username_field.send_keys(USERNAME)
	password_field.send_keys(PASSWORD)

	login_submit_button.click()

	PASSWORD = None # no longer require password so discard
	return True


def add_activity(activity, date, hours, skills_gained='', skills_explanation=''):
	"""Completes the add activity form for a given activity.

	Args:
		activity (str): the activity description
		date (str): a date in the format DD/MM/YYYY
		hours (float): the number of hours the activity took
		skills_gailed (str, optional): a String stating any skills gained. 
			Defaults to blank String.
		skills_explanation (str, optional): a String explaining how any 
			listed skills were gained. Defaults to a blank String.

	Returns:
		bool: The status of the functions execution. True for success, False otherwise.
	
	"""
	try:
		activity_field = browser.find_element_by_name('InsertRecordVolunteeractivity')
		date_field = browser.find_element_by_name('InsertRecordDateofactivity')
		total_hours_field = browser.find_element_by_name('InsertRecordHoursrecorded')
		skills_gained_field = browser.find_element_by_name('InsertRecordSkills')
		skills_gained_how_field = browser.find_element_by_name('InsertRecordskills_gained_how')

		submit_button = browser.find_element_by_name('Submit')
	except NoSuchElementException:
		print("One or more fields could not be found on the page")
		return False

	# enter data into each field
	activity_field.send_keys(activity)
	date_field.send_keys(date)
	total_hours_field.send_keys(hours)
	skills_gained_field.send_keys(skills_gained)
	skills_gained_how_field.send_keys(skills_explanation)

	sleep_for_random_time(TIME_BETWEEN_REQUESTS_LOWER_BOUND, TIME_BETWEEN_REQUESTS_UPPER_BOUND)

	submit_button.click()

	print("\tSubmitted Activity")
	return True

def process_csv_hours(filename):
	"""Processes a CSV file of activities, adding each to the log.

	Args:
		filename (str): the name of the file containing the activities we wish 
			to add to the log

	Returns:
		bool: The status of the functions execution. True for success, False 
			otherwise.
	
	"""
	print("Processing all rows in CSV")

	with open(filename, 'r') as file:
		reader = csv.reader(file)
		header = next(reader)
		# check file as empty
		if header != None:
			# iterate over each row after the header
			for row in reader:
				add_activity(row[0], uk_date_to_us_format(row[1]), row[2], row[3], row[4])
				write_processed_activity_to_csv(row, filename)
		else:
			print("Header Missing in Input CSV")

	print("All rows in CSV processed")
	# overwrite file
	with open(filename, 'w') as file:
		file.write("Activity,UK Date,Hours,Skills Gained,How Gained/Developed Skills")

def write_processed_activity_to_csv(activity_row, read_from_filename):
	"""Writes an activity that was added to a given CSV file.

	Args:
		activity_row: list containing activity details
		read_from_filename (str): the name of the file we read the activity from
	
	"""
	write_to_filename = read_from_filename[:-4] + '_processed.csv'
	with open(write_to_filename, 'a') as file:
		# write activity to file excluding all square bracket and single quote characters
		file.write('\n' + str(activity_row).replace('[', '').replace("\'", '').replace("]", ''))

def sleep_for_random_time(min, max):
	"""Pauses the program for a random time within bounds.

	Args:
		min (int): the minimum time in seconds to pause execution for
		max (int): the maximum time in seconds to pause execution for
	
	"""
	time_to_sleep = random.randrange(min, max)
	print("\tSleeping for ", time_to_sleep, " Seconds")
	time.sleep(time_to_sleep)
			
def uk_date_to_us_format(uk_date):
	"""Converts a UK date (DD/MM/YYYY) into a US date format (MM/DD/YYYY).

	Args:
		uk_date (str): a UK formatted date (DD/MM/YYYY format) string 

	Returns:
		str: A US formatted date (MM/DD/YYYY format) of the UK date provided 
			(in DD/MM/YYYY format)

	"""
	return datetime.datetime.strptime(uk_date, '%d/%m/%Y').strftime('%m/%d/%Y')

print("To prevent spamming the SU form, a time delay should be set in between form submissions:")
TIME_BETWEEN_REQUESTS_LOWER_BOUND = int(input("\tEnter the LOWER BOUND for the number of seconds between form submissions (in seconds): "))
TIME_BETWEEN_REQUESTS_UPPER_BOUND = int(input("\tEnter the UPPER BOUND for the number of seconds between form submissions (in seconds): "))

# ensure that upper bound is greater than lower bound, can't be equal due to random call
if TIME_BETWEEN_REQUESTS_UPPER_BOUND <= TIME_BETWEEN_REQUESTS_LOWER_BOUND:
	TIME_BETWEEN_REQUESTS_UPPER_BOUND = TIME_BETWEEN_REQUESTS_LOWER_BOUND + 1

BROWSER = webdriver.Chrome()

BROWSER.get(URL)
login_if_required()
process_csv_hours('hours.csv')

BROWSER.quit()
