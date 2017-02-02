import time

import pygame

import state
from highDimension import highDimensionGui, highDimensionQlearnAgent

gui_board = highDimensionGui.MineSweeperGui()

# gui_board.show()
# gui_board.update()
print(" start ")
finish = False
# myAgent = qLearnAgent2.QLearnAgent2()
# myAgent = qLearnAgent.QLearnAgent()
myAgent = highDimensionQlearnAgent.largeQlearnAgent()
is_run = True
speed = 1.0
scale = 0
different_map_count = 1
while True:
    speed_scale = 1.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("learn in average: " + str(gui_board.game_count / different_map_count))
            pygame.quit()
            break
        elif event.type == pygame.MOUSEBUTTONDOWN:
            is_run, speed_scale = gui_board.mouseDown(pygame.mouse.get_pos())
    if not is_run:
        continue
    if speed / speed_scale != 0:
        if speed_scale > 1:
            scale *= 2
        else:
            scale /= 2
        speed = speed / speed_scale
        gui_board.speed = speed
    if scale > 100000:
        time.sleep(0)
        gui_board.speed = 0
    else:
        time.sleep(speed)
        gui_board.speed = speed

    x, y = myAgent.choose_action(gui_board.get_local_map())
    if x == -1:
        print("################ Shift Map #######################")
        if not gui_board.shift_window():
            print("***************** return to first window ********************: ")
            myAgent.bound += 1
        print("window: ", str(gui_board.window))
        continue
    action_tuple = (x, y)
    last_map_id = state.get_id_from_map(gui_board.get_local_map())
    res, reward = gui_board.select_tile(action_tuple)
    next_state_id = state.get_id_from_map(gui_board.get_local_map())
    new_value = myAgent.update_q_value(last_state_id=last_map_id, action=action_tuple,
                                       next_state_id=next_state_id, reward=reward, next_map=gui_board.get_local_map())

    if res == -1:
        time.sleep(speed / 10)
        myAgent.bound = 0
        gui_board.replay_game()
        finish = True
    elif res == 2:
        gui_board.restart_game()
        different_map_count+=1
        myAgent.bound = 0
        finish = True
        # time.sleep(5)
    gui_board.update_q_value(myAgent.q_matrix[next_state_id])



