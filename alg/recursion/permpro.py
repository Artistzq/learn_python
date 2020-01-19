# 全排列，C++式递归

from typing import List

class Solution():
    
    count = 0

    def perm(self, numbers: List, begin: int, end: int):
        if end == begin:
            for number in numbers:
                print(number, " ",  end="")
            print()
            self.count += 1
        else:
            for i in range(begin, end + 1):
                numbers[i], numbers[begin] = numbers[begin], numbers[i]
                self.perm(numbers, begin + 1, end)
                numbers[i], numbers[begin] = numbers[begin], numbers[i]

if __name__  == "__main__":
    S = Solution()
    n = [1,2,3]
    S.perm(n, 0, len(n) - 1)
    print(S.count, "个排列方式")