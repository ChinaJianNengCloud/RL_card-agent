from yinda.rule_two import CardGame, RandomPlayer, QPlayer
import pickle
import numpy as np
import copy
# epsilon = 0.9
replace_rule = {
    0:3,1:3,2:4,3:4,4:1,5:1,6:2,7:2
}
max_index_recorded = -1
player1 = QPlayer()
player2 = RandomPlayer()
game = CardGame(player1, player2)
N_episodes = 1000000
counts = {1: 0, 0: 0, -1: 0}
player1_card = copy.deepcopy(player1.get_first_index())
card_deck = [('Red', 1), ('Red', 1), ('Red', 2), ('Red', 2),
                    ('Black', 1), ('Black', 1), ('Black', 2), ('Black', 2)]
index = 0
for episodes in range(N_episodes):
    a,b=game.play()
    positions = [player1_card.index(item) for item in b if item in player1_card]
    player1_card = [replace_rule.get(i,i) for i in player1_card]
    max_value = max(player1_card)
    if a == [1,1]:
        counts[1] +=1
    else:
        counts[-1]+= 1
    if player1_card.count(max_value) >= 2:
        indexes_of_a = [index for index, value in enumerate(player1_card) if value == a]
        set1 = set(indexes_of_a)
        set2 = set(positions)
        if set1 == set2:
            index = index + 1
    else:
        top_two = sorted(set(player1_card), reverse=True)[:2]
        elements_by_indices = [player1_card[index] for index in positions]
        if all(element in elements_by_indices for element in top_two):
            index = index + 1
    game.reset()
    player1_card =copy.deepcopy(player1.get_first_index())
    if (episodes + 1) % 100 == 0:
        print(f"After {episodes + 1} episodes, counts are: {counts}")
        counts = {1: 0, 0: 0, -1: 0}
        print(index)
        if index > 55:
            max_index_recorded = index
            Q_for_max_index = copy.deepcopy(game.Q)
            break
        index = 0
# for key  in Q_for_max_index:
#     for inner_key in Q_for_max_index[key]:
#         Q_for_max_index[key][inner_key]=1
#
filename = "two{}middle.p".format(N_episodes)
pickle.dump(Q_for_max_index, open(filename, "wb"))
