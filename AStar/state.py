# _*_ coding: utf-8 _*_
# !/usr/bin/env python

import numpy as np
from enum import Enum
from typing import List
from operator import attrgetter
import copy


class Direction(Enum):
    UP = 1
    Down = 2
    LEFT = 3
    RIGHT = 4


class State(object):
    """
    表示状态结点的类
    """

    ORDER: int
    ERROR_ARRAY: np.ndarray
    CORRECT_ARRAY: np.ndarray

    ORDER = 3
    ERROR_ARRAY = np.zeros((3, 3), np.int8)
    CORRECT_ARRAY = np.array([[1, 2, 3], [4, 0, 5], [6, 7, 8]])

    @classmethod
    def set_order(cls, order):
        cls.ORDER = order

    def __init__(self, state_array: np.ndarray, f=0, g=0, h=0):
        """
        初始化某个状态，默认为3阶，实际代价和估计代价为0，当前状态为空

        Args:

            state_array (np.ndarray, optional): 状态数组. Defaults to None.
            f (int, optional): 估价函数总值
            g (int, optional): 当前代价. Defaults to 0.
            h (int, optional): 估计代价. Defaults to 0.
        """
        # 状态（数组）
        self.state_array = state_array
        # 估价函数f = g + h
        self.f = f
        # g(x)实际代价
        self.g = g
        # h(x)估价代价
        self.h = h
        # 父状态结点
        self.father = None  # type: State

    def set_g(self, g):
        """设置g的值"""
        self.g = g
        self.f = self.g + self.h

    def set_h(self, h):
        """设置h的值"""
        self.h = h
        self.f = self.g + self.h

    def get_f(self) -> int:
        """返回f=g+h的估价函数值"""
        return self.g + self.h

    def set_father(self, father):
        """
        设置父状态节点指针

        Args:
            father (State):
        """
        self.father = father

    def calculate_g(self, start_state):
        """
        计算g值
        Args:
            start_state (State):
        """

        pass

    def calculate_h_1(self, end_state):
        """
        计算到end_state的估计代价
        方法1：估价函数是该状态格局域目的格局位置不符的数码数目
        Args:
            end_state (State):
        Returns:
        """
        count = 0
        for x, y in zip(np.nditer(self.state_array), np.nditer(end_state.state_array)):
            if x != y:
                count += 1
        self.h = count
        self.f = self.g + self.h

    def calculate_f(self, start_state, end_state, method=1):
        """
        Args:
            method (int):
            start_state (State):
            end_state (State):
        Returns:
        """
        if method == 1:
            self.calculate_h_1(end_state)

    def array_equal_to(self, another_state) -> bool:
        """判断another_state_node状态结点的状态是否于本状态相同"""
        if np.array_equal(self.state_array, another_state.state_array):
            return True
        return False

    def array_is_exist_in(self, a_list):
        """
        本状态是否存在于列表a_list中（比较的是数组）
        若存在，返回True和列表中相同状态的引用，格式：(是否存在, 相同状态的引用)
        否则，返回False和错误状态
        Args:
            a_list (List[State]):

        Returns (bool), (State):

        """
        for a_state in a_list:  # type: State
            if np.array_equal(self.state_array, a_state.state_array):
                # same_state = State(a.state_array.cop())
                return True, a_state
        return False, State(State.ERROR_ARRAY)

    def display_array(self):
        print(self.state_array)
        print()

    def display_info(self):
        print(self.state_array)
        print(self.f, self.g, self.h)
        print("father is: ")
        if self.father is not None:
            print(self.father.state_array)
            print(self.father.f, self.father.g, self.father.h)
        else:
            print("father is None")
        print()


