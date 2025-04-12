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

slot_machine = {'Anpan': [0.1,1000000],
                'deez nuts': [1, 100000],
                'pantsu':[3, 50000],
                'Dildo': [20,10000],
                'Squirrel': [25,7000],
                'Fart wad': [30,6300],
                'Croissant': [33,6000],
                '❀': [35,5000],
                '♥︎': [40,3000],
                '✪': [80,1500],
                'Boner pills': [300, 700],
                'O-Chinchin': [400,500],
                'O-Manko': [400,500],
                'Pube sandwhich': [480, 250],
                'Derptoid': [650,100],
                'Boobies': [650,50],
                '糞': [550,5]
                }

# BOT COMMANDS

def _say(message, args):
    return message


def _bgtime(message, args):
    try:
        a, b, c = message[0], message[1], message
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


def _numbergame(message, args):
    try:
        if message == 'start':
            try:
                manager["games"]["numbergame"]
                return "There is already a game!!"
            except:
                _num = random.randint(1,30)
                manager["games"]["numbergame"] = _num
                return "You have started the guessing game! Pick a number between 1 and 30."
        else:
            _num = manager["games"]["numbergame"]
            guess = message
            try:
                guess = int(message)
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


#def _dicebet(message):
    #each player bets a certain amount of points on a dice number, same for every player, winner takes all. cpu takes number not bet on for jackpot pool. maybe have a player wallet for betting games. one number rarest gives chance for jackpot. player can earn title with points.

def _register(message, args):
    user = args['user']
    try:
        manager["games"][user]
        return "You are already registered"
    except:
        manager["games"][user] = dict(
            wallet = 1000,
            title = None,
            items = []
        )
        return "Registered for the games. Your starting wallet is 1000 points."

def _check(message, args):
    user = args["user"]
    if message.lower() == "wallet":
        return str(manager["games"][user]["wallet"])

def _slot(message, args):
    user = args["user"]
    try:
        derp = manager["games"][user]
    except:
        return 'You must register for games first. Use the "register" command.'
    wallet = manager["games"][user]["wallet"]
    title = manager["games"][user]["title"]
    title = user if title == None else title
    if wallet < 100:
        return "You do not have enough points to play the slot machine. (100 points required)"
    wallet -= 100
    choice_pool = []
    for i in slot_machine:
        _num = slot_machine[i][0]
        _num = int(_num*10)
        [choice_pool.append(i) for x in range(_num)]
    outcome = []
    for i in range(3):
        outcome.append(random.choice(choice_pool))
    result_num = []
    for i in slot_machine:
        result_num.append([i, outcome.count(i)])
    for i in result_num:
        if i[1] < 2:
            result_num.remove(i)
    final_results = '['+', '.join(outcome)+'] '
    for i in result_num:
        if i[1] == 3:
            amount = slot_machine[i[0]][1]*2
            wallet += amount
            manager["games"][user]["wallet"] = wallet
            if i == 'Anpan':
                return final_results+'You hit the big Anpan jackpot!! You win '+str(amount)+' points. [-100 points for playing]'
            else:
                return final_results+'You hit a three of a kind with ['+i[0]+']!!! You win '+str(amount)+' points. [-100 points for playing]'
        elif i[1] == 2:
            outcome.remove(i[0])
            outcome.remove(i[0])
            amount = round(
                    (
                        (slot_machine[i[0]][1]*(1/10))*2
                        )
                    +(slot_machine[outcome[0]][1]*(1/20))
                 )
            if amount < 1:
                amount = 1
            wallet += amount
            manager["games"][user]["wallet"] = wallet
            return final_results+'You hit a two of a kind with ['+i[0]+']!!! You win '+str(amount)+' points. [-100 points for playing]'
        else:
            continue
    amount = [slot_machine[i][1]*(1/20) for i in outcome]
    a,b,c = amount
    amount = round(a+b+c)
    if amount < 1:
        amount = 1
    wallet += amount
    manager["games"][user]["wallet"] = wallet
    return 'The results are '+final_results+'You win '+str(amount)+' points. [-100 points for playing]'
