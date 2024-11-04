import math

import numpy as np
import random

import copy


# 一个简单的环境类
class CardGame:
    def __init__(self, player1, player2, Q_learn=True, Q={}, alpha=0.3, gamma=0.9):
        # 定义牌库
        self.deck = Deck()
        self.player1 = player1
        self.player2 = player2
        # 发牌
        self.reset()
        self.Q_learn = Q_learn
        self.win = []
        self.a_deck = []
        if self.Q_learn:
            self.Q = Q
            self.alpha = alpha  # Learning rate
            self.gamma = gamma  # Discount rate

    def reset(self):
        # 洗牌并发牌
        self.win = []
        self.a_deck = []
        self.qplayer = self.player1
        self.randomplayer = self.player2
        self.qplayer.arr = None
        self.qplayer.card = None
        self.randomplayer.arr = None
        self.randomplayer.card = None
        self.deck.one = [np.nan] * len(self.deck.card_deck)
        card = self.deck.card_deck
        index = self.deck.indices
        six_indices = set(random.sample(index, 6))
        p1_indices = set(random.sample(six_indices, 3))
        p2_indices = six_indices - p1_indices
        p1_list = list(p1_indices)
        p2_list = list(p2_indices)
        p1_list_sort = sorted(p1_list)
        p2_list_sort = sorted(p2_list)
        self.qplayer.setcard([card[idx] for idx in p1_list_sort])
        self.qplayer.setarr(p1_list)
        self.randomplayer.setcard([card[idx] for idx in p2_list_sort])
        self.randomplayer.setarr(p2_list)

    def play(self):
        if isinstance(self.qplayer, QPlayer) and isinstance(self.randomplayer, RandomPlayer):
            i = 0
            while True:  # Make the two computer players play against each other without button presses
                if i >= 2:
                    return self.win,self.a_deck
                i = i + 1
                self.play_turn(i)

    def play_turn(self, i):

        self.learn_Q(i, self.qplayer, self.randomplayer)

    def learn_Q(self, i, qplayer, randomplayer):

        state_key = QPlayer.make_and_maybe_add_key(qplayer.arr, self.deck, self.Q)
        # 这里的ab是针对牌库的
        a = qplayer.get_card(self.deck)
        b = randomplayer.get_card(self.deck)
        self.win.append(self.deck.winner(i, a, b))
        self.a_deck.append(a)
        self.qplayer.remove_player1(a)
        self.randomplayer.remove_player2(b)
        # 移动之后的棋盘
        next_board = self.deck.get_next_state(a, b)
        # 奖励
        reward = next_board.give_reward(i, self.win)
        next_state_key = QPlayer.make_and_maybe_add_key(self.qplayer.arr, next_board, self.Q)
        if i == 2:
            expected = reward
        else:
            next_Qs = self.Q[
                next_state_key]  # The Q values represent the expected future reward for player X for each available move in the next state (after the move has been made)

            expected = reward + (self.gamma * max(
                next_Qs.values()))  # If the current player is X, the next player is O, and the move with the minimum Q value should be chosen according to our "sign convention"
        change = self.alpha * (expected - self.Q[state_key][a])
        self.Q[state_key][a] += change
        self.deck.updatadeck(a, b)
        self.qplayer.Q = self.Q


