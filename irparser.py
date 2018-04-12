 #!/usr/bin/python3

import sys
import re
import json
from collections import OrderedDict

def parse_lirc_raw_codes(data):
	assert type(data) is str

	return [int(numstr) for numstr in re.split(r'\s+', data.strip(), flags=re.M)]

def parse_adrsir_hex(data):
	assert type(data) is str

	line = data.splitlines()[0]
	counts = [int(line[i+2:i+4] + line[i:i+2], 16) for i in range(0, len(line), 4)]
	return [round(count * 1000.0 * 1000.0 / 38000.0) for count in counts]

def parse_irkit_json(data):
	assert type(data) is str

	obj = json.loads(data)
	assert 'freq' in obj 
	hz = obj['freq'] * 1000.0
	assert hz > 0

	return [round(count * 1000.0 * 1000.0 / hz) for count in obj['data']]

# A table of pairs of the regex for the specific IR data format and its parser.
table = OrderedDict([
	('adrsir_hex',     (re.compile(r'^(?:[0-9a-f]{4})+\s*$', flags=re.I), parse_adrsir_hex)),
	('lirc_raw_codes', (re.compile(r'^\s*[0-9]+[0-9\s]*$', flags=re.M),   parse_lirc_raw_codes)),
	('irkit_json',     (re.compile(r'^\s*\{\s*\".*\}\s*$', flags=re.M),   parse_irkit_json)),
])

def parse(data, kind=None):
	try:
		if kind:
			if kind not in table:
				raise ValueError('Invalid data type: {}'.format(kind))

			regex, func = table[key]
			if not regex.match(data):
				raise ValueError('Invalid data as "{}"'.format(kind))

			return func(data)

		else:
			for key in table:
				regex, func = table[key]
				if regex.match(data):
					return func(data)

			raise ValueError('Cannot parse')

	except Exception as e:
		print('{}'.format(e), file=sys.stderr)

	return None
