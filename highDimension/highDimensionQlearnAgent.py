# update q of redundant state

import numpy as np
import operator
import state
from random import randint
import random


def greedy_choose_action(sorted_actions):
    # print("sorted action"+str(sorted_actions))
    if len(sorted_actions) == 0:
        return -1, -1
    equal_action = []
    equal_action.append(sorted_actions[0])
    for i in range(1, len(sorted_actions)):
        if sorted_actions[i][1] == equal_action[0][1]:
            equal_action.append(sorted_actions[i])
    period = 100.0 / len(equal_action)
    index = 0
    random_number = randint(0, 100)
    # print("random number" + str(random_number))
    # print("period " + str(period))
    for i in range(0, len(equal_action)):
        if (i + 1) * period > random_number > i * period:
            index = i
    # print("equal action: "+str(equal_action))
    pair = sorted_actions[index]
    # print("paire action: " + str(pair))
    return int(pair[0][0]), int(pair[0][1])


def epsilon_greedy_choose_action(sorted_actions, epsilon):
    if len(sorted_actions) == 0:
        return -1, -1
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


pos_str = ['00', '01', '02', '03', '10', '11', '12', '13', '20', '21', '22', '23', '30', '31', '32', '33']
pos_rot90_str = ['03', '13', '23', '33', '02', '12', '22', '32', '01', '11', '21', '31', '00', '10', '20', '30']
pos_rot180_str = ['33', '32', '31', '30', '23', '22', '21', '20', '13', '12', '11', '10', '03', '02', '01', '00']
pos_rot270_str = ['30', '20', '10', '00', '31', '21', '11', '01', '32', '22', '12', '02', '33', '23', '13', '03']


class largeQlearnAgent:
    def __init__(self):
        super().__init__()
        self.q_matrix = {}
        self.alpha = 1.0
        self.discount_factor = 0.5
        self.bound = 0
        self.action_count = 0.0
        self.epsilon = 1.0

    def retreive_from_db(self):
        pass

    def choose_action(self, current_game_map):
        self.action_count += 1
        current_map = current_game_map
        current_state_id = state.get_id_from_map(current_game_map)
        if current_state_id not in self.q_matrix.keys():
            action_list = self.get_possible_action(game_board=current_map)
            self.q_matrix[current_state_id] = {}
            for i in range(0, len(action_list)):
                self.q_matrix[current_state_id][action_list[i]] = 0.0
        sorted_actions = sorted(self.q_matrix[current_state_id].items(), key=operator.itemgetter(1), reverse=True)
        not_seen = False
        for i in range(0, len(sorted_actions)):
            if sorted_actions[i][1] == 0:
                not_seen = True
        if not_seen:
            # return greedy_choose_action(sorted_actions)
            return epsilon_greedy_choose_action(sorted_actions=sorted_actions, epsilon=self.epsilon / self.action_count)
        if sum(self.q_matrix[current_state_id].values()) >= 0 - self.bound:
            # return greedy_choose_action(sorted_actions)
            return epsilon_greedy_choose_action(sorted_actions=sorted_actions, epsilon=self.epsilon / self.action_count)
        else:
            return -1, -1

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
            if len(self.q_matrix[next_state_id].items()) > 0:
                max_next_state = sorted(self.q_matrix[next_state_id].items(), key=operator.itemgetter(1), reverse=True)
                max_value = max_next_state[0][1]
            else:
                return
        else:
            action_list = self.get_possible_action(game_board=next_map)
            self.q_matrix[next_state_id] = {}
            for i in range(0, len(action_list)):
                self.q_matrix[next_state_id][action_list[i]] = 0.0
        self.q_matrix[last_state_id][action_str] += (self.alpha / self.action_count) * (
        reward + self.discount_factor * max_value
        - self.q_matrix[last_state_id][action_str])

        current_map = state.get_map_from_id(last_state_id, 4, 4)
        rot_90_state_id = state.get_id_from_map(np.rot90(np.array(current_map), 1))
        rot_90_next_state_id = state.get_id_from_map(np.rot90(np.array(next_map), 1))
        max_value = 0.0
        if rot_90_next_state_id not in self.q_matrix.keys():
            self.not_exist_state(rot_90_next_state_id)
        if rot_90_next_state_id in self.q_matrix.keys():
            if len(self.q_matrix[rot_90_next_state_id].items()) > 0:
                max_next_state = sorted(self.q_matrix[rot_90_next_state_id].items(), key=operator.itemgetter(1),
                                        reverse=True)
                max_value = max_next_state[0][1]
        rotate_action = pos_rot90_str[pos_str.index(action_str)]
        if rot_90_state_id not in self.q_matrix.keys():
            self.not_exist_state(rot_90_state_id)
        self.q_matrix[rot_90_state_id][rotate_action] += (self.alpha / self.action_count) * (
        reward + self.discount_factor * max_value
        - self.q_matrix[rot_90_state_id][rotate_action])

        rot_180_state_id = state.get_id_from_map(np.rot90(np.array(current_map), 2))
        rot_180_next_state_id = state.get_id_from_map(np.rot90(np.array(next_map), 2))
        max_value = 0.0
        if rot_180_next_state_id not in self.q_matrix.keys():
            self.not_exist_state(rot_180_next_state_id)
        if rot_180_next_state_id in self.q_matrix.keys():
            if len(self.q_matrix[rot_180_next_state_id].items()) > 0:
                max_next_state = sorted(self.q_matrix[rot_180_next_state_id].items(), key=operator.itemgetter(1),
                                        reverse=True)
                max_value = max_next_state[0][1]
        rotate_action = pos_rot180_str[pos_str.index(action_str)]
        if rot_180_state_id not in self.q_matrix.keys():
            self.not_exist_state(rot_180_state_id)
        self.q_matrix[rot_180_state_id][rotate_action] += (self.alpha / self.action_count) * (
        reward + self.discount_factor * max_value
        - self.q_matrix[rot_180_state_id][rotate_action])
        rot_270_state_id = state.get_id_from_map(np.rot90(np.array(current_map), 3))
        rot_270_next_state_id = state.get_id_from_map(np.rot90(np.array(next_map), 3))
        max_value = 0.0
        if rot_270_next_state_id not in self.q_matrix.keys():
            self.not_exist_state(rot_270_next_state_id)
        if rot_270_next_state_id in self.q_matrix.keys():
            if len(self.q_matrix[rot_270_next_state_id].items()) > 0:
                max_next_state = sorted(self.q_matrix[rot_270_next_state_id].items(), key=operator.itemgetter(1),
                                        reverse=True)
                max_value = max_next_state[0][1]
        rotate_action = pos_rot270_str[pos_str.index(action_str)]
        if rot_270_state_id not in self.q_matrix.keys():
            self.not_exist_state(rot_270_state_id)
        self.q_matrix[rot_270_state_id][rotate_action] += (self.alpha / self.action_count) * (
        reward + self.discount_factor * max_value
        - self.q_matrix[rot_270_state_id][rotate_action])

        return self.q_matrix[last_state_id][action_str]

    def not_exist_state(self, state_id):
        action_list = self.get_possible_action(game_board=state.get_map_from_id(state_id, 4, 4))
        self.q_matrix[state_id] = {}
        for i in range(0, len(action_list)):
            self.q_matrix[state_id][action_list[i]] = 0.0
