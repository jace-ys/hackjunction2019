from gglsbl import SafeBrowsingList

import sys

api_key='API-KEY-GOES-HERE'
sbl = SafeBrowsingList(api_key)
bl = sbl.lookup_url('http://google.com')

# ADD SOURCE CODE HERE
if bl is None:
    print('{} is not blacklisted'.format('http://google.com'))
else:
    print('{} is blacklisted in {}'.format('http://google.com', bl))
    sys.exit(blacklisted_return_code)
sys.exit(0)