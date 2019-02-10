import copy
import setup
import string
import common
   

def get_team(teams, ip):
    for teamname, team_ips in teams.items():
        if ip in team_ips:
            return teamname


def get_player_class(teams, spymasters, ip):
    playerClass = getTeam(teams=teams, ip=ip) + "player"
    if ip in spymasters:
        playerClass += " spymaster"
    return playerClass


def evaluate_guess(state, tile):
    team_order = state['team_order']
    team = team_order[state['active_team']]
    board = state['board']
    chosen_tile = board[tile]
    if chosen_tile.revealed:
        raise ValueError('Already revealed')
    is_correct = chosen_tile.team_id == team
    new_tile = common.tile(chosen_tile.word, chosen_tile.team_id, True)
    new_board = [s if idx != tile else new_tile
                   for idx, s in enumerate(board)]
    new_state = copy.deepcopy(state)
    new_state['board'] = new_board
    return is_correct, new_state


def end_turn(state):
    raise NotImplementedError


def end_round(state):
    raise NotImplementedError


def main(config):
    setup.validate_config(**config)
    lexicon = string.ascii_letters
    state = setup.setup_board(lexicon, **config)

    board = state['board']

    while True:
        guess, new_state = evaluate_guess(state, 1)
        new_board = new_state['board']
        print('New board: {}'.format(new_board))
        for idx, its in enumerate(zip(board, new_board)):
            it = its[0]
            it2 = its[1]
            print(its)
            txt = "w: {} t: {} ex-r: {} r: {}"
            print(txt.format(it.word, it.team_id, it.revealed, it2.revealed))
        print(guess)
        break
        state = new_state


if __name__ == "__main__":
    config = {
        "assassins": 1,
        "board_size": 25,
        "teams": 2,
        "team_size": 8
    }

    main(config)
