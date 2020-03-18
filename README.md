# Day-to-Day-Scripts
A (limited) collection of small day to day scripts

## [aber-su-log-volunteer-hours](/aber-su-log-volunteer-hours)
A small Python script to provide an automated solution to logging volunteer hours to the Aberystwyth University Student's Union system. 

Activities are defined in a CSV file and the program automatically submits these using the submission form.

Submitted hours are placed in a separate file for logging and the original file is overwritten. Spam prevention is integrated into the project through program pausing for a randomised user-defined time in seconds between form submissions.

![](aber-su-log-volunteer-hours/log_hours_in_use.gif)
![](aber-su-log-volunteer-hours/log_hours_in_use_terminal.png)

## [circuit-laundry-availability](/circuit-laundry-availability)

Provides a status monitor for Circuit Laundry locations. The availability of washers and dryers is reported back to the user for a given site.

### Example Output:
```
$ python3 get_circuit_laundry_status.py 
Penglais Farm (Site ID 6390)

 04 Washers Available 
 05 Dryers Available 

### Status of All Washers ###

ID 	 Status    	Time Remaining

  2	 available	
  4	    in use	17 mins
  6	      idle	
  8	 available	
 10	    in use	17 mins
 12	 available	
 14	    in use	16 mins
 16	 available	

### Status of All Dryers ###

ID 	 Status    	Time Remaining

  1	    in use	29 mins
  3	 available	
  5	 available	
  7	    in use	45 mins
  9	 available	
 11	    in use	36 mins
 13	 available	
 15	 available	
```

## [hours-minutes-sum](/hours-minutes-sum)
A small Python script to take input of a set number of times in a HH:MM format and sums these together, outputting the resulting time. Utilised for manual time addition.

