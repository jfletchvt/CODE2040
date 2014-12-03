import json
import requests
import dateutil.parser

def main():

	data = json.dumps({'email':'joevt@vt.edu', 'github':'https://github.com/jfletchvt/CODE2040.git'}) 

	r = requests.post('http://challenge.code2040.org/api/register', data=data)

	token = r.json()['result']

	stage_one(token)
	stage_two(token)
	stage_three(token)
	stage_four(token)

# Stage I: Reverse a string
def stage_one(token):

	url = 'http://challenge.code2040.org/api/getstring'

	r = requests.post(url, data=json.dumps({'token':token}))

	string = r.json()['result']

	rev_string = string[::-1]

	url = 'http://challenge.code2040.org/api/validatestring'

	r = requests.post(url, data=json.dumps({'token':token,'string':rev_string}))

	print(r.text)

# Stage II: Needle in a haystack
def stage_two(token):

	url = 'http://challenge.code2040.org/api/haystack'

	r = requests.post(url, data=json.dumps({'token':token}))

	data = r.json()['result']

	needle = data['needle']

	haystack = data['haystack']

	pos = -1

	for x in range(len(haystack)):
		if haystack[x] == needle:
			pos = x
			break

	url = 'http://challenge.code2040.org/api/validateneedle'

	r = requests.post(url, data=json.dumps({'token':token,'needle':pos}))

	print(r.text)

# Stage III: Prefix
def stage_three(token):
	
	url = 'http://challenge.code2040.org/api/prefix'

	r = requests.post(url, data=json.dumps({'token':token}))

	data = r.json()['result']
	prefix = data['prefix']
	array = data['array']

	size = len(prefix)

	new_array = []

	for x in xrange(len(array)):
		if(not array[x].startswith(prefix)):
			new_array.append(array[x])

	url = 'http://challenge.code2040.org/api/validateprefix'

	r = requests.post(url, data=json.dumps({'token':token,'array':new_array}))

	print(r.text)	

# Stage IV: The dating game
def stage_four(token):
	
	url = 'http://challenge.code2040.org/api/time'

	r = requests.post(url, data=json.dumps({'token':token}))

	data = r.json()['result']
	date_stamp = data['datestamp']
	interval = data['interval']	

	print(data)
	print(date_stamp)
	print(interval)

	given_year = int(date_stamp[0:4])
	given_month = int(date_stamp[5:7])
	given_day = int(date_stamp[8:10])
	given_hour = int(date_stamp[11:13])
	given_minute = int(date_stamp[14:16])
	given_second = int(date_stamp[17:19])
	given_time_zone = date_stamp[20:24] #tends to be the .000Z extension 

	# print(given_year)
	# print(given_month)
	# print(given_day)
	# print(given_hour)
	# print(given_minute)
	# print(given_second)
	# print(given_time_zone)


	seconds = int(interval)
	seconds_remaining = seconds % 60
	seconds = seconds - seconds_remaining
	
	minutes = int(seconds/60)
	minutes_remaining = minutes % 60
	minutes = minutes - minutes_remaining

	hours = int(minutes/60)
	hours_remaining = hours % 24
	hours = hours - hours_remaining

	days = int(hours/24)
	days_remaining = days % 356
	days = days - days_remaining

	years = int(days/356)

	print(seconds_remaining)
	print(minutes_remaining)
	print(hours_remaining)
	print(days_remaining)
	print(years)

	given_year = given_year + years

	while (days_remaining != 0):
	
		# 30 days have September, April, June, and November:
		if(given_month == 9 or given_month == 4 or given_month == 6 or given_month == 11):
			
			if 31 - given_day <= days_remaining:
				given_month = given_month + 1
				days_remaining = days_remaining - (31 - given_day)
				given_day = 1
			else:
				given_day = given_day + days_remaining
				days_remaining = 0

		# Ferbruary has 28 days, and 29 in leap year	
		elif (given_month == 2):
			
			if 29 - given_day <= days_remaining:
				given_month = given_month + 1
				days_remaining = days_remaining - (29 - given_day)
				given_day = 1
			else:
				given_day = given_day + days_remaining
				days_remaining = 0

		# 31 days for the rest
		else:
			if 32 - given_day <= days_remaining:
				given_month = given_month + 1
				days_remaining = days_remaining - (32 - given_day)
				given_day = 1
			else:
				given_day = given_day + days_remaining	
				days_remaining = 0	

		


	if(given_month > 12):
		given_year = given_year + 1
		given_month = given_month % 12

	given_hour = given_hour + hours_remaining
	
	given_minute = given_minute + minutes_remaining

	given_second = given_second + seconds_remaining

	if given_second > 60:
		given_minute = given_minute + 1
		given_second = given_second % 60

	if given_minute > 60:
		given_hour = given_hour + 1
		given_minute = given_minute % 60	

	if given_hour > 24:
		given_day = given_day + 1
		given_hour = given_hour % 24


	given_year = str(given_year)
	
	if(given_month < 10):
		given_month = '0' + str(given_month)
	else:
		given_month = str(given_month)

	if(given_day < 10):
		given_day = '0' + str(given_day)
	else:
		given_day = str(given_day)

	if(given_hour < 10):
		given_hour = '0' + str(given_hour)
	else:
		given_hour = str(given_hour)
	
	if(given_minute < 10):
		given_minute = '0' + str(given_minute)
	else:
		given_minute = str(given_minute)
	
	if(given_second < 10):
		given_second = '0' + str(given_second)
	else:
		given_second = str(given_second)

	new_time = given_year + '-' + given_month + '-' + given_day + 'T' + given_hour + ':' + given_minute + ':' + given_second + '.' + given_time_zone


	# print(given_year)
	# print(given_month)
	# print(given_day)
	# print(given_hour)
	# print(given_minute)
	# print(given_second)			


	print(new_time)

	url = 'http://challenge.code2040.org/api/validatetime'

	r = requests.post(url, data=json.dumps({'token':token, 'datestamp':new_time}))
	print(r.text)


if __name__ == "__main__":
    main()



