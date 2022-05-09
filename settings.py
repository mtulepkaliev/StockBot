#I know, global variable bad, but it's a constant,ok
from decimal import Decimal


global DECIMAL_FORMAT
DECIMAL_FORMAT = Decimal('0.01')
REFRESH_TIMEOUT_SEC:int = 60