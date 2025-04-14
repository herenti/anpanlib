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
manager["game_session"] = {}

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

def _fart(message, args):
    choice = ['thbt','tttbbbbtt', 'tttttthhhhhhbbbbbttt', 'flubflublbblb','brrrrrraapppp','brrrurnnnntttt', ' ']
    _num = random.randrange(1, 5)
    choice = [random.choice(choice) for x in range(_num)]
    choice = ''.join(choice)
    if choice == ' ':
        choice = '   - It was a silent one....'
    return ''.join(choice)

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
    user = args["user"]
    chat = args["chat"]
    try:
        derp = manager["games"][user]
    except:
        return 'You must register for games first. Use the [register] command.'
    wallet = manager["games"][user]["wallet"]
    title = manager["games"][user]["title"]
    title = user if title == None else title
    try:
        if message == 'start':
            try:
                manager["game_session"][chat]
                return "There is already a game!!"
            except:
                _num = random.randint(1,30)
                manager["game_session"][chat] = dict(numbergame = _num)
                return title+', you have started the guessing game! Everyone in the chat can play. Pick a number between 1 and 30. Command example is [numbergame 14]'
        else:
            _num = manager["game_session"][chat]["numbergame"]
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
                del manager["game_session"][chat]
                wallet += 200
                manager["games"][user]["wallet"] = wallet
                return title+' thats it!!! [200 points added to your wallet.]'
    except:
        return 'You must start the game first! The command is [numbergame start]'


def _dice(message, args):
    x = message.split(' ',1)
    try:
        if len(x) > 1:
            command, number = x[0], int(x[1])
        else:
            command = x[0]
    except:
        return "That is not a valid command"
    user = args['user']
    chat = args["chat"]
    try:
        derp = manager["games"][user]
    except:
        return 'You must register for games first. Use the [register] command.'
    wallet = manager["games"][user]["wallet"]
    title = manager["games"][user]["title"]
    amount = 250
    if command == 'start':
        try:
            manager["game_session"][chat]
            return "There is already a game in this chat. Please finish it first!!"
        except:
            _num = random.randint(1,7)
            try:
                manager["game_session"][chat]["dice"]
            except KeyError:
                manager["game_session"][chat] = {}
                manager["game_session"][chat]["dice"] = {}
                manager["game_session"][chat]["dice"]["roll"] = _num
                manager["game_session"][chat]["dice"]["users"] = {}
                manager["game_session"][chat]["dice"]["pot"] = 0
                return title+', you have started a round of dice betting. Up to seven users may play. Minimum of two. Place bets with this command on numbers 1-7 of the dice sides: example: [dice bet 6]. When all players are ready use the command [dice roll].'
    elif command == 'bet':
        if number > 7:
            return "That is not a valid number."
        elif number < 1:
            return "That is not a valid number."
        if user in manager["game_session"][chat]["dice"]["users"]:
            return "You have already bet on the dice this round."
        elif number in list(manager["game_session"][chat]["dice"]["users"].values()):
            return "A user has already bet on that number."
        elif amount > wallet:
            return "You dont have enough points in your wallet. [Wallet: %s points]"  % wallet
        elif len(manager["game_session"][chat]["dice"]["users"]) == 7:
            return "The game is full. Please use the command [dice roll]"
        else:
            manager["games"][user]["wallet"] -= amount
            manager["game_session"][chat]["dice"]["pot"] += amount
            manager["game_session"][chat]["dice"]["users"][user] = number
            return "You have bet %s on the number %s." % (amount, number)
    elif command == "roll":
        if user not in manager["game_session"][chat]["dice"]["users"]:
            return "You are not playing this game. Place a bet first."
        elif len(manager["game_session"][chat]["dice"]["users"]) < 2:
            return "There must be at least two users playing."
        else:
            win_num = manager["game_session"][chat]["dice"]["roll"]
            if win_num not in list(manager["game_session"][chat]["dice"]["users"].values()):
                del manager["game_session"][chat]
                return "The winning number is %s. A user did not win. The bot takes the pot." % win_num
            winner = [i for i in manager["game_session"][chat]["dice"]["users"] if manager["game_session"][chat]["dice"]["users"][i] == win_num][0]
            manager["games"][winner]["wallet"] += manager["game_session"][chat]["dice"]["pot"]
            winner = manager["games"][winner]["title"]
            pot = manager["game_session"][chat]["dice"]["pot"]
            del manager["game_session"][chat]
            return "The winner is " + winner  + '!!!! They win the pot of '+ str(pot) + ' points. The winning number was '+ str(win_num) + '.'



    #each player bets a certain amount of points on a dice number, same for every player, winner takes all. cpu takes number not bet on for jackpot pool. maybe have a player wallet for betting games. one number rarest gives chance for jackpot. player can earn title with points.

def _register(message, args):
    user = args['user']
    try:
        manager["games"][user]
        return "You are already registered"
    except:
        manager["games"][user] = dict(
            wallet = 1000,
            title = user,
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
    final_results = '<b>[</b> '+' <b>|</b> '.join(outcome)+' <b>]</b> '
    for i in result_num:
        if i[1] == 3:
            amount = slot_machine[i[0]][1]*2
            wallet += amount
            manager["games"][user]["wallet"] = wallet
            if i == 'Anpan':
                return final_results+'You hit the big Anpan jackpot!! You win '+str(amount)+' points. [<b>-100</b> points for playing]'
            else:
                return final_results+'You hit a three of a kind with <b>[</b> '+i[0]+' <b>]</b>!!! You win '+str(amount)+' points. [<b>-100</b> points for playing]'
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
            return final_results+'You hit a two of a kind with <b>[</b> '+i[0]+' <b>]</b>!!! You win '+str(amount)+' points. [<b>-100</b> points for playing]'
        else:
            continue
    amount = [slot_machine[i][1]*(1/20) for i in outcome]
    a,b,c = amount
    amount = round(a+b+c)
    if amount < 1:
        amount = 1
    wallet += amount
    manager["games"][user]["wallet"] = wallet
    return 'The results are '+final_results+'You win '+str(amount)+' points. [<b>-100</b> points for playing]'