class Deck():
    def __init__(self):
        self.card_deck = [('Red', 1), ('Red', 1), ('Red', 2), ('Red', 2),
                          ('Black', 1), ('Black', 1), ('Black', 2), ('Black', 2)]
        self.indices = set(range(len(self.card_deck)))
        self.one = [np.nan] * len(self.card_deck)

    def get_player1_arr(self, a):
        self.player1_arr = a

    def deck_state(self):
        return self.one

    def updatadeck(self, a, b):
        self.one[a] = 1
        self.one[b] = 1

    def winner(self, i, a, b):
        if self.win_rule(a, b) == 1:
            return 1
        elif self.win_rule(a, b) == -1:
            return -1
        elif self.win_rule(a, b) == 0:
            return 0

    def win_rule(self, a, b):
        card1_color, card1_num = self.card_deck[a]
        card2_color, card2_num = self.card_deck[b]
        if all(var is not None for var in [card1_color, card2_color, card1_num, card2_num]):
            if card1_color != card2_color:  # 颜色不同，红色赢
                return 1 if card1_color == 'Red' else -1
            elif card1_num > card2_num:  # 颜色相同，点数大者赢
                return 1
            elif card1_num < card2_num:
                return -1
            else:
                return 0  # 平局

    def give_reward(self, i, win):  # Assign a reward for the player with mark X in the current board position.
        if i == 2 and win == [1, 1]:
            return 3
        elif i == 2 and (win ==[0,1] or win == [1,0]):
            return 0.5
        elif i == 2 and (win ==[-1,1] or win == [1,-1]):
            return 0.00
        elif i == 2 and (win == [-1, 0] or win == [0, -1]):
            return -1
        elif i == 2 and (win == [-1, -1]):
            return -2
        elif i == 2 and (win == [0, 0]):
            return 0.1
        elif i == 1 and (win==[0]):
            return 0
        elif i == 1 and (win == [-1]):
            return -1
        elif i == 1 and (win == [1]):
            return 1
    def make_key(
            self,
            player1_arr):  # For Q-learning, returns a 10-character string representing the state of the board and the player whose turn it is
        fill_value = 9
        filled_one = copy.deepcopy(self.one)
        for i in range(len(filled_one)):
            if math.isnan(filled_one[i]):
                filled_one[i] = fill_value

        return ''.join(map(str, filled_one + player1_arr))

    def get_next_state(self, a, b):
        next_deck = copy.deepcopy(self)
        next_deck.one[a] = 1
        next_deck.one[b] = 1
        return next_deck


class Player(object):
    def setcard(self, card_list):
        self.card = card_list

    def setarr(self, arr):
        self.arr = arr

    def getcard(self):
        return self.card

    def getarr(self):
        return self.arr

    def getcolorandnum(self):
        if len(self.card) == 1:
            color, num = self.card[0]
            return color, num
        else:
            return None, None


class RandomPlayer(Player):
    def __init__(self):
        super().__init__()

    def get_card(self, deck):
        if self.card is not None:  # 检查card列表是否非空
            # 随机选取card列表中的一个索引
            cards = self.card
            arrs = self.arr
            chosen_index = np.random.choice(len(arrs))
            # 根据选取的索引获取具体的卡片
            index = arrs[chosen_index]
            return index
        else:
            return None

    def remove_player2(self, index):
        cards = self.card
        arrs = self.arr
        if index in arrs:
            position = arrs.index(index)
            self.arr.remove(index)
            if position < len(cards):
                del self.card[position]
        else:
            print(f"Index not found in")


class QPlayer(Player):
    def __init__(self, Q={}, epsilon=0.01):
        self.Q = Q
        self.epsilon = epsilon
        super().__init__()

    def get_first_index(self):
        if len(self.arr) == 3:
            return self.arr

    def getlastcard(self):
        if len(self.arr) == 1:
            return self.arr

    def get_card(self, deck):
        if np.random.uniform() < self.epsilon:
            return RandomPlayer.get_card(self, deck)
        else:
            arr_list = self.arr
            state_key = self.make_and_maybe_add_key(arr_list, deck, self.Q)
            Qs = self.Q[state_key]
            return self.stochastic_argminmax(Qs, max)

    @staticmethod
    def make_and_maybe_add_key(arr_list, deck,
                               Q):  # Make a dictionary key for the current state (board + player turn) and if Q does not yet have it, add it to Q
        default_Qvalue = 1.0  # Encourages exploration
        state_key = deck.make_key(arr_list)
        if Q.get(state_key) is None:
            arrs = arr_list
            Q[state_key] = {arr: default_Qvalue for arr in
                            arrs}  # The available moves in each state are initially given a default value of zero
        # print(Q)
        # print("\n")

        return state_key

    @staticmethod
    def stochastic_argminmax(Qs,
                             min_or_max):  # Determines either the argmin or argmax of the array Qs such that if there are 'ties', one is chosen at random
        min_or_maxQ = min_or_max(list(Qs.values()))
        if list(Qs.values()).count(
                min_or_maxQ) > 1:  # If there is more than one move corresponding to the maximum Q-value, choose one at random
            best_options = [arr for arr in list(Qs.keys()) if Qs[arr] == min_or_maxQ]
            index = best_options[np.random.choice(len(best_options))]
        else:
            index = min_or_max(Qs, key=Qs.get)
        # QPlayer.remove_player1(index)
        return index

    def remove_player1(self, index):
        cards = self.card
        arrs = self.arr
        if index in arrs:
            position = arrs.index(index)
            self.arr.remove(index)
            if position < len(cards):
                del self.card[position]
        else:
            print(f"Index not found in")
