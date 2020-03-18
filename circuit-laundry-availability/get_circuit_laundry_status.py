"""Circuit Laundry Appliance Status Monitor.

This module provides a status monitor solution for Circuit Laundry locations.
The availability of washers and dryers is reported back to the user for a 
given site.

Example:
	$ python3 get_circuit_laundry_status.py

Your site ID must be defined on line 25. This can be found in the URL when 
looking at a sites availability through the typical web interface.

"""

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options

# DEFINE SITE ID HERE
SITE_ID = None



def format_circuit_site_url(site_id):
	"""Generates a URL for a Circuit Laundry Site ID

	Args:
		site_id (int): the Circuit Laundry Site ID

	Returns:
		str: a URL for the Circuit View of a given Circuit site

	"""
	return f'https://www.circuit.co.uk/circuit-view/laundry-site/?site={site_id}'

def move_to_list_view():
	"""Clicks the list view button if present."""
	try:
	    list_view_button = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/section/div[3]/div/div[2]/div[1]/div/button[2]")))
	    list_view_button.click()
	except TimeoutException:
	    print("Loading list view took too much time!")

def move_to_gui_view():
	"""Clicks the GUI view button if present."""
	gui_view_button = browser.find_element_by_xpath("/html/body/div[1]/section/div[3]/div/div[2]/div[1]/div/button[1]")
	gui_view_button.click()

def get_site_name():
	"""Returns the Circuit Laundry Site Name from the webpage.

	Returns:
		str: the name of the Circuit site

	"""
	return browser.find_element_by_xpath("/html/body/div[1]/section/div[3]/div/div[1]/div/h4").text

def get_availability_summary():
	"""Returns the Appliance Availability Summary from the webpage.

	Returns:
		str: the HTML code for the availability summary

	"""
	try:
	    return WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/section/div[3]/div/div[2]/div[2]/div/div[2]/div"))).get_attribute('innerHTML')
	except TimeoutException:
	    print("Loading summary list took too much time!")



def get_washers():
	"""Returns the accordion of Washing Machines shown in the list view of the webpage.

	Returns:
		str: the HTML code for the Washing Machine list

	"""
	try:
	    return WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/section/div[3]/div/div[2]/div[2]/div/div[2]/div[2]/div[2]/div[2]/div[4]/div/div'))).get_attribute('innerHTML')
	except TimeoutException:
	    print("Loading washers list view took too much time!")

def get_dryers():
	"""Returns the accordion of Drying Machines shown in the list view of the webpage.

	Returns:
		str: the HTML code for the Drying Machine list

	"""
	try:
	    return WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/section/div[3]/div/div[2]/div[2]/div/div[2]/div[2]/div[1]/div[2]/div[4]/div/div'))).get_attribute('innerHTML')
	except TimeoutException:
	    print("Loading dryers list view took too much time!")

def print_site_details():
	"""Outputs the Site Name and ID."""
	print("%s (Site ID %d)\n" % (get_site_name(), SITE_ID))

def print_availability_summary(availability_summary_html):
	"""Outputs both the Washer and Dryer Availability Counts

	Args:
		availability_summary_html (str): the HTML code for the site summary

	"""
	soup = BeautifulSoup(availability_summary_html, "html.parser") # create beautiful soup object
	print(soup.findAll("div")[0].text.replace('\n',' ')) # print washer availability count
	print(soup.findAll("div")[1].text.replace('\n',' ')) # print dryer availability count

def print_all_appliance_information(accordion_html, type):
	"""Outputs the Status and Time Remaining for each Appliance in an Accordion

	Args:
		accordion_html (str): the HTML code for the accordion to print information about
		type (str): the name of the appliance to be printed

	"""
	soup = BeautifulSoup(accordion_html, "html.parser") # create beautiful soup object
	appliances = soup.findAll("div", {"class": "accordion"})

	if appliances != None:
		print_appliance_table_header(type)
		for appliance in appliances:
			appliance_id = appliance.find("div")['data-appliance']
			appliance_status = appliance.find("p").find("strong").text.strip()
			appliance_time_remaining = appliance.find("div").find("div", {"class": "time-remaining"}).text.strip()

			print_appliance_information(appliance_id, appliance_status, appliance_time_remaining)
	else:
		print("No appliances found!")
		
def print_appliance_table_header(type):
	"""Outputs a table header when displaying the state of multiple appliances.

	Args:
		type (str): the name of the appliance to be printed

	"""
	print("\n### Status of All %ss ###\n" % type)
	print("ID \t Status    \tTime Remaining\n")

def print_appliance_information(id, status, time_remaining):
	"""Outputs the Status and Time Remaining for a Single Appliance

	Args:
		id (int): the ID of the appliance
		status (str): the status of the appliance
		time_remaining(str): the time remaining for the appliance

	"""
	print("%3d\t%10s\t%s" % (int(id), status, time_remaining))

def print_laundry_status():
	"""Outputs a sites full details along with full availability details."""
	print_site_details()
	print_availability_summary(get_availability_summary())
	move_to_list_view()
	print_all_appliance_information(get_washers(), 'Washer')
	print_all_appliance_information(get_dryers(), 'Dryer')


URL = format_circuit_site_url(SITE_ID)
delay = 5 # seconds

options = Options()
options.headless = True # should run in background
browser = webdriver.Chrome(options=options)

browser.get(URL)

print_laundry_status()

browser.quit()