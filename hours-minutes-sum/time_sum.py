import datetime

time_list = []

number_of_times = int(input("Enter Number of Times to Input (format: HH:MM): "))

for i in range(0, number_of_times):
	time_list.append(input("Enter Next Time: "))

total_minutes = 0
for tm in time_list:
    time_parts = [int(s) for s in tm.split(':')]
    total_minutes += time_parts[0] * 60 + time_parts[1]

print(str(datetime.timedelta(minutes=total_minutes)))
