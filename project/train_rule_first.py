from yinda.rule_first import CardGame, RandomPlayer, QPlayer
import pickle
import numpy as np
import copy

# 初始化参数和对象
player1 = QPlayer()
player2 = RandomPlayer()
game = CardGame(player1, player2)
N_episodes = 1000000
counts = {1: 0, 0: 0, -1: 0}
replace_rule = {
    0: 3, 1: 3, 2: 4, 3: 4,
    4: 1, 5: 1, 6: 2, 7: 2
}

# 需要跟踪记录最大index值及对应游戏状态（Q-value）
max_index_recorded = -1  # 记录遇到的最大index值初始化为-1
Q_for_max_index = None  # 初始化为空
index = 0
segment_size = 100  # 设定检查点间隔
index_records = []  # 可选：用于记录每个段落内最大index

for episodes in range(N_episodes):
    player1_card = copy.deepcopy(player1.get_first_index())

    a, b = game.play()
    b = [b]
    positions = [player1_card.index(item) for item in b if item in player1_card]
    player1_card = [replace_rule.get(i, i) for i in player1_card]
    max_value = max(player1_card)

    if positions and player1_card[positions[0]] == max_value:
        index += 1

    if a in counts:
        counts[a] += 1

    game.reset()

    # 每10000回合打印一次结果，并在每10000回合检查一次是否需要更新Q_for_max_index
    if (episodes + 1) % 100 == 0:
        print(f"After {episodes + 1} episodes, counts are: {counts}")
        counts = {1: 0, 0: 0, -1: 0}

    if (episodes + 1) % segment_size == 0 or episodes == N_episodes - 1:
        print(f"Segment {((episodes + 1) // segment_size)} Index Count: {index}")
        index_records.append(index)

        # if index > max_index_recorded:
        #     max_index_recorded = index
        #     Q_for_max_index = copy.deepcopy(game.Q)
        if index >= 70:
            max_index_recorded = index
            Q_for_max_index = copy.deepcopy(game.Q)
            break
        index = 0  # 段结束，重置index

# for key  in Q_for_max_index:
#     for inner_key in Q_for_max_index[key]:
#         Q_for_max_index[key][inner_key]=1

# 在所有游戏回合完成后保存具有最大index值对应的Q到文件中
filename_format_string = "first{}_middleIndex.p"
filename = filename_format_string.format(N_episodes)
pickle.dump(Q_for_max_index, open(filename, "wb"))
print("Completed. Q corresponding to the maximum index has been saved.")