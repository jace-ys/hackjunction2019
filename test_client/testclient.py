from gglsbl import SafeBrowsingList

import sys
import os

api_key=os.getenv("api-key")
sbl = SafeBrowsingList(api_key)
URL="http://google.com"
bl = sbl.lookup_url(URL)

# ADD SOURCE CODE HERE
if bl is None:
    print('{} is not blacklisted'.format(URL))
else:
    print('{} is blacklisted in {}'.format(URL, bl))
    sys.exit(blacklisted_return_code)
sys.exit(0)