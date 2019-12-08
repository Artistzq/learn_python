# _*_ coding: utf-8 _*_
# !/usr/bin/env python
from typing import List
import numpy as np
from operator import attrgetter
from state import State
from state import Operation
import time


class Solution(object):
    """
    A*算法
    """

    def __init__(self, start_state_array, end_state_array=State.CORRECT_ARRAY):
        # 开始状态节点
        self.start_state = State(start_state_array)  # type: State
        # 终止状态节点
        self.end_state = State(end_state_array)  # type: State
        # 当前状态节点
        self.current_state = None  # type: State
        # open表
        self.open_list = []  # type: List[State]
        # close表
        self.close_list = []  # type: List[State]
        # 搜索的结点数
        self.count = 0

    def solute_2(self):
        self.open_list.append(self.start_state)
        while self.open_list:
            # 记得改成按关键字找最小值，现在是加一个就排序
            self.current_state = Operation.find_min_f_from(self.open_list)
            if self.current_state.array_equal_to(self.end_state):
                return self.current_state
            # 8位数码状态均可扩展出子状态，所以生成所有的子状态
            child_list = Operation.get_all_next_state(self.current_state)
            for child_state in child_list:  # type: State
                exist_open, same_state_open = child_state.array_is_exist_in(self.open_list)
                exist_close, same_state_close = child_state.array_is_exist_in(self.close_list)
                if not (exist_open or exist_close):
                    child_state.calculate_f(self.start_state, self.end_state)
                    # child_list.remove(child_state)
                    self.open_list.append(child_state)
                elif exist_open:
                    if child_state.f < same_state_open.f:
                        same_state_open.set_father(child_state.father)
                        same_state_open.calculate_f(self.start_state, self.end_state)
                elif exist_close:
                    if child_state.f < same_state_close.f:
                        self.open_list.append(same_state_close)
                        self.close_list.remove(same_state_close)
                        same_state_close.calculate_f()
            self.open_list.remove(self.current_state)
            self.close_list.append(self.current_state)
            self.count += 1
            if self.count % 1000 == 0:
                print("检查了", self.count, "个结点")
                print("open 表长：", len(self.open_list))
                print("close 表长：", len(self.close_list))
                print()
        return State(State.ERROR_ARRAY)

    def solute(self, method = 1):
        """
        解此问题，搜索算法
        Args:
            method (int) :
        Returns:

        """
        self.open_list.append(self.start_state)
        while self.open_list:
            self.current_state = self.open_list.pop()
            if self.current_state.array_equal_to(self.end_state):
                return self.current_state
            # 8位数码状态均可扩展出子状态，所以生成所有的子状态
            child_list = Operation.get_all_next_state(self.current_state)
            for child_state in child_list:  # type: State
                exist_open, same_state_open = child_state.array_is_exist_in(self.open_list)
                exist_close, same_state_close = child_state.array_is_exist_in(self.close_list)
                if not (exist_open or exist_close):
                    child_state.calculate_f(self.start_state, self.end_state, method)
                    # child_list.remove(child_state)
                    self.open_list.append(child_state)
                elif exist_open:
                    if child_state.f < same_state_open.f:
                        same_state_open.set_father(child_state.father)
                        same_state_open.calculate_f(self.start_state, self.end_state, method)
                elif exist_close:
                    if child_state.f < same_state_close.f:
                        self.open_list.append(same_state_close)
                        self.close_list.remove(same_state_close)
                        same_state_close.calculate_f()
            self.close_list.append(self.current_state)
            self.open_list.sort(key=attrgetter("f"), reverse=True)
            self.count += 1
            if self.count % 1000 == 0:
                print("检查了", self.count, "个结点")
                print("open 表长：", len(self.open_list))
                print("close 表长：", len(self.close_list))
                print()
        return State(State.ERROR_ARRAY)

    def display_path(self):
        cur_state = self.current_state
        print("共检查了", self.count, "个结点")
        path = []
        while cur_state is not None:
            path.append(cur_state)
            cur_state = cur_state.father
        path.reverse()
        for state in path:
            state.display_array()

    def reset(self):
        # 当前状态节点
        self.current_state = State(start_state_array)  # type: State
        # open表
        self.open_list = []  # type: List[State]
        # close表
        self.close_list = []  # type: List[State]
        # 搜索的结点数
        self.count = 0

if __name__ == "__main__":
    start_state_array = np.array([[1, 2, 3], [4, 7, 5], [6, 0, 8]])
    test = []
    test.append(State.CORRECT_ARRAY)
    test.append(np.array([[2, 8, 3], [1, 6, 4], [7, 0, 5]]))
    test.append(np.array([[1, 2, 3], [8, 0, 4], [7, 6, 5]]))
    test.append(np.array([[1, 2, 3], [8, 4, 5], [7, 6, 0]]))
    test.append(np.array([[1, 2, 3], [8, 4, 5], [7, 0, 6]]))
    test.append(np.array([[1, 2, 0], [3, 4, 5], [6, 7, 8]]))
    test.append(np.array([[1, 2, 3], [0, 4, 5], [6, 8, 7]])) # error state
    # end_state_array = np.array([[1, 2, 0], [3, 4, 5], [6, 7, 8]])
    solution = Solution(test[0], test[5])

    start = time.perf_counter()
    solution.solute()
    # solution.solute_2()
    end = time.perf_counter()
    solution.display_path()
    print("检索时间：", end-start)
