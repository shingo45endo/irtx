 #!/usr/bin/python3

import sys
import re
import urllib.request
import urllib.parse

import irparser
import irdevice

# TODO: Implement command line parser.
path = sys.argv[1]

# Reads an IR data from the URL or the file path.
frags = urllib.parse.urlparse(path)
if re.match(r'https?', frags.scheme):
	with urllib.request.urlopen(path) as res:
		data = res.read().decode('utf-8')
else:
	filepath = path if frags.scheme != 'file' else urllib.request.url2pathname(frags.path)
	with open(filepath) as file:
		data = file.read()

# Parses an IR data.
usecs = irparser.parse(data)

# Transmits the IR data with an IR device.
irdev = irdevice.get_device()
irdev.send(usecs)
