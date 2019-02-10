# -*- coding: utf-8 -*-
from bottle import route, run, request, template, static_file
import random

from . import common
from .logic import get_team as getTeam, get_player_class as getPlayerClass


def setupMatch(word_list, deck_size):
    global wordsSample, blue_first, spymasters, spies, revealed, gameOver
    gameOver = False
    spymasters = []
    wordsSample = random.sample(word_list, deck_size)
    revealed = [False] * deck_size
    r = b = 8
    blue_first = (random.randint(0,1) == 0)
    b, r = (b + 1, r) if blue_first else (b, r + 1)
    spies = [0] * deck_size
    spies[random.randint(0, deck_size - 1)] = -1
    while b > 0 or r > 0:
        pos = random.randint(0, deck_size - 1)
        if spies[pos] == 0:
            if b > 0:
                spies[pos] = 1
                b -= 1
            elif r > 0:
                spies[pos] = 2
                r -= 1


def newGame():
    try:
        request.query['newgame']
        if gameOver:
            setup_match()
    except:
        pass


def checkAccount(player_dict, word_list):
    ip = request['REMOTE_ADDR']
    if not ip in player_dict:
        player_dict[ip] = random.choice(word_list)
        if len(teams['blue']) <= len(teams['red']):
            teams['blue'].append(ip)
        else:
            teams['red'].append(ip)
    return ip


def listPlayers(teamname=None):
    if teamname is None:
        if blue_first:
            return listPlayers('blue') + listPlayers('red')
        else:
            return listPlayers('red') + listPlayers('blue')
    else:
        players = ""
        for ip in teams[teamname]:
            player_class = getPlayerClass(teams=teams, spymasters=spymasters, ip=ip)
            players += "<span class='" + player_class + "'>" + player_dict[ip] + "</span>&nbsp;"
        return players


def getWordHtml():
    ip = checkAccount(player_dict=player_dict, word_list=word_list)
    isMaster = ip in spymasters
    wordhtml = [""] * common.deck_size
    for i in range(len(spies)):
        wordColour = ""
        if spies[i] == -1: wordColour = "black"
        elif spies[i] == 0: wordColour = "gray"
        elif spies[i] == 1: wordColour = "blue"
        elif spies[i] == 2: wordColour = "red"
        wordbase = wordsSample[i]
        if revealed[i]:
            wordclass = "hidden-" + wordColour + " revealed-" + wordColour
        elif isMaster or gameOver:
            wordclass = "hidden-" + wordColour
        else:
            wordclass = "hidden"
            wordbase = "<a href='/?reveal=" + str(i) + "'>" + wordbase + "</a>"        
        wordhtml[i] = "<td class='" + wordclass + "'>" + wordbase + "</td>"    
    return wordhtml


def gameOverScreen(game_over):
    gameover_text = "<h2 class='account'><a href='/?newgame=1'>Νέα παρτίδα</a></h2>"
    return "" if not game_over else gameover_text


def revealWord():
    global revealed
    ip = checkAccount(player_dict=player_dict, word_list=word_list)
    try:
        word = int(request.query['reveal'])
        if not gameOver and not ip in spymasters and not revealed[word]:
            revealed[word] = True
            checkGameOver()
    except:
        pass


def checkGameOver():
    global gameOver
    redDone = True
    blueDone = True
    for i in range(len(spies)):
        if not revealed[i]:
            if spies[i] == 1:
                blueDone = False
            elif spies[i] == 2:
                redDone = False
        elif spies[i] == -1:
            gameOver = True
    if redDone or blueDone:
        gameOver = True


@route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root='./static/')

@route('/')
def main():
    ip = checkAccount(player_dict=player_dict, word_list=word_list)
    newGame()
    revealWord()
    return template('main', username = player_dict[ip], word = getWordHtml(), players=listPlayers(), gameoverscreen = gameOverScreen(game_over=gameOver))

@route('/account')
def account():
    ip = checkAccount(player_dict=player_dict, word_list=word_list)
    accountTeam = getTeam(teams=teams, ip=ip)
    blue = "checked" if accountTeam == 'blue' else ""
    red =  "checked" if accountTeam == 'red' else ""
    master = "checked disabled='true'" if ip in spymasters else ""
    return template('account', ipaddress = ip, username = player_dict[ip], checkedBlue = blue, checkedRed = red, spymaster = master)


@route('/account', method='POST')
def account_post():
    try:
        #gather original info:
        ip = request['REMOTE_ADDR']
        oldTeam = getTeam(teams=teams, ip=ip)
        #gather changed  info
        newTeam = request.forms.get('team')
        newName = request.forms.get('username')
        isMaster = not request.forms.get('spymaster') is None
        #save new info:
        if len(newName) > 0:
            player_dict[ip] = newName
        else:
            raise #μπράβο Παύλε μεγάλε τέστερ και καραμπουζουκλή!!
        if not newTeam == oldTeam:
            teams[oldTeam].remove(ip)
            teams[newTeam].append(ip)
        if isMaster:
            spymasters.append(ip)
        return "<a href='/'>Οι αλλαγές αποθηκεύτηκαν!</a>"
    except:
        return "<a href='/account'>Προέκυψε κάποιο πρόβλημα!</a>"


def starter():
    gameOver = False
    spymasters = []
    wordsSample = []
    spies = []
    revealed = []

    setupMatch(word_list=word_list, deck_size=common.deck_size)
    run(host='0.0.0.0', port=8080, debug=True)


if __name__ == "__main__":
    player_dict = {}
    word_file = 'words-el.txt'
    word_list = [word for word in open(word_file, 'r')]
    teams = {'blue':[], 'red':[]}
    starter()
