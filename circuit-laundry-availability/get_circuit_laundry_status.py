from selenium import webdriver

# DEFINE SITE ID HERE
SITE_ID = None

def format_circuit_location_url(site_id):
	"""Generates a URL for a Circuit Laundry Site ID"""
	return f'https://www.circuit.co.uk/circuit-view/laundry-site/?site={site_id}'

URL = format_circuit_location_url(SITE_ID)

browser = webdriver.Chrome()

browser.get(URL)

number_of_washers_free = browser.find_element_by_xpath("/html/body/div[1]/section/div[3]/div/div[2]/div[2]/div/div[2]/div/div[1]/span").text

number_of_dryers_free = browser.find_element_by_xpath("/html/body/div[1]/section/div[3]/div/div[2]/div[2]/div/div[2]/div/div[2]/span").text

print("Washers Available:", number_of_washers_free)
print("Dryers Available:", number_of_dryers_free)

browser.quit()