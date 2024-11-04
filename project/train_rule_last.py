from yinda.rule_last import CardGame, RandomPlayer, QPlayer
import pickle
import numpy as np
import copy
# epsilon = 0.9
replace_rule = {
    0:3,1:3,2:4,3:4,4:1,5:1,6:2,7:2
}

player1 = QPlayer()
player2 = RandomPlayer()
game = CardGame(player1, player2)
N_episodes = 2000000
counts = {1: 0, 0: 0, -1: 0}
player1_card = copy.deepcopy(player1.get_first_index())
card_deck = [('Red', 1), ('Red', 1), ('Red', 2), ('Red', 2),
                    ('Black', 1), ('Black', 1), ('Black', 2), ('Black', 2)]
index = 0
for episodes in range(N_episodes):
    a, b = game.play()
    positions = [player1_card.index(item) for item in b if item in player1_card]
    player1_card = [replace_rule.get(i,i) for i in player1_card]
    max_value = max(player1_card)
    if player1_card[positions[0]] == max_value:
        index =index +1
    if a in counts:
        counts[a] += 1
    game.reset()
    player1_card =copy.deepcopy(player1.get_first_index())
    if (episodes + 1) % 1000 == 0:
        print(f"After {episodes + 1} episodes, counts are: {counts}")
        counts = {1: 0, 0: 0, -1: 0}
        print(index)
        index = 0

#
# Q = game.Q
# filename = "qi{}.p".format(N_episodes)
# pickle.dump(Q, open(filename, "wb"))
