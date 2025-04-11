import time
import urllib.request
import urllib.parse
import random
import re
from datetime import datetime

def regex(pattern, x, default):
        return re.search(pattern, x).group(1) if re.search(pattern, x) else default

manager = {}
manager["games"] = {}

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


def _numbergame(args):
    try:
        if args == 'start':
            try:
                manager["games"]["numbergame"]
                return "There is already a game!!"
            except:
                _num = random.randint(1,30)
                manager["games"]["numbergame"] = _num
                return "You have started the guessing game! Pick a number between 1 and 30."
        else:
            _num = manager["games"]["numbergame"]
            guess = args
            try:
                guess = int(args)
            except:
                return 'Not a valid guess.'
            if guess > _num:
                return 'Too high!'
            elif guess < _num:
                return 'Too low!!'
            else:
                del manager["games"]["numbergame"]
                return 'Thats it!!!'
    except:
        return 'You must start the game first! "numbergame start"'
