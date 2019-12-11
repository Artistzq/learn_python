# _*_ coding: utf-8 _*_
# !/usr/bin/env python
from typing import List, Optional
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
        # self.start_state.father = State(State.INIT_ARRAY)
        # 终止状态节点
        self.end_state = State(end_state_array)  # type: State
        # 当前状态节点
        self.current_state = None  # type: (State, Optional)
        # open表
        self.open_list = []  # type: List[State]
        # close表
        self.close_list = []  # type: List[State]
        # 搜索的结点数
        self.count = 0
        # 搜索的时间
        self.solve_time = 0
        # 是否可解
        self.is_solvable = False
        # 是否有解
        self.has_solution = False

    def judge_solvable(self):
        a = self.start_state.get_inverse_num()
        b = self.end_state.get_inverse_num()
        if a % 2 == b % 2:
            self.is_solvable = True

    def solve(self, method=2):
        """
        解此八数码问题
        Args:
            method (int) :
        Returns:

        """
        self.judge_solvable()
        # 如果是可解的
        if self.is_solvable:
            start_time = time.perf_counter()
            self.open_list.append(self.start_state)
            self.start_state.calculate_f(self.end_state, method)
            while self.open_list:
                # sss = time.clock()
                self.current_state = self.open_list.pop()
                self.count += 1
                if self.current_state.array_equal_to(self.end_state):
                    end_time = time.perf_counter()
                    self.solve_time = end_time - start_time
                    self.has_solution = True
                    return
                # 8位数码状态均可扩展出子状态，所以生成所有的子状态
                child_list = Operation.get_all_next_state(self.current_state)  # type: List[State]
                for child_state in child_list:  # type: State
                    in_open_list, same_state_open = child_state.array_is_exist_in(self.open_list)
                    in_close_list, same_state_close = child_state.array_is_exist_in(self.close_list)
                    if not (in_open_list or in_close_list):
                        child_state.calculate_f(self.end_state, method)
                        self.open_list.append(child_state)
                    elif in_open_list:
                        # A*算法不需要判断存在的情况，若有重复无需操作，第一次找到的就是最短路径
                        pass
                        # if child_state.f < same_state_open.f:
                        #     child_state.calculate_f(self.end_state, method)
                        #     same_state_open.update_info(child_state)
                    elif in_close_list:
                        pass
                        # A*算法不需要判断存在的情况，若有重复无需操作，第一次找到的就是最短路径
                        # if child_state.f < same_state_close.f:
                        #     child_state.calculate_f(self.end_state, method)
                        #     same_state_close.update_info(child_state)
                        #     self.open_list.append(same_state_close)
                        #     self.close_list.remove(same_state_close)
                self.close_list.append(self.current_state)
                self.open_list.sort(key=attrgetter("f"), reverse=True)
                # Operation.min_sort(self.open_list)
                if self.count % 400 == 0:
                    print("搜索了", self.count, "个结点")
                    print(self.current_state.f)
                    print("open 表长：", len(self.open_list))
                    print("close 表长：", len(self.close_list))
                    print()
                    print(".\n.\n.")
                # rrr = time.clock()
                # ttt = rrr - sss
                # print(ttt, "    ", len(child_list))
            # open表空也没找到
            print("异常：open表空未搜索到解")
            return

    def display_solution(self):
        print("初始状态：")
        self.start_state.display_array()
        print("目的状态：")
        self.end_state.display_array()
        print("=============")
        if self.is_solvable and self.has_solution:
            cur_state = self.current_state
            path = []
            while cur_state is not None:
                path.append(cur_state)
                cur_state = cur_state.father
            path.reverse()
            for state in path:
                print(state.g)
                state.display_array()
            print("共检查了", self.count, "个结点")
            print("从初始状态到目的状态经历了", len(path) - 1, "次操作")
            print("检索时间：", self.solve_time)
        else:
            print("该初始状态和结束状态无法解")

    def reset(self):
        """重置解算法"""
        # open表
        self.open_list = []  # type: List[State]
        # close表
        self.close_list = []  # type: List[State]
        # 搜索的结点数
        self.count = 0


if __name__ == "__main__":
    start_array = np.array([[1, 2, 3], [4, 7, 5], [6, 0, 8]])
    test = [
        # 书上示例 0，1
        np.array([[2, 8, 3],
                  [1, 6, 4], # 0
                  [7, 0, 5]]),
        np.array([[1, 2, 3],
                  [8, 0, 4], # 1
                  [7, 6, 5]]),
        np.array([[1, 0, 3],
                  [7, 2, 4], # 和1搭配 2
                  [6, 8, 5]]),
        np.array([[1, 2, 3],
                  [8, 4, 5],
                  [7, 0, 6]]),
        # 和 correctArray搭配使用
        np.array([[1, 2, 0],
                  [3, 4, 5], # 4
                  [6, 7, 8]]),
        np.array([[1, 2, 3],
                  [0, 4, 5],
                  [6, 8, 7]]),
        np.array([[1, 2, 3],
                  [4, 5, 6],
                  [7, 8, 0]]),
        np.array([[1, 2, 3],
                  [4, 5, 6],
                  [8, 7, 0]]),
        # 最大反序 8, 9
        np.array([[8, 7, 6],
                  [5, 0, 4],  # 8
                  [3, 2, 1]]),
        np.array([[1, 2, 3],
                  [4, 0, 5],  # 9
                  [6, 7, 8]]),
        # 无解
        np.array([[2, 5, 4],
                  [3, 0, 7],  # 10
                  [1, 8, 6]]),
        np.array([[1, 2, 3],
                  [8, 0, 4],  # 11
                  [7, 6, 5]]),
        # 解二
        np.array([[5, 4, 1],
                  [6, 7, 0],  # 12
                  [2, 8, 3]]),
        np.array([[1, 2, 3],
                  [4, 5, 6],  # 13
                  [7, 8, 0]]),
        # 解三
        np.array([[5, 4, 1],
                  [6, 7, 0],  # 14
                  [2, 8, 3]]),
        np.array([[5, 4, 1],
                  [6, 7, 3],  # 15
                  [2, 8, 0]]),
        State.CORRECT_ARRAY
    ]

    solution = Solution(test[8], test[9])
    print("解：")
    solution.solve(2)
    solution.display_solution()
