
from decimal import Decimal

#format to print decimals
global DOLLAR_FORMAT
DOLLAR_FORMAT = Decimal('0.01')

#time between refrshing ticker info
REFRESH_TIMEOUT_SEC:int = 60