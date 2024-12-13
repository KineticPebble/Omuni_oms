'''Contains all filename for channel and dates
Does Not contain any function
'''

from datetime import date as dt
from datetime import timedelta, datetime
from dateutil.relativedelta import relativedelta

# below are some date formating i usualy need but most of them are not used
td = dt.today()
yt = td - timedelta(days = 1)
ytd = yt.strftime("%d.%m.%Y")
ytymd = yt.strftime("%Y-%m-%d")
tdymd = td.strftime("%Y-%m-%d")
tddmy = td.strftime("%d-%m-%Y")
tdmdy = td.strftime("%m_%d_%Y")
tddmynu = td.strftime("%d%m%Y")
tddmy_ = td.strftime("%d_%m_%Y")
ytdmy_ = yt.strftime("%d_%m_%Y")

nmd = td + relativedelta(months=1)
nmd = nmd.replace(day=1)
lmd = nmd - relativedelta(days=1)
lmd = lmd.strftime("%Y-%m-%d")

location = 'omuni_oms' #location for saving the file
log_loc = '' # location for saving logs

email_address = '' #email address to send the file
database = '' # database to connect
table = '' # table to use