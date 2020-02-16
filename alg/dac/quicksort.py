
class Solution():
    
    def quicksort(self, arraylist, start, end, method=1):
        if start >= end:
            return
        else:
            if method == 1:
                middle = self.partition(arraylist, start, end)
            elif method == 2:
                middle = self.partition_2(arraylist, start, end)
            self.quicksort(arraylist, start, middle-1, method)
            self.quicksort(arraylist, middle+1, end, method)

    def partition(self, arraylist, start, end) -> int:
        pivot = arraylist[start]
        while start < end:
            while arraylist[end] >= pivot and start < end:
                end -= 1
            arraylist[start] = arraylist[end]
            while arraylist[start] <= pivot and start < end:
                start += 1
            arraylist[end] = arraylist[start]
        arraylist[start] = pivot
        return start

    def partition_2(self, arraylist, start, end) -> int:
        pivot = start
        start += 1
        while start < end:
            while arraylist[end] >= arraylist[pivot] and start < end:
                end -= 1
            while arraylist[start] <= arraylist[pivot] and start < end:
                start += 1
            arraylist[start], arraylist[end] = arraylist[end], arraylist[start]
        arraylist[start], arraylist[pivot] = arraylist[pivot], arraylist[start]
        return start

    def quicksort_py(self, arraylist):
        if len(arraylist)<2:
            return arraylist
        else:
            pivot = arraylist[0]
            front = [i for i in arraylist[1:] if i <= pivot]
            back = [i for i in arraylist[1:] if i > pivot]
            return self.quicksort_py(front) + [pivot] + self.quicksort_py(back)

if __name__ == "__main__":
    S = Solution()
    n = [1.9,3,5,6,7,5,4,2,36,7]
    S.quicksort(n, 0, 9)
    print(n)