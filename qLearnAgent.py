import numpy as np
import operator
import state
from random import randint
import random



def greedy_choose_action(sorted_actions):
    equal_action = []
    equal_action.append(sorted_actions[0])
    for i in range(1, len(sorted_actions)):
        if sorted_actions[i][1] == equal_action[0][1]:
            equal_action.append(sorted_actions[i])
    period = 100.0 / len(equal_action)
    index = 0
    random_number = randint(0, 100)
    for i in range(0, len(equal_action)):
        if (i + 1) * period > random_number > i * period:
            index = i
    pair = sorted_actions[index]
    return int(pair[0][0]), int(pair[0][1])


def epsilon_greedy_choose_action(sorted_actions,epsilon):

    probability_list = []
    optimal_action = [sorted_actions[0]]
    for i in range(1, len(sorted_actions)):
        if sorted_actions[i][1] == sorted_actions[0][1]:
            optimal_action.append(sorted_actions[i])
    for i in range(0, len(sorted_actions)):
        if i < len(optimal_action):
            accumulate = 0
            if i != 0:
                accumulate = probability_list[i - 1]
            probability_list.append(accumulate + ((1 - epsilon + epsilon / len(sorted_actions)) / len(optimal_action)))
        else:
            probability_list.append(epsilon / len(sorted_actions))
    probability_list[-1] = 1
    random_number = random.random()
    for i in range(0, len(probability_list)):
        if random_number < probability_list[i]:
            pair = sorted_actions[i]
            return int(pair[0][0]), int(pair[0][1])


class QLearnAgent:
    def __init__(self):
        super().__init__()
        self.q_matrix = {}
        self.alpha = 1.0
        self.discount_factor = 0.5
        self.action_count = 0.0
        self.epsilon = 1.0

    def retreive_from_db(self):
        pass

    def choose_action(self, current_game_map):
        self.action_count +=1
        current_map = current_game_map
        current_state_id = state.get_id_from_map(current_game_map)
        if current_state_id not in self.q_matrix.keys():
            action_list = self.get_possible_action(game_board=current_map)
            self.q_matrix[current_state_id] = {}
            for i in range(0, len(action_list)):
                self.q_matrix[current_state_id][action_list[i]] = 0.0
        sorted_actions = sorted(self.q_matrix[current_state_id].items(), key=operator.itemgetter(1), reverse=True)
        return greedy_choose_action(sorted_actions)
        # return epsilon_greedy_choose_action(sorted_actions=sorted_actions,epsilon=self.epsilon/self.action_count)

    def get_possible_action(self, game_board):
        result = []
        for i in range(0, len(game_board)):
            for j in range(0, len(game_board[i])):
                if game_board[i][j] == -1 or game_board[i][j] == -2:
                    result.append(str(j) + str(i))
        return result

    def update_q_value(self, last_state_id, action, next_state_id, reward, next_map):
        # last_state_id = state.get_id_from_map(last_state_map)
        # next_state_id = state.get_id_from_map(next_state_map)
        action_str = str(action[0]) + str(action[1])
        max_value = 0.0
        if next_state_id in self.q_matrix.keys():
            max_next_state = sorted(self.q_matrix[next_state_id].items(), key=operator.itemgetter(1), reverse=True)
            max_value = max_next_state[0][1]
        else:
            action_list = self.get_possible_action(game_board=next_map)
            # print("state")
            # print(np.matrix(next_map))
            # print("posible action:")
            # print(action_list)
            self.q_matrix[next_state_id] = {}
            for i in range(0, len(action_list)):
                self.q_matrix[next_state_id][action_list[i]] = 0.0
        # print("last-state-id= ", last_state_id)
        # print("action= ", action)
        # print("next-state-id= ",next_state_id)
        # print("q_matrix=",self.q_matrix)
        self.q_matrix[last_state_id][action_str] += (self.alpha/self.action_count) * (reward + self.discount_factor * max_value
                                                                  - self.q_matrix[last_state_id][action_str])
        # print('qmatrix.key= ',self.q_matrix.keys())
        return self.q_matrix[last_state_id][action_str]
