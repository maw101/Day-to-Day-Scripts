import datetime

def get_time_sum():
	time_list = []

	number_of_times = int(input("Enter Number of Times to Input (format: HH:MM): "))

	for i in range(0, number_of_times):
		time_list.append(input("Enter Next Time: "))

	total_minutes = 0
	for tm in time_list:
	    time_parts = [int(s) for s in tm.split(':')]
	    total_minutes += time_parts[0] * 60 + time_parts[1]

	return total_minutes

def format_total_minutes(total_minutes):
	hours = total_minutes // 60 # take floor
	minutes = total_minutes - (hours * 60)

	return (hours, minutes)

def print_hours_minutes(hours, minutes):
	print("%d:%02d" % (hours, minutes))

def print_wordy_hours_minutes(hours, minutes):
	print("%d hours %d minutes" % (hours, minutes))

total_minutes = get_time_sum()
hours, minutes = format_total_minutes(total_minutes)

print_hours_minutes(hours, minutes)
print_wordy_hours_minutes(hours, minutes)