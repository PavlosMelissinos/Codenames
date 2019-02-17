import random
import string
import sys

from common import tile


def shuffle_identities(group_sizes):
    all = [it for idx, group_size in enumerate(group_sizes)
              for it in group_size * [idx]]
    random.shuffle(all)
    return all


def assign_to_groups(plays_first, teams, team_size, **kwargs):
    team_sizes = [team_size if plays_first != gid else team_size + 1 for gid in range(teams)]
    return team_sizes


def validate_config(assassins, board_size, teams, team_size, **kwargs):
    num_actors = assassins + teams * team_size + 1
    if num_actors >= board_size:
        raise ValueError("Pick a larger board or remove some actors")


def setup_board(lexicon, board_size, assassins, **config):
    # choose words
    words = random.sample(lexicon, board_size)


    teams = config['teams']

    # assign identities
    team_order = random.sample(range(teams), teams)

    active_team = 0
    config['plays_first'] = active_team
    spy_groups = assign_to_groups(**config)

    civilians = board_size - assassins - sum(spy_groups)

    groups = [assassins, civilians] + spy_groups
    ids = shuffle_identities(groups)

    # set initial state to hidden
    revealed = [False] * board_size

    # zip fields and return state
    zipped = zip(words, ids, revealed)
    board = [tile(*i) for i in zipped]

    return {
        'active_team': active_team,
        'phase': 0,
        'team_order': team_order,
        'board': board
    }


def main():
    config = {
        "assassins": 1,
        "board_size": 25,
        "teams": 2,
        "team_size": 8
    }

    validate_config(**config)
    print("lala")
    lexicon = string.ascii_letters
    state = setup_board(lexicon=lexicon, **config)
    team_order = state['team_order']
    active_team = team_order[state['active_team']]
    board = state['board']

    for idx, it in enumerate(board):
        print(idx+1, it.word, it.team_id, it.revealed)
    print(board[-1])
    print('First team: {}'.format(active_team))
    print('Team order: {}'.format(team_order))
    


if __name__ == "__main__":
    main()
