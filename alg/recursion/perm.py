# 全排列

from typing import List

import numpy as np


class Solution():
    
    def perm(self, numbers: List) -> List:
        if len(numbers) == 1:
            return [numbers]
        else:
            result_matrix = []
            for number in numbers:
                rest_numbers = numbers.copy()
                rest_numbers.remove(number)
                rest_matrix = self.perm(rest_numbers)
                for rest in rest_matrix:
                    result_matrix.append([number]+ rest)
            return result_matrix

if __name__ == "__main__":
    S = Solution()
    n = [1,2,3,4,5]
    r = np.array(S.perm(n))
    print(r)
    print(len(r), "个排列方式")
    