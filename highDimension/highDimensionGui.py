from random import randint
import pygame
import time
import numpy as np
import Buttons

TOP_CONTROL_HEIGHT = 300

TILE_WIDTH = 150
TILE_HEIGHT = 150
import math
# TOP_MARGIN = 100
REWARD_LIST = [9, 8, 7, 6, 5, 4, 3, 2, 1]
import random

class MineSweeperGui():
    def __init__(self, ):
        self.output_file = open("agent2.txt", 'w')
        self.game_count = 0.0
        self.win_count = 0.0
        self.lost_count = 0.0
        self.speed = 1
        self.is_running = True
        self.is_game_over = False
        self.is_win = False
        self.margin = 5
        self.min_count = 7.0
        self.minesweeper_size = 6
        self.d = self.min_count / (self.minesweeper_size * self.minesweeper_size)
        self.mines_density = (self.min_count + 0.0) / (self.minesweeper_size * self.minesweeper_size)
        self.game_map = []
        self.mins_pos = []
        self.GAME_WIDTH_SCREEN = 640
        self.GAME_HEIGHT_SCREEN = 480
        self.generate_mines()
        self.generate_map()
        self.window = (0, 0, 3, 3)
        self.window_size = 4
        self.GAME_WIDTH_SCREEN = (
                                     self.minesweeper_size * TILE_WIDTH) + self.minesweeper_size * self.margin + self.margin
        # self.GAME_HEIGHT_SCREEN = ((self.minesweeper_size * TILE_HEIGHT) + self.minesweeper_size * 2 * self.margin)*2
        self.GAME_HEIGHT_SCREEN = (
                                      self.minesweeper_size * TILE_HEIGHT) + self.minesweeper_size * self.margin + self.margin
        self.screen = pygame.display.set_mode((self.GAME_WIDTH_SCREEN, self.GAME_HEIGHT_SCREEN + TOP_CONTROL_HEIGHT))
        self.preview_screen = pygame.display.set_mode(
            (self.GAME_WIDTH_SCREEN, self.GAME_HEIGHT_SCREEN + TOP_CONTROL_HEIGHT))
        self.selected_tile_count = 0
        self.mins_img = pygame.image.load('res/ic_mins.png')
        self.mins_img = pygame.transform.scale(self.mins_img,
                                               (TILE_HEIGHT,
                                                TILE_HEIGHT))
        zero_img = pygame.image.load('res/ic_zero.png')
        zero_img = pygame.transform.scale(zero_img,
                                          (TILE_HEIGHT,
                                           TILE_HEIGHT))
        one_img = pygame.image.load('res/ic_one.png')
        one_img = pygame.transform.scale(one_img,
                                         (TILE_HEIGHT,
                                          TILE_HEIGHT))
        two_img = pygame.image.load('res/ic_two.png')
        two_img = pygame.transform.scale(two_img,
                                         (TILE_HEIGHT,
                                          TILE_HEIGHT))
        three_img = pygame.image.load('res/ic_three.png')
        three_img = pygame.transform.scale(three_img,
                                           (TILE_HEIGHT,
                                            TILE_HEIGHT))
        four_img = pygame.image.load('res/ic_four.png')
        four_img = pygame.transform.scale(four_img,
                                          (TILE_HEIGHT,
                                           TILE_HEIGHT))
        five_img = pygame.image.load('res/ic_five.png')
        five_img = pygame.transform.scale(five_img,
                                          (TILE_HEIGHT,
                                           TILE_HEIGHT))
        six_img = pygame.image.load('res/ic_six.png')
        six_img = pygame.transform.scale(six_img,
                                         (TILE_HEIGHT,
                                          TILE_HEIGHT))
        seven_img = pygame.image.load('res/ic_seven.png')
        seven_img = pygame.transform.scale(seven_img,
                                           (TILE_HEIGHT,
                                            TILE_HEIGHT))
        eight_img = pygame.image.load('res/ic_eight.png')
        eight_img = pygame.transform.scale(eight_img,
                                           (TILE_HEIGHT,
                                            TILE_HEIGHT))
        self.image_numbers = [zero_img, one_img, two_img, three_img, four_img, five_img, six_img, seven_img, eight_img]
        self.white_color = (255, 255, 255)
        self.red_color = (255, 0, 0)
        self.black_color = (0, 0, 0)
        self.grey_color = (80, 80, 80)
        self.play_btn_color = (0, 255, 26)
        self.pause_btn_color = (255, 0, 102)
        self.speed_up_color = (255, 139, 61)
        self.speed_down_color = (0, 255, 128)
        self.screen.fill(self.white_color)

        for i in range(0, len(self.game_map)):
            for j in range(0, len(self.game_map)):
                x = i * (TILE_WIDTH + self.margin) + self.margin
                y = j * (TILE_HEIGHT + self.margin) + self.margin
                pygame.draw.rect(self.screen, self.grey_color, pygame.Rect(x, y, TILE_WIDTH, TILE_HEIGHT))
        self.font = None
        self.play_pause_btn = Buttons.Button()
        self.speed_up_btn = Buttons.Button()
        self.speed_down_btn = Buttons.Button()
        x_draw = self.GAME_WIDTH_SCREEN / 2 - 50
        y_draw = self.minesweeper_size * TILE_HEIGHT + TOP_CONTROL_HEIGHT / 4
        # Parameters:               surface,      color,       x,   y,   length, height, width,    text,      text_color
        self.play_pause_btn.create_button(self.screen, self.pause_btn_color, x_draw, y_draw, 100, 50, 100,
                                          "   Pause   ", self.black_color)
        self.speed_down_btn.create_button(self.screen, self.speed_down_color, x_draw - 150, y_draw, 100, 50, 100,
                                          " Speed Down ", self.black_color)
        self.speed_up_btn.create_button(self.screen, self.speed_up_color, x_draw + 150, y_draw, 100, 50, 100,
                                        " Speed Up ", self.black_color)
        self.show()
        self.font = pygame.font.SysFont("monospace", 25, bold=True)
        x_draw = 0
        width = x_draw + self.GAME_WIDTH_SCREEN
        y_draw = self.minesweeper_size * (TILE_HEIGHT + self.margin) + TOP_CONTROL_HEIGHT / 2
        height = TOP_CONTROL_HEIGHT / 2
        pygame.draw.rect(self.screen, self.white_color, pygame.Rect(x_draw, y_draw, width, height))
        y_draw = self.minesweeper_size * (TILE_HEIGHT + self.margin) + TOP_CONTROL_HEIGHT / 2
        status = "     Game Count= " + str(self.game_count)
        self.screen.blit(self.font.render(status, True, (255, 0, 0)), (x_draw, y_draw))
        y_draw = self.minesweeper_size * (TILE_HEIGHT + self.margin) + TOP_CONTROL_HEIGHT / 2 + TOP_CONTROL_HEIGHT / 6
        status = "     Win rate= % 0"
        self.screen.blit(self.font.render(status, True, (255, 0, 0)), (x_draw, y_draw))
        y_draw = self.minesweeper_size * TILE_HEIGHT + TOP_CONTROL_HEIGHT / 8
        x_draw = self.GAME_WIDTH_SCREEN / 2 - 50
        try:
            status = "Speed=  " + str(int(1 / self.speed)) + "x"
        except:
            status = "Speed=  nx"
        self.screen.blit(self.font.render(status, True, (255, 0, 0)), (x_draw, y_draw))

    def generate_map(self):
        game_map = []  # [[-2, -1, -1, -1], [-1, -2, -1, -1], [-1, 2, -1, -1], [-1, -1, -1, -2]]
        for i in range(0, self.minesweeper_size):
            temp = []
            for j in range(0, self.minesweeper_size):
                min_exist = False
                for k in range(0, len(self.mins_pos)):
                    if j == self.mins_pos[k][0] and i == self.mins_pos[k][1]:
                        temp.append(-2)
                        min_exist = True
                if not min_exist:
                    temp.append(-1)
            game_map.append(temp)
        self.game_map = game_map

    def generate_mines(self):

        # if self.game_count%4==0:
        #     self.min_count=7
        # else:
        #     self.min_count=6
        # mins_pos = [(0, 0), (2, 1), (2, 2), (0, 3)]
        mins_pos = []
        while len(mins_pos) < self.min_count:
            # for i in range(0, self.minesweeper_size):
            #     for j in range(0, self.minesweeper_size):
            i = random.randint(0, self.minesweeper_size-1)
            j = random.randint(0, self.minesweeper_size-1)
            rand_number = random.random()
            if i == 0:
                if j == 0:
                    p = math.pow(1. - self.d, 4.)
                    if rand_number < p:
                        continue
                elif j == self.minesweeper_size - 1:
                    p = math.pow(1. - self.d, 4.)
                    if rand_number < p:
                        continue
                else:
                    p = math.pow(1. - self.d, 6.)
                    if rand_number < p:
                        continue
            elif i == self.minesweeper_size - 1:
                if j == 0:
                    p = math.pow(1. - self.d, 4.)
                    if rand_number < p:
                        continue
                elif j == self.minesweeper_size - 1:
                    p = math.pow(1. - self.d, 4.)
                    if rand_number < p:
                        continue
                else:
                    p = math.pow(1. - self.d, 6.)
                    if rand_number < p:
                        continue
            else:
                if j == 0:
                    p = math.pow(1 - self.d, 6.)
                    if rand_number < p:
                        continue
                elif j == self.minesweeper_size - 1:
                    p = math.pow(1 - self.d, 6.)
                    if rand_number < p:
                        continue
                else:
                    p = math.pow(1 - self.d, 9.)
                    if rand_number < p:
                        continue
            # if rand_number < self.mines_density * 100:
            if (j, i) not in mins_pos:
                mins_pos.append((j, i))

        self.mins_pos = mins_pos
        return self.mins_pos

        self.mins_pos = mins_pos
        return self.mins_pos

    def show(self):
        pygame.init()
        pygame.display.set_caption('QLearning Agent Minesweper')
        # x_draw = self.GAME_WIDTH_SCREEN/2 - 50
        # y_draw = self.minesweeper_size*TILE_HEIGHT + TOP_CONTROL_HEIGHT/2
        # pygame.draw.rect(self.screen, self.grey_color, pygame.Rect(x_draw, y_draw, 50, 20))
        # self.font = pygame.font.SysFont("monospace", 25, bold=True)
        # self.screen.blit(self.font.render(" Pause ", True, (255, 0, 0)), (x_draw, y_draw))
        # pygame.display.update()

    def update(self, position):
        x = position[0] * (TILE_WIDTH + self.margin) + self.margin
        y = position[1] * (TILE_HEIGHT + self.margin) + self.margin
        pygame.draw.rect(self.screen, self.red_color, pygame.Rect(x, y, TILE_WIDTH, TILE_HEIGHT))
        pygame.display.update()
        time.sleep(self.speed / 10)
        pygame.draw.rect(self.screen, self.white_color, pygame.Rect(x, y, TILE_WIDTH, TILE_HEIGHT))
        temp_pos = (
            position[0] * (TILE_WIDTH + self.margin) + self.margin,
            position[1] * (TILE_WIDTH + self.margin) + self.margin)
        self.screen.blit(self.image_numbers[self.game_map[position[1]][position[0]]], temp_pos)
        pygame.display.update()

    def update_q_value(self, position_value_dict):
        for key in position_value_dict.keys():
            x = int(key[0]) + self.window[0]
            y = int(key[1]) + self.window[1]
            if self.game_map[y][x] not in [-1, -2]:
                continue
            x_draw = x * (TILE_WIDTH + self.margin) + self.margin
            y_draw = y * (TILE_HEIGHT + self.margin) + self.margin
            pygame.draw.rect(self.screen, self.grey_color, pygame.Rect(x_draw, y_draw, TILE_WIDTH, TILE_HEIGHT))
            str_val = str(position_value_dict[key])
            y_draw += TILE_HEIGHT / 2
            self.screen.blit(self.font.render(str_val[0:5], True, (255, 0, 0)), (x_draw, y_draw))
        pygame.display.update()

    # return -1 if select mines and game over
    # return 1 if select number
    # return 2 if agent win
    def select_tile(self, local_position):
        position = (local_position[0] + self.window[0], local_position[1] + self.window[1])
        if self.is_game_over:
            return -10
        if self.is_win:
            return 2
        if self.game_map[position[1]][position[0]] >= 0:
            return 0
        # print self.game_map
        for i in range(0, len(self.mins_pos)):
            if self.mins_pos[i] == position:
                self.lost_count += 1
                x = position[0] * (TILE_WIDTH + self.margin) + self.margin
                y = position[1] * (TILE_HEIGHT + self.margin) + self.margin
                width = TILE_WIDTH  # - 2 * self.margin
                height = TILE_HEIGHT  # - 2 * self.margin
                pygame.draw.rect(self.screen, self.red_color, pygame.Rect(x, y, width, height))
                temp_pos = (position[0] * (TILE_WIDTH + self.margin) + self.margin,
                            position[1] * (TILE_WIDTH + self.margin) + self.margin)
                self.screen.blit(self.mins_img, temp_pos)

                pygame.display.update()
                self.is_game_over = True
                print("=============================== Game Over ====================================")
                return -1, -10
        mine_around = self.measure_mine_count_around_point(position)
        self.game_map[position[1]][position[0]] = mine_around
        self.update(position)
        if mine_around == 0:
            self.zero_item_selected(position=position)
        self.selected_tile_count += 1
        # print(np.matrix(self.game_map))
        if self.selected_tile_count == (self.minesweeper_size * self.minesweeper_size) - self.min_count:
            self.win_count += 1
            return 2, REWARD_LIST[mine_around]
        return 1, REWARD_LIST[mine_around]

    def zero_item_selected(self, position):
        if position[0] == 0:
            if position[1] == 0:
                if self.game_map[position[1] + 1][position[0]] == -1:
                    self.expand_zero(position=(position[0], position[1] + 1))
                if self.game_map[position[1]][position[0] + 1] == -1:
                    self.expand_zero(position=(position[0] + 1, position[1]))
                if self.game_map[position[1] + 1][position[0] + 1] == -1:
                    self.expand_zero(position=(position[0] + 1, position[1] + 1))
            elif position[1] == self.minesweeper_size - 1:
                if self.game_map[position[1] - 1][position[0]] == -1:
                    self.expand_zero(position=(position[0], position[1] - 1))
                if self.game_map[position[1] - 1][position[0] + 1] == -1:
                    self.expand_zero(position=(position[0] + 1, position[1] - 1))
                if self.game_map[position[1]][position[0] + 1] == -1:
                    self.expand_zero(position=(position[0] + 1, position[1]))
            else:
                if self.game_map[position[1] - 1][position[0]] == -1:
                    self.expand_zero(position=(position[0], position[1] - 1))
                if self.game_map[position[1] + 1][position[0]] == -1:
                    self.expand_zero(position=(position[0], position[1] + 1))
                if self.game_map[position[1] - 1][position[0] + 1] == -1:
                    self.expand_zero(position=(position[0] + 1, position[1] - 1))
                if self.game_map[position[1]][position[0] + 1] == -1:
                    self.expand_zero(position=(position[0] + 1, position[1]))
                if self.game_map[position[1] + 1][position[0] + 1] == -1:
                    self.expand_zero(position=(position[0] + 1, position[1] + 1))
        elif position[0] == self.minesweeper_size - 1:
            if position[1] == 0:
                if self.game_map[position[1]][position[0] - 1] == -1:
                    self.expand_zero(position=(position[0] - 1, position[1]))
                if self.game_map[position[1] + 1][position[0] - 1] == -1:
                    self.expand_zero(position=(position[0] - 1, position[1] + 1))
                if self.game_map[position[1] + 1][position[0]] == -1:
                    self.expand_zero(position=(position[0], position[1] + 1))
            elif position[1] == self.minesweeper_size - 1:
                if self.game_map[position[1] - 1][position[0] - 1] == -1:
                    self.expand_zero(position=(position[0] - 1, position[1] - 1))
                if self.game_map[position[1]][position[0] - 1] == -1:
                    self.expand_zero(position=(position[0] - 1, position[1]))
                if self.game_map[position[1] - 1][position[0]] == -1:
                    self.expand_zero(position=(position[0], position[1] - 1))
            else:
                if self.game_map[position[1] - 1][position[0] - 1] == -1:
                    self.expand_zero(position=(position[0] - 1, position[1] - 1))
                if self.game_map[position[1]][position[0] - 1] == -1:
                    self.expand_zero(position=(position[0] - 1, position[1]))
                if self.game_map[position[1] + 1][position[0] - 1] == -1:
                    self.expand_zero(position=(position[0] - 1, position[1] + 1))
                if self.game_map[position[1] - 1][position[0]] == -1:
                    self.expand_zero(position=(position[0], position[1] - 1))
                if self.game_map[position[1] + 1][position[0]] == -1:
                    self.expand_zero(position=(position[0], position[1] + 1))
        else:
            if position[1] == 0:
                if self.game_map[position[1]][position[0] - 1] == -1:
                    self.expand_zero(position=(position[0] - 1, position[1]))
                if self.game_map[position[1] + 1][position[0] - 1] == -1:
                    self.expand_zero(position=(position[0] - 1, position[1] + 1))
                if self.game_map[position[1] + 1][position[0]] == -1:
                    self.expand_zero(position=(position[0], position[1] + 1))
                if self.game_map[position[1]][position[0] + 1] == -1:
                    self.expand_zero(position=(position[0] + 1, position[1]))
                if self.game_map[position[1] + 1][position[0] + 1] == -1:
                    self.expand_zero(position=(position[0] + 1, position[1] + 1))
            elif position[1] == self.minesweeper_size - 1:
                if self.game_map[position[1] - 1][position[0] - 1] == -1:
                    self.expand_zero(position=(position[0] - 1, position[1] - 1))
                if self.game_map[position[1]][position[0] - 1] == -1:
                    self.expand_zero(position=(position[0] - 1, position[1]))
                if self.game_map[position[1] - 1][position[0]] == -1:
                    self.expand_zero(position=(position[0], position[1] - 1))
                if self.game_map[position[1] - 1][position[0] + 1] == -1:
                    self.expand_zero(position=(position[0] + 1, position[1] - 1))
                if self.game_map[position[1]][position[0] + 1] == -1:
                    self.expand_zero(position=(position[0] + 1, position[1]))
            else:
                if self.game_map[position[1] - 1][position[0] - 1] == -1:
                    # print("left-top")
                    self.expand_zero(position=(position[0] - 1, position[1] - 1))
                if self.game_map[position[1]][position[0] - 1] == -1:
                    # print("left")
                    self.expand_zero(position=(position[0] - 1, position[1]))
                if self.game_map[position[1] + 1][position[0] - 1] == -1:
                    # print("left-bottom")
                    self.expand_zero(position=(position[0] - 1, position[1] + 1))
                if self.game_map[position[1] - 1][position[0]] == -1:
                    # print("top")
                    self.expand_zero(position=(position[0], position[1] - 1))
                if self.game_map[position[1] + 1][position[0]] == -1:
                    # print("bottom")
                    self.expand_zero(position=(position[0], position[1] + 1))
                if self.game_map[position[1] - 1][position[0] + 1] == -1:
                    # print("top-right")
                    self.expand_zero(position=(position[0] + 1, position[1] - 1))
                if self.game_map[position[1]][position[0] + 1] == -1:
                    # print("right")
                    self.expand_zero(position=(position[0] + 1, position[1]))
                if self.game_map[position[1] + 1][position[0] + 1] == -1:
                    # print("right-bottom")
                    self.expand_zero(position=(position[0] + 1, position[1] + 1))

    def measure_mine_count_around_point(self, position):
        mine_around = 0
        if position[0] == 0:
            if position[1] == 0:
                if self.game_map[position[1]][position[0] + 1] == -2:
                    mine_around += 1
                if self.game_map[position[1] + 1][position[0]] == -2:
                    mine_around += 1
                if self.game_map[position[1] + 1][position[0] + 1] == -2:
                    mine_around += 1
            elif position[1] == self.minesweeper_size - 1:
                if self.game_map[position[1] - 1][position[0]] == -2:
                    mine_around += 1
                if self.game_map[position[1] - 1][position[0] + 1] == -2:
                    mine_around += 1
                if self.game_map[position[1]][position[0] + 1] == -2:
                    mine_around += 1
            else:
                if self.game_map[position[1] - 1][position[0]] == -2:
                    mine_around += 1
                if self.game_map[position[1] - 1][position[0] + 1] == -2:
                    mine_around += 1
                if self.game_map[position[1]][position[0] + 1] == -2:
                    mine_around += 1
                if self.game_map[position[1] + 1][position[0]] == -2:
                    mine_around += 1
                if self.game_map[position[1] + 1][position[0] + 1] == -2:
                    mine_around += 1
        elif position[0] == self.minesweeper_size - 1:
            if position[1] == 0:
                if self.game_map[position[1]][position[0] - 1] == -2:
                    mine_around += 1
                if self.game_map[position[1] + 1][position[0] - 1] == -2:
                    mine_around += 1
                if self.game_map[position[1] + 1][position[0]] == -2:
                    mine_around += 1
            elif position[1] == self.minesweeper_size - 1:
                if self.game_map[position[1] - 1][position[0] - 1] == -2:
                    mine_around += 1
                if self.game_map[position[1] - 1][position[0]] == -2:
                    mine_around += 1
                if self.game_map[position[1]][position[0] - 1] == -2:
                    mine_around += 1
            else:
                if self.game_map[position[1] - 1][position[0] - 1] == -2:
                    mine_around += 1
                if self.game_map[position[1] - 1][position[0]] == -2:
                    mine_around += 1
                if self.game_map[position[1]][position[0] - 1] == -2:
                    mine_around += 1
                if self.game_map[position[1] + 1][position[0] - 1] == -2:
                    mine_around += 1
                if self.game_map[position[1] + 1][position[0]] == -2:
                    mine_around += 1
        else:
            if position[1] == 0:
                if self.game_map[position[1]][position[0] - 1] == -2:
                    mine_around += 1
                if self.game_map[position[1]][position[0] + 1] == -2:
                    mine_around += 1
                if self.game_map[position[1] + 1][position[0] - 1] == -2:
                    mine_around += 1
                if self.game_map[position[1] + 1][position[0]] == -2:
                    mine_around += 1
                if self.game_map[position[1] + 1][position[0] + 1] == -2:
                    mine_around += 1
            elif position[1] == self.minesweeper_size - 1:
                if self.game_map[position[1] - 1][position[0] - 1] == -2:
                    mine_around += 1
                if self.game_map[position[1] - 1][position[0]] == -2:
                    mine_around += 1
                if self.game_map[position[1] - 1][position[0] + 1] == -2:
                    mine_around += 1
                if self.game_map[position[1]][position[0] - 1] == -2:
                    mine_around += 1
                if self.game_map[position[1]][position[0] + 1] == -2:
                    mine_around += 1

            else:
                if self.game_map[position[1] - 1][position[0] - 1] == -2:
                    mine_around += 1
                if self.game_map[position[1] - 1][position[0]] == -2:
                    mine_around += 1
                if self.game_map[position[1] - 1][position[0] + 1] == -2:
                    mine_around += 1
                if self.game_map[position[1]][position[0] - 1] == -2:
                    mine_around += 1
                if self.game_map[position[1]][position[0] + 1] == -2:
                    mine_around += 1
                if self.game_map[position[1] + 1][position[0] - 1] == -2:
                    mine_around += 1
                if self.game_map[position[1] + 1][position[0]] == -2:
                    mine_around += 1
                if self.game_map[position[1] + 1][position[0] + 1] == -2:
                    mine_around += 1
        return mine_around

    def expand_zero(self, position):
        # print("expand_zero : ", position[0], position[1])
        if self.game_map[position[1]][position[0]] != -1:
            # print("expand_zero : Seen")
            return
        min_count = self.measure_mine_count_around_point(position=position)
        if min_count != 0:
            # print("expand_zero : not zero")
            return
        # print("expand_zero : is zero ")
        self.game_map[position[1]][position[0]] = min_count
        self.update(position)
        if min_count == 0:
            self.zero_item_selected(position=position)
        self.selected_tile_count += 1
        if self.selected_tile_count == (self.minesweeper_size * self.minesweeper_size) - self.min_count:
            self.is_win = True

    def restart_game(self):
        self.generate_mines()
        self.generate_map()
        self.replay_game()

    def replay_game(self):
        self.window = (0, 0, 3, 3)
        self.game_count += 1
        self.is_win = False
        self.selected_tile_count = 0
        self.is_game_over = False
        self.screen.fill(self.white_color)
        for i in range(0, self.minesweeper_size):
            for j in range(0, self.minesweeper_size):
                if self.game_map[i][j] != -2:
                    self.game_map[i][j] = -1
        for i in range(0, len(self.game_map)):
            for j in range(0, len(self.game_map)):
                x = i * (TILE_WIDTH + self.margin) + self.margin
                y = j * (TILE_HEIGHT + self.margin) + self.margin
                width = (TILE_WIDTH)  # - 2 * self.margin
                height = (TILE_HEIGHT)  # - 2 * self.margin
                pygame.draw.rect(self.screen, self.grey_color, pygame.Rect(x, y, width, height))
        x_draw = self.GAME_WIDTH_SCREEN / 2 - 50
        y_draw = self.minesweeper_size * TILE_HEIGHT + TOP_CONTROL_HEIGHT / 4
        self.play_pause_btn.create_button(self.screen, self.pause_btn_color, x_draw, y_draw, 100, 50, 100, "   Pause   "
                                          , self.black_color)
        self.speed_down_btn.create_button(self.screen, self.speed_down_color, x_draw - 150, y_draw, 100, 50, 100,
                                          " Speed Down ", self.black_color)
        self.speed_up_btn.create_button(self.screen, self.speed_up_color, x_draw + 150, y_draw, 100, 50, 100,
                                        " Speed Up ", self.black_color)

        x_draw = 0
        width = x_draw + self.GAME_WIDTH_SCREEN
        y_draw = self.minesweeper_size * (TILE_HEIGHT + self.margin) + TOP_CONTROL_HEIGHT / 2
        height = TOP_CONTROL_HEIGHT / 2
        pygame.draw.rect(self.screen, self.white_color, pygame.Rect(x_draw, y_draw, width, height))
        y_draw = self.minesweeper_size * (TILE_HEIGHT + self.margin) + TOP_CONTROL_HEIGHT / 2
        status = "     Game Count= " + str(self.game_count)
        self.screen.blit(self.font.render(status, True, (255, 0, 0)), (x_draw, y_draw))
        y_draw = self.minesweeper_size * (TILE_HEIGHT + self.margin) + TOP_CONTROL_HEIGHT / 2 + TOP_CONTROL_HEIGHT / 6
        status = "     Win rate= % " + str(self.win_count / self.game_count)
        self.output_file.write("\ngame count=" + str(self.game_count))
        self.output_file.write("\n" + status)
        self.output_file.write("\n=================================")
        self.screen.blit(self.font.render(status, True, (255, 0, 0)), (x_draw, y_draw))

        y_draw = self.minesweeper_size * TILE_HEIGHT + TOP_CONTROL_HEIGHT / 8
        x_draw = self.GAME_WIDTH_SCREEN / 2 - 50
        try:
            status = "Speed=  " + str(int(1 / self.speed)) + "x"
        except:
            status = "Speed=  nx"
        self.screen.blit(self.font.render(status, True, (255, 0, 0)), (x_draw, y_draw))

    def mouseDown(self, position):
        speed = 1
        if self.play_pause_btn.pressed(position):
            x_draw = self.GAME_WIDTH_SCREEN / 2 - 50
            y_draw = self.minesweeper_size * TILE_HEIGHT + TOP_CONTROL_HEIGHT / 4
            if self.is_running:
                self.play_pause_btn.create_button(self.screen, self.play_btn_color, x_draw, y_draw, 100, 50, 100,
                                                  "   Play   ",
                                                  self.black_color)
                self.is_running = False
            else:
                self.play_pause_btn.create_button(self.screen, self.pause_btn_color, x_draw, y_draw, 100, 50, 100,
                                                  "   Pause   ",
                                                  self.black_color)
                self.is_running = True
            pygame.display.update()
        elif self.speed_down_btn.pressed(position):
            speed = 0.5
        elif self.speed_up_btn.pressed(position):
            speed = 2
        if speed != 1:
            y_draw = self.minesweeper_size * TILE_HEIGHT + TOP_CONTROL_HEIGHT / 8
            x_draw = self.GAME_WIDTH_SCREEN / 2 - 50
            try:
                status = "Speed=  " + str(int(1 / self.speed)) + "x"
            except:
                status = "Speed=  nx"
            self.screen.blit(self.font.render(status, True, (255, 0, 0)), (x_draw, y_draw))
            pygame.display.update()

        return self.is_running, speed

    def get_local_map(self):
        local_map = []
        for i in range(0, 4):
            temp = []
            for j in range(0, 4):
                temp.append(self.game_map[i + self.window[1]][j + self.window[0]])
            local_map.append(temp)
        return local_map

    def shift_window(self):
        # if window right of map
        if self.window[2] == len(self.game_map[0])-1:
            if self.window[3] == len(self.game_map)-1:
                self.window = (0, 0, self.window_size-1, self.window_size-1)
                return False
            else:
                self.window = (0, self.window[1] + 1, self.window_size-1, self.window[3] + 1)
                return True
        else:
            self.window = (self.window[0] + 1, self.window[1], self.window[2] + 1, self.window[3])
            return True
