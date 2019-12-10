# _*_ coding: utf-8 _*_
# !/usr/bin/env python

import numpy as np
from typing import List, Optional
from enum import Enum
import time


class Direction(Enum):
    NO_MOVE = 0
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


class State(object):
    """
    格局状态类
    """

    ORDER = 3  # type: int
    ZERO_ARRAY = np.zeros((3, 3), np.int8)  # type: np.ndarray
    ERROR_ARRAY = np.array([[0, 1, 2], [3, 4, 5], [6, 7, 8]])
    CORRECT_ARRAY = np.array([[1, 2, 3], [4, 0, 5], [6, 7, 8]])  # type: np.ndarray
    INIT_ARRAY = np.zeros((3, 3), np.int8)  # type: np.ndarray

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
        # 上一次从什么方向移动而得到
        self.last_direction_from = Direction.NO_MOVE

    def set_g(self, g):
        self.g = g
        self.f = self.g + self.h

    def update_info(self, new_state):
        """
        根据新状态(数码格局相同)，更新自己的价值信息
        Args:
            new_state (State): 新状态
        Returns:
        """
        self.f = new_state.f
        self.g = new_state.g
        self.h = new_state.h
        self.father = new_state.father
        self.last_direction_from = new_state.last_direction_from

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

    def calculate_h_2(self, end_state):
        """
        计算到end_state的估计代价
        方法2：估价函数是该状态格局域目的格局位置的曼哈顿距离
        Args:
            end_state (State):
        """
        dist = 0
        for index_self_x in range(State.ORDER):
            for index_self_y in range(State.ORDER):
                temp = np.where(end_state.state_array == self.state_array[index_self_x][index_self_y])
                index_end = [temp[0][0], temp[1][0]]
                dist += abs(index_end[0] - index_self_x) + abs(index_end[1] - index_self_y)
        self.h = dist

    def calculate_h_3(self, end_state):
        count_1 = 0
        for x, y in zip(np.nditer(self.state_array), np.nditer(end_state.state_array)):
            if x != y:
                count_1 += 1
        count_2 = 0
        xy = list(self.state_array.flatten().tolist())
        xy.remove(0)
        for x in range(len(xy)):
            for y in range(x, len(xy)):
                if xy[x] > xy[y]:
                    count_2 += 1
        self.h = count_1 + count_2

    def calculate_f(self, end_state, method=1):
        """
        Args:
            method (int):
            end_state (State):
        """
        if method == 1:
            self.calculate_h_1(end_state)
            self.f = self.g + self.h
        elif method == 2:
            self.calculate_h_2(end_state)
            self.f = self.g + self.h
        elif method == 3:
            self.calculate_h_3(end_state)
            self.f = self.g + self.h

    def array_equal_to(self, another_state) -> bool:
        """判断another_state_node状态结点的状态是否于本状态相同"""
        if another_state is not None:
            if np.array_equal(self.state_array, another_state.state_array):
                return True
            return False
        else:
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
        return False, State(State.ZERO_ARRAY)

    def get_inverse_num(self):
        """
        Returns (int): 逆序数
        """
        count = 0
        xy = list(self.state_array.flatten().tolist())
        xy.remove(0)
        for x in range(len(xy)):
            for y in range(x, len(xy)):
                if xy[x] > xy[y]:
                    count += 1
        return count

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
    def move(cls, current_state: State, direction):
        """
        将当前状态的数组中的0，向direction指示的方向移动
        Args:
            current_state(State): 当前状态
            direction(Direction):方向
        Returns(State):
        """
        # 获得0的索引
        x, y = cls.get_zero_index_in(current_state)
        temp_state = State(current_state.state_array.copy())

        if direction == Direction.NO_MOVE:
            return None
        elif direction == Direction.UP:
            if x != 0:  # 如果空格不在最上一行，就可以向上移动
                temp_state.state_array[x][y], temp_state.state_array[x - 1][y] \
                    = temp_state.state_array[x - 1][y], temp_state.state_array[x][y]
                temp_state.set_father(current_state)
                temp_state.set_g(current_state.g + 1)
                temp_state.last_direction_from = Direction.DOWN
                return temp_state
            else:
                return None
        elif direction == Direction.DOWN:
            if x != State.ORDER - 1:  # 如果空格不在最下一行，就可以向下移动
                temp_state.state_array[x][y], temp_state.state_array[x + 1][y] \
                    = temp_state.state_array[x + 1][y], temp_state.state_array[x][y]
                temp_state.set_father(current_state)
                temp_state.set_g(current_state.g + 1)
                temp_state.last_direction_from = Direction.UP
                return temp_state
            else:
                return None
        elif direction == Direction.LEFT:
            if y != 0:  # 如果空格不在最左列，就可以往左移
                temp_state.state_array[x][y], temp_state.state_array[x][y - 1] \
                    = temp_state.state_array[x][y - 1], temp_state.state_array[x][y]
                temp_state.set_father(current_state)
                temp_state.set_g(current_state.g + 1)
                temp_state.last_direction_from = Direction.RIGHT
                return temp_state
            else:
                return None
        elif direction == Direction.RIGHT:
            if y != State.ORDER - 1:  # 如果空格不在最右列，就可以往右移
                temp_state.state_array[x][y], temp_state.state_array[x][y + 1] \
                    = temp_state.state_array[x][y + 1], temp_state.state_array[x][y]
                temp_state.set_father(current_state)
                temp_state.set_g(current_state.g + 1)
                temp_state.last_direction_from = Direction.LEFT
                return temp_state
            else:
                return None
        else:
            print("错误的方向")
            return None

    @classmethod
    def get_all_next_state(cls, father_state: State) -> list:
        """返回current_state的所有可以扩展的状态，装在列表中返回"""
        # 子状态列表
        child_states = []  # type: List[State]

        if father_state is None:
            print("错误，空状态无法扩展")
            return child_states

        for direction in Direction:
            child_state = cls.move(father_state, direction)
            if child_state is not None:
                if father_state.father is None:  # 如果是初始节点（父节点为空）
                    child_states.append(child_state)
                else:  # 否则要判断重不重复（比如往下移动又往上移动）
                    if direction != father_state.last_direction_from:
                        child_states.append(child_state)
        return child_states

    @classmethod
    def min_sort(cls, state_list: List[State]):
        """把最小值和列表末尾的值互换"""
        min_f_index = 0
        min_f = state_list[min_f_index].f
        for index in range(len(state_list)):
            if state_list[index].f < min_f:
                min_f = state_list[index].f
                min_f_index = index
        state_list[min_f_index], state_list[-1] = state_list[-1], state_list[min_f_index]


if __name__ == "__main__":
    a = State(State.CORRECT_ARRAY)

    # 测试单方向移动
    b = State(np.array([[0, 1, 2], [3, 4, 5], [6, 7, 8]]))
    b.display_info()
    c = Operation.move(b, Direction.RIGHT)
    c.display_info()

    # 测试生成子状态列表
    a_child_list = Operation.get_all_next_state(a)
    aa_child_list = Operation.get_all_next_state(a_child_list[0])
    aaa_child_list = Operation.get_all_next_state(aa_child_list[0])
    for state in a_child_list:
        state.display_info()
    for state in aa_child_list:
        state.display_info()

    # 测试计算H值

    t = [1, 2, 3]
    t[0], t[1] = t[1], t[0]
    t[-1], t[-1] = t[-1], t[-1]
    print(t)

    # 测试numpy复制速度, 还是对象.copy最快
    # start = time.perf_counter()
    #
    # temp_array = np.zeros((3,3), np.int8)
    # np.copyto(temp_array, a.state_array)
    #
    # end = time.perf_counter()
    # print(temp_array, end - start)
    #
    #
    # start = time.perf_counter()
    #
    # temp_b = a.state_array.copy()
    #
    # end = time.perf_counter()
    # print(temp_b, end - start)
    #
    #
    # start = time.perf_counter()
    #
    # temp_c = np.copy(a.state_array)
    #
    # end = time.perf_counter()
    # print(temp_c, end - start)
