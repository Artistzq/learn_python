# 汉诺塔

from typing import List

class Solution(object):

    def __init__(self, n = 4):
        self.n = n
        self.a = list(range(n, 0, -1))
        self.b = []
        self.c = []
    
    def hanoi(self, n: int, a: List, b: List, c: List):
        """把n个圆盘（从上到下），从a，由b辅助，移动到c"""
        if n >= 1:
            self.hanoi(n-1, a, c, b)
            self.move(a, c)
            self.disp()
            self.hanoi(n-1, b, a, c)

    def move(self, a: List, b: List):
        """从a取一个圆盘（最顶层），放到b上"""
        tmp = a.pop()
        b.append(tmp)

    def disp(self):
        print("a: ", self.a)
        print("b: ", self.b)
        print("c: ", self.c)
        print()

if __name__ == "__main__":
    S = Solution(5)
    S.disp()
    S.hanoi(S.n, S.a, S.c, S.b) # 从a移动到b
