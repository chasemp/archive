#very first thing I ever wrote
#was to try to calculate the stardate...

import time, decimal, os

now = time.time()
dse = now / 86400.0
centpercent = dse / 36525
sdd = centpercent * 100000
print sdd
