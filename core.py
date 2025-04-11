import time
import urllib.request
import urllib.parse
import re
from datetime import datetime

def regex(pattern, x, default):
        return re.search(pattern, x).group(1) if re.search(pattern, x) else default


# BOT COMMANDS

def _say(args):
    return args


def _bgtime(args):
    try:
        a, b, c = args[0], args[1], args
        url = 'http://st.chatango.com/profileimg/%s/%s/%s/mod1.xml' % (a,b,c)
        data = regex('<d>(.*?)</d>', urllib.request.urlopen(url).read().decode(), None)
        data = int(data)
        if time.time() > data:
            ret = 'Expired'
        else: ret = 'Expires'
        data = datetime.fromtimestamp(data).strftime(ret + ': Year: %Y - Month: %m - Day: %d')
        return data
    except:
        return 'That user has never had a background, or there is some other error.'