class Operation(object):
    """操作算子"""

    @classmethod
    def get_zero_coord_in(cls, current_state: State) -> list:
        """
        返回传入状态的数组中的0（空格）坐标，坐标[x,y]形式，最终状态的为[2, 2]
        """
        coord = np.where(current_state.state_array == 0)
        return [coord[0][0] + 1, coord[1][0] + 1]

    @classmethod
    def get_zero_index_in(cls, current_state: State) -> list:
        """
        返回传入状态的数组中的0（空格）的索引，为坐标值-1，索引 [x,y]形式，最终状态的为[1, 1]
        """
        index = np.where(current_state.state_array == 0)
        return [index[0][0], index[1][0]]

    @classmethod
    def move_up(cls, current_state: State):
        x, y = cls.get_zero_index_in(current_state)
        if x != 0:  # 如果空格不在最上一行，就可以向上移动
            temp_state = State(current_state.state_array.copy(), current_state.f, current_state.g, current_state.h)
            temp_state.state_array[x][y], temp_state.state_array[x - 1][y] \
                = temp_state.state_array[x - 1][y], temp_state.state_array[x][y]
            temp_state.set_father(current_state)
            temp_state.set_g(temp_state.g + 1)
            return temp_state
        else:
            return None

    @classmethod
    def move_down(cls, current_state: State):
        x, y = cls.get_zero_index_in(current_state)
        if x != State.ORDER - 1:  # 如果空格不在最下一行，就可以向下移动
            temp_state = State(current_state.state_array.copy(), current_state.f, current_state.g, current_state.h)
            temp_state.state_array[x][y], temp_state.state_array[x + 1][y] \
                = temp_state.state_array[x + 1][y], temp_state.state_array[x][y]
            temp_state.set_father(current_state)
            temp_state.set_g(temp_state.g + 1)
            return temp_state
        else:
            return None

    @classmethod
    def move_left(cls, current_state: State):
        x, y = cls.get_zero_index_in(current_state)
        if y != 0:  # 如果空格不在最左一列，就可以向左移动
            temp_state = State(current_state.state_array.copy(), current_state.f, current_state.g, current_state.h)
            temp_state.state_array[x][y], temp_state.state_array[x][y - 1] \
                = temp_state.state_array[x][y - 1], temp_state.state_array[x][y]
            temp_state.set_father(current_state)
            temp_state.set_g(temp_state.g + 1)
            return temp_state
        else:
            return None

    @classmethod
    def move_right(cls, current_state: State):
        x, y = cls.get_zero_index_in(current_state)
        if y != State.ORDER - 1:  # 如果空格不在最右列，就可以往右移
            temp_state = State(current_state.state_array.copy(), current_state.f, current_state.g, current_state.h)
            temp_state.state_array[x][y], temp_state.state_array[x][y + 1] \
                = temp_state.state_array[x][y + 1], temp_state.state_array[x][y]
            temp_state.set_father(current_state)
            temp_state.set_g(temp_state.g + 1)
            return temp_state
        else:
            return None

    @classmethod
    def get_all_next_state(cls, current_state: State) -> list:
        """返回current_state的所有可以扩展的状态，装在列表中返回"""
        # 子状态列表
        child_states = []  # type: List[State]

        up_state = cls.move_up(current_state)
        if up_state is not None:
            child_states.append(up_state)

        down_state = cls.move_down(current_state)
        if down_state is not None:
            child_states.append(down_state)

        left_state = cls.move_left(current_state)
        if left_state is not None:
            child_states.append(left_state)

        right_state = cls.move_right(current_state)
        if right_state is not None:
            child_states.append(right_state)

        return child_states

    @staticmethod
    def find_min_f_from(states):
        """
        找到状态表中第一个f值最小的状态
        Args:
            states (List[State]):

        Returns (State):

        """
        # 表非空
        if states:
            min_state = states[0]
            for state in states:
                if state.f < min_state.f:
                    min_state = state
            return min_state

    @staticmethod
    def display_full_info_of(a_state):
        """
            state (State):
        """
        if a_state is not None:
            a_state.display_info()
        else:
            print("this state is None")


if __name__ == "__main__":
    a = State(np.arange(State.ORDER ** 2).reshape(State.ORDER, State.ORDER))
    aa = State(np.array([1, 2, 3, 4, 5, 6, 0, 7, 8]).reshape(State.ORDER, State.ORDER))
    a.calculate_f(aa, State(State.CORRECT_ARRAY))
    a.display_info()
    State(State.CORRECT_ARRAY).display_info()

    a.calculate_f(aa, State(State.CORRECT_ARRAY), 1)
    a.display_info()
    State(State.CORRECT_ARRAY).display_info()

    # a = State(np.array([1,2,3,4,5,6,0,7,8]).reshape(State.ORDER, State.ORDER))
    # a = State(State.CORRECT_ARRAY)
    # a_child_list = Operation.get_all_next_state(a)
    # for state in a_child_list:
    #     Operation.display_full_info_of(state)
    # aa_list = Operation.get_all_next_state(a_child_list[0])
    # for state in aa_list:
    #     Operation.display_full_info_of(state)

    # b = State(State.CORRECT_ARRAY, 10)
    # c = State(State.ERROR_ARRAY, 8)
    # d = State(np.array([[1, 2, 3], [4, 0, 5], [6, 7, 8]]), 9)

    # 测试单方向移动
    # b = State(np.array([[1, 0, 2], [3, 4, 5], [6, 7, 8]]))
    # b.display_info()
    #     # g = Operation.move_down(b)
    #     # g.display_info()

    # print(id(b),id(c))
    # open_l = [b, c, d]
    # for i in open_l:
    #     i.display_info()
    #
    # open_l.sort(key=attrgetter("f"), reverse=True)
    # for i in open_l:
    #     i.display_info()

    # exist_open, same_state_open = d.array_is_exist_in(open_l)
    # e = c # type: # State
    # print(id(e), id(c), id(open_l[1]))
    # open_l.remove(c)
    # print(id(e), id(c), id(open_l[1]))
    # e.display_array()

    # e.display_array()

    # if exist_open:
    #     print("local's d", id(b))
    #     print(exist_open)
    #     print("same's id" ,id(same_state_open))
    #     # same_state_open.display_array()
