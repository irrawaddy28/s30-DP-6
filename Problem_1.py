'''
264 Ugly Number 2
https://leetcode.com/problems/ugly-number-ii/description/

An ugly number is a positive integer whose prime factors are limited to 2, 3, and 5. Given an integer n, return the nth ugly number.

Example 1:
Input: n = 10
Output: 12
Explanation: [1, 2, 3, 4, 5, 6, 8, 9, 10, 12] is the sequence of the first 10 ugly numbers.

Example 2:
Input: n = 1
Output: 1
Explanation: 1 has no prime factors, therefore all of its prime factors are limited to 2, 3, and 5.

Constraints:
1 <= n <= 1690

Solution:
1. Set and Min Heap
Start with 1 as the first ugly number and use a min-heap to always get the next smallest. Multiply the current ugly number by 2, 3, and 5 and add new numbers to the heap. Use a set to skip duplicates and continue until the nth ugly number is reached.
https://youtu.be/fzGieY0mH2I?t=432 (generation of ugly nos. and the problems associated with the generation)
https://youtu.be/fzGieY0mH2I?t=582 (why set and heap? set fixes the duplicate problem, heap fixes the ordering problem)
Time: O(N log M), Space: O(M), M=size of heap, N=no. of ugly nos. generated

2. Array traversal using three pointers
We start with the first ugly number as 1 and keep generating the next ones.
We multiply by 2, 3, and 5 and track the smallest new values using three pointers. Whichever value gets picked, we move its pointer forward and update that value.
https://youtu.be/fzGieY0mH2I?t=2105
Time: O(N), Space: O(1)

Hint: Use Ugly Number 2 formulations to solve similar problems such as happy number, beautiful number etc. involving prime factors.
'''
import heapq

def uglyNumber2_heap(n):
    primes = [2, 3, 5]
    h = set()
    h.add(1)
    heap = [1]
    heapq.heapify(heap)
    count = 0
    while count < n: # O(N)
        num = heapq.heappop(heap) # O(log M)
        for prime in primes: # O(3)
            x = num*prime
            if x not in h: # O(1)
                h.add(x) # O(1)
                heapq.heappush(heap, x) # O(log M)
        count += 1
    return num

def uglyNumber2_iterative(n):
    result = [0]*n
    result[0] = 1
    p2, p3, p5 = 0, 0, 0
    n2, n3, n5 = 2, 3, 5
    i = 1
    while i < n:
        result[i] = min(n2, n3, n5)
        #print(f"i = {i}\n(p2, p3, p5) = ({p2}, {p3}, {p5})\n(n2, n3, n5) = ({n2}, {n3}, {n5})\nresult = {result}\n")
        if result[i] == n2:
            p2 += 1
        if result[i] == n3:
            p3 += 1
        if result[i] == n5:
            p5 += 1
        n2, n3, n5 = 2*result[p2], 3*result[p3], 5*result[p5]
        i += 1

    return result[n-1]

def run_uglyNumber2():
    tests = [(10, 12), (1,1)]
    for test in tests:
        n, ans = test[0], test[1]
        print(f"\nn = {n}")
        for method in ['heap', 'array-traversal']:
            if method == 'heap':
                ugly = uglyNumber2_heap(n)
            elif method == 'array-traversal':
                ugly = uglyNumber2_iterative(n)
            print(f"Method {method}: Ugly number = {ugly}")
            success = (ans == ugly)
            print(f"Pass: {success}")
            if not success:
                print(f"Failed")
                return

run_uglyNumber2()