# 原项目github
原项目是一个用强化学习训练一个井字棋的机器人
github网址是https://github.com/khpeek/Q-learning-Tic-Tac-Toe

# 项目介绍
利用井字棋的强化学习的基础逻辑，修改成训练一个出牌机器人。

游戏规则:
给两人发放牌库里的八张中随机的六张，每人随机发到三张牌，牌库里的八张牌分别是（两张红1、两张红2、两张黑1、两张黑2）。
比赛规则是如果颜色不一样，红色的牌大就是赢；如果颜色一样，点数大就大，如果颜色和点数都一样那就是平局。三张牌每局出一张牌，只有第三局赢才算赢。


# 代码介绍
存在3种赢的规则，
第一种赢的规则，第一次赢就赢。

第二个赢的规则，最后一次赢就赢。

第三个赢的规则，先赢2次的就赢。
对应了三个训练代码train_rule_first.py train_rule_last.py train_rule_two.py


# 项目结果
在result中

# 个人理解
本人对于强化学习的理解就是在游戏规则内遍历所有的情况，在某次要进行操作的时候找到适合当前情况的所有操作数据，拿到权重最高的那个操作，并且执行，下一次也是如此。