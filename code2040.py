import json
import requests

def main():

	data = json.dumps({'email':'joevt@vt.edu', 'github':'https://github.com/jfletchvt/CODE2040.git'}) 

	r = requests.post('http://challenge.code2040.org/api/register', data=data)

	token = r.json()['result']

	stage_one(token)
	stage_two(token)

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



if __name__ == "__main__":
    main()



