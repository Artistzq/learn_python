# 求划分个数

class Solution():
    
    def equation_count(self, n, m):
        if n == 1 or m == 1:
            return 1
        elif n < m:
            return self.equation_count(n, n)
        elif n == m:
            return self.equation_count(n, n-1) + 1
        else:
            return self.equation_count(n, m-1) + self.equation_count(n-m, m)

if __name__ == "__main__":
    S = Solution()
    n = 50
    result = S.equation_count(n, n)
    print(result)