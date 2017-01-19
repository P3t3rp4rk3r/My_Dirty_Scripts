from shodan import Shodan
from shodan.helpers import open_file, write_banner
from shodan.cli.helpers import get_api_key
from sys import argv, exit

# Validation
if len(argv) != 3:
	print('Usage: {} <IPs filename> <output.json.gz>'.format(argv[0]))
	print('Example: {} grizzly-ips.txt shodan-grizzly.json.gz'.format(argv[0]))
	exit(1)

input_filename = argv[1]
output_filename = argv[2]

# Must have initialized the CLI before running this script
key = get_api_key()

api = Shodan(key)

#Output file
fout = open_file(output_filename, 'w')

# Open the file containing the list of IPs
with open(input_filename, 'r') as fin:
	# Loop over all the IPs in the file
	for line in fin:
		ip = line.strip() # Remove any trailing whitespace/ newlines

		# Wrap the API calls to nicely skip IPs which don't have data
		try:
			print('Processing: {}'.format(ip))
			info = api.host(ip)
			
			# All the banners are stored in the "data" property
			for banner in info['data']:
				write_banner(fout, banner)
		except:
			pass # No data
		
