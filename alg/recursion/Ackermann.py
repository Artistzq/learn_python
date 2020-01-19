
class Solution(object):
    
    def ackermann(self, n, m):
        """http://yuenshome.lofter.com/post/459740_962ca41"""
        if n == 1 and m == 0:
            return 2
        elif n == 0 and m >= 0:
            return 1
        elif m == 0 and n >= 2:
            return n + 2
        elif n>=1 and m>=1:
            return self.ackermann(self.ackermann(n-1, m), m-1)

    def ackermann_wiki(self, m, n):
        """http://mathworld.wolfram.com/AckermannFunction.html"""
        if m==0:
            return n+1
        elif n==0:
            return self.ackermann_wiki(m-1, 1)
        else:
            return self.ackermann_wiki(m-1, self.ackermann_wiki(m, n-1))

if __name__ == "__main__":
    S = Solution()
    a = S.ackermann(2, 2)
    b = S.ackermann_wiki(2, 2)
    # ？？？？？？？？？？？？？？？？？？？？？？？？？？？？
    # which one
    print(a, b)