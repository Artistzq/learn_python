# _*_ coding: utf-8 _*_
# !/usr/bin/env python

import numpy as np
from typing import List, Optional


class State(object):
    """
    格局状态类
    """

    ORDER = 3  # type: int
    ERROR_ARRAY = np.zeros((3, 3), np.int8)  # type: np.ndarray
    CORRECT_ARRAY = np.array([[1, 2, 3], [4, 0, 5], [6, 7, 8]])  # type: np.ndarray

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
        # g(x)实际代价，此属性的信息从父结点得到（父结点g值+1）
        self.g = g
        # h(x)估价代价
        self.h = h
        # 父状态结点
        self.father = None  # type: (State, Optional)

    def set_g(self, g):
        self.g = g
        self.f = self.g + self.h

    def set_father(self, father):
        """
        设置父状态节点指针

        Args:
            father (State):
        """
        self.father = father

    def calculate_h_1(self, end_state):
        """
        计算到end_state的估计代价
        方法1：估价函数是该状态格局域目的格局位置不符的数码数目
        Args:
            end_state (State):
        """
        count = 0
        for x, y in zip(np.nditer(self.state_array), np.nditer(end_state.state_array)):
            if x != y:
                count += 1
        self.h = count
        self.f = self.g + self.h

    def calculate_f(self, end_state, method = 1):
        """
        Args:
            method (int):
            end_state (State):
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
        """显示该状态的数码格局"""
        print(self.state_array)
        print()

    def display_info(self):
        """显示该状态的数码格局，f，g，h值，和其父状态的数码格局，f，g，h值"""
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
    """操作算子类"""

    @classmethod
    def get_zero_index_in(cls, current_state: State) -> list:
        """
        返回传入状态的数组中的0（空格）的索引，为[x,y]形式，正确状态的为[1, 1]
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
    def display_full_info_of(a_state):
        """
            state (State):
        """
        if a_state is not None:
            a_state.display_info()
        else:
            print("this state is None")


if __name__ == "__main__":
    a = State(State.CORRECT_ARRAY)

    # 测试单方向移动
    b = State(np.array([[1, 0, 2], [3, 4, 5], [6, 7, 8]]))
    b.display_info()
    c = Operation.move_down(b)
    c.display_info()

    # 测试生成子状态列表
    a_child_list = Operation.get_all_next_state(a)
    for state in a_child_list:
        Operation.display_full_info_of(state)

