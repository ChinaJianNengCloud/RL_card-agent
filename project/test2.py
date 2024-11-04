import random
from agent import agent
# 定义牌组
deck = [
    ('Red', 1), ('Red', 1), ('Red', 2), ('Red', 2),
    ('Black', 1), ('Black', 1), ('Black', 2), ('Black', 2)
]
num = 0
a = agent("./two1000000min.p")
# 循环1000次
for _ in range(10000):
    # 随机选择3张牌及其索引
    selected_cards_with_indices = random.sample(list(enumerate(deck)), 3)

    # 分别提取选中卡片和它们的索引
    selected_indices, selected_cards = zip(*selected_cards_with_indices)
    index1 = list(selected_indices)
    cards=list(selected_cards)
    total =[cards,index1]

    a.getinfo(total)

    pai = a.chupai()
    replace_rule = {
        0: 3, 1: 3, 2: 4, 3: 4,
        4: 1, 5: 1, 6: 2, 7: 2
    }
    pai = [pai]
    positions = [index1.index(item) for item in pai if item in index1]
    player1_card = [replace_rule.get(i, i) for i in index1]

    max_value = max(player1_card)
    if positions and player1_card[positions[0]] == max_value:
        num += 1
print(num)