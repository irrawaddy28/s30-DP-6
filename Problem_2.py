'''
5 Longest Palindromic Substring (LPS)
https://leetcode.com/problems/longest-palindromic-substring/description/

Given a string s, return the LPS in s.

Example 1:
Input: s = "babad"
Output: "bab"
Explanation: "aba" is also a valid answer.

Example 2:
Input: s = "cbbd"
Output: "bb"

Constraints:
1 <= s.length <= 1000
s consist of only digits and English letters.

1. DP bottom-up
For every start index j, we check for each end index i (i >= j) if s[j..i] is a palindrome.
We use a 2D dp array where dp[i][j] tells if substring from j to i is a palindrome.
Define dp[i][j] = substring s[i...j] a palindrome or not (bool)
where 0<=i<=N-1, 0<=j<=N-1.
Thus start indices are in columns, end indices are in rows.
Every time a dp[i][j] is True, we check the len of the substring and save the substring as lps if this substring is longer than all previously detected substring.
https://youtu.be/HgTVjpgRTIk?t=254 (lecture)
Time: O(N^2), Space: O(N^2)

2. DP bottom-up using gap (easier to understand)
This is no different from the DP non-gap approach. The only difference is the way we fill the DP matrix. We fill the upper triangle of the DP matrix filling the main diagonal first, then the sub diagonals above the main diagonal.

Define dp[start][end] = substring s[start...end] a palindrome or not (bool)
where start = start index of substring, end = end index of substring,
0<=start<=N-1, 0<=end<=N-1
Thus start indices are in rows, end indices are in columns.

In the gap strategy, we fill the dp by the lengths of the substrings.
a) length 1 substrings are always palindromes.
Hence, dp[start][end]=1, where start=end, 0<=start<=N-1
Since start=end, the main diagonal is filled first.

b) length 2 substrings are palindromes only if first char == second char
For eg, s = 'ab'. s is a palindrome only if s[0] == s[1]
Hence, if s[start] == s[end]:  # end = start + 1
          dp[start][end] = True

c) length K (2 < K <= N) strings are palindromes if
  a) s[start] == s[end] and
  b) s[start+1,...,end-1] = dp[start+1][end-1] is True
Hence, if s[start] == s[end] and dp[start+1][end-1]:
          dp[start][end] = True (end = start + K -1)

https://youtu.be/UflHuQj6MVA?t=184 (gap strategy)
Time: O(N^2), Space: O(N^2)

3. Iterative (expand around the middle)
Consider a middle element positioned at the center of a string with both left and right pointers pointing to the mid element. We then move the left pointer by 1 step to the left and the right pointer by one step to the right. If both the left and right characters match, it becomes a 3 length palindrome. We
keep expanding (left--, right++) until the left and right characters do not match. We record the max length of the substring that formed a valid palindrome.

There are two possible cases
a) to find odd-length palindromes, the middle element is a single element
b) to find even-length palindromes, there are two middle elements (mid, mid + 1)

Thus, we need to consider both the odd and even cases. We record the max len of palindrome discovered in both odd and even cases. The final longest palindrome = max (odd len palindrome, even len palindrome)

We consider every element in the string as a potential middle element s[0,...,N-1] and execute the two expansions (case a and b). We discover the longest palindrome for each middle element and update if we discover a new palindrome that is longer than all previously discovered palindromes.

The advantage of this approach (over DP) is that takes O(1) space (DP takes
O(N^2) space)

https://youtu.be/HgTVjpgRTIk?t=1733 (lecture)
https://www.youtube.com/watch?v=0CKUjDcUYYA
Time: O(N^2), Space: O(1)

'''
def mprint(matrix):
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in matrix]))

def longestPalindrome_dp(s: str) -> str:
    ''' Time: O(N^2), Space: O(N^2) '''
    if not s:
        return s, []

    N = len(s)
    max_len = 0
    start, end = -1, -1
    dp = [[False]*N for _ in range(N)]
    for i in range(N):
        for j in range(i+1):
            len_sub = i-j-1 # inner substr between j and i
            if s[i] == s[j]:
                if len_sub < 2:
                    dp[i][j] = True
                elif dp[i-1][j+1] == True:
                    dp[i][j] = True

            if dp[i][j] == True:
                if i - j + 1 > max_len:
                    max_len = i - j  + 1
                    start = j
                    end = i
    return s[start:end+1], dp

def longestPalindrome_dp_gap(s: str) -> str:
    ''' Time: O(N^2), Space: O(N^2) '''
    if not s:
        return s, []
    N = len(s)
    max_len = 1
    lps = s[0]
    start, end = -1, -1
    dp = [[False]*N for _ in range(N)]

    # length 1 strings are always palindromes
    for start in range(N):
        end = start
        dp[start][end] = True


    # length 2 strings are palindromes if first char == last char
    for start in range(N-1):
        end = start + 1
        if s[start] == s[end]:
            dp[start][end] = True
            max_len = 2
            lps = s[start:end+1]

    # length K (2 < K <= N) strings are palindromes if
    # a) s[start] == s[end] and
    # b) s[start+1,...,end-1] = dp[start+1][end-1] is True
    for ln in range(3, N+1):
        for start in range(N-ln+1):
            end = ln + start - 1
            if s[start] == s[end]:
                if dp[start+1][end-1]:
                    dp[start][end] = True

                    if ln > max_len:
                        max_len = ln
                        lps = s[start:end+1]

    return lps, dp

def longestPalindrome_iterative(s: str) -> str:
    ''' Time: O(N^2), Space: O(1) '''
    def expandAroundCenter(s, left, right):
        nonlocal max_len, start, end
        while (left >= 0 and right <= N-1) and s[left] == s[right]:
            left -= 1 # decrease left
            right += 1 # increase right
        # at this point, either l/r have gone out of bounds or they are
        # pointing to mismatched characters
        left += 1
        right -= 1
        ln = right - left + 1
        if ln > max_len:
            max_len = ln
            start = left
            end = right
        return

    if not s:
        return s
    N = len(s)
    start, end = 0, 0
    max_len = 0
    # Expand around the middle element to check for palindrome.
    # We consider every element in the string as a potential middle element.
    for mid in range(N):
         # for odd-length palindromes, the middle element is a single element
        expandAroundCenter(s, mid, mid)
        if (mid < N-1):
            # for even-length palindromes, there are two middle elements (mid, mid + 1)
            expandAroundCenter(s, mid, mid+1)

    return s[start:end+1]


def run_longestPalindromeSubstring():
    tests = [("babab", "babab"),
             ("cbbd", "bb"),
             ("aaaabbaa", "aabbaa"),
             ("a", "a"),
             ("ab", "a"),
             ("abc", "a"),
             ("", ""),
    ]
    for test in tests:
        s, ans = test[0], test[1]
        print(f"-------\ns = {s}")
        for method in ['dp', 'dp-gap', 'iterative']:
            if method == 'dp':
                lps, dp = longestPalindrome_dp(s)
                print(f"DP matrix:")
                mprint(dp)
            elif method == 'dp-gap':
                lps, dp = longestPalindrome_dp_gap(s)
                print(f"DP matrix:")
                mprint(dp)
            elif method == 'iterative':
                lps = longestPalindrome_iterative(s)
            print(f"Method {method}: Longest Palindrome Substring: {lps}")
            success = (lps == ans)
            print(f"Pass: {success}\n")
            if not success:
                print(f"Failed")
                return

run_longestPalindromeSubstring()