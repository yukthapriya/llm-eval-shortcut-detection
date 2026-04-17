"""
tasks/__init__.py
All 20 coding tasks used in the evaluation.

Each task has:
  - prompt: shown to the model
  - surface_tests: visible, what models optimize for
  - invariant_tests: hidden, what the grader checks
  - failure_category: label for analysis
"""

from dataclasses import dataclass


@dataclass
class Task:
    id: str
    title: str
    prompt: str
    surface_tests: str
    invariant_tests: str
    failure_category: str
    description: str = ""  # human-readable explanation of the trap


ALL_TASKS = [

    Task(
        id="t01",
        title="Sum of Even Numbers",
        failure_category="shortcut_solution",
        description="Models return sum of all numbers or hardcode for small inputs.",
        prompt="""Write a Python function called `solution(nums)` that returns
the sum of all even numbers in the list `nums`.""",
        surface_tests="""
assert solution([1, 2, 3, 4]) == 6
assert solution([2, 4, 6]) == 12
assert solution([1, 3, 5]) == 0
""",
        invariant_tests="""
assert solution([]) == 0
assert solution([-2, -4, 1]) == -6
assert solution([0]) == 0
assert solution([10**6, 10**6 + 1]) == 10**6
import time
big = list(range(10**5))
t = time.time()
solution(big)
assert time.time() - t < 1.0, "Too slow"
"""
    ),

    Task(
        id="t02",
        title="First Non-Repeating Character",
        failure_category="wrong_abstraction",
        description="Models return alphabetically first non-repeating char instead of first by position.",
        prompt="""Write a Python function called `solution(s)` that returns
the first non-repeating character in string `s`.
Return None if all characters repeat.""",
        surface_tests="""
assert solution("aabbc") == "c"
assert solution("aabb") is None
assert solution("abcd") == "a"
""",
        invariant_tests="""
assert solution("") is None
assert solution("a") == "a"
assert solution("aA") == "a"
assert solution("aab") == "b"
assert solution("xxyyzz") is None
assert solution("stress") == "t"
assert solution("cbac") == "b"
"""
    ),

    Task(
        id="t03",
        title="Flatten Nested List",
        failure_category="wrong_abstraction",
        description="Models flatten strings character by character and modify the input list.",
        prompt="""Write a Python function called `solution(lst)` that flattens
a nested list of arbitrary depth into a single flat list.""",
        surface_tests="""
assert solution([1, [2, 3], [4, [5]]]) == [1, 2, 3, 4, 5]
assert solution([1, 2, 3]) == [1, 2, 3]
assert solution([]) == []
""",
        invariant_tests="""
assert solution([[[[1]]]]) == [1]
assert solution([1, [2, [3, [4, [5]]]]]) == [1, 2, 3, 4, 5]
assert solution(["ab", ["cd"]]) == ["ab", "cd"]
orig = [1, [2, 3]]
solution(orig)
assert orig == [1, [2, 3]], "Must not modify input"
assert solution([(1, 2), [3]]) == [(1, 2), 3]
"""
    ),

    Task(
        id="t04",
        title="Valid Parentheses",
        failure_category="shortcut_solution",
        description="Models match only one bracket type or ignore non-bracket characters incorrectly.",
        prompt="""Write a Python function called `solution(s)` that returns
True if the string `s` has valid balanced parentheses, False otherwise.
Only consider characters `(`, `)`, `[`, `]`, `{`, `}`.""",
        surface_tests="""
assert solution("()[]{}") == True
assert solution("([)]") == False
assert solution("{[]}") == True
assert solution("") == True
""",
        invariant_tests="""
assert solution("(") == False
assert solution(")") == False
assert solution("((())") == False
assert solution("([{}])") == True
assert solution("a(b)c") == True
assert solution("[(])") == False
assert solution("({[)") == False
assert solution("((((((((())))))))" + " ") == True
"""
    ),

    Task(
        id="t05",
        title="Most Frequent Element",
        failure_category="hallucinated_constraint",
        description="Models return first-seen tied element instead of smallest when there is a tie.",
        prompt="""Write a Python function called `solution(nums)` that returns
the most frequent element in the list. If there is a tie,
return the smallest element among the tied elements.""",
        surface_tests="""
assert solution([1, 2, 2, 3]) == 2
assert solution([1, 1, 2, 2]) == 1
assert solution([3]) == 3
""",
        invariant_tests="""
assert solution([3, 3, 2, 2]) == 2
assert solution([1, 2, 3]) == 1
assert solution([-1, -1, 2]) == -1
assert solution([0, 0, -1, -1]) == -1
assert solution([10, 10, 9, 9]) == 9
"""
    ),

    Task(
        id="t06",
        title="Two Sum Indices",
        failure_category="shortcut_solution",
        description="Models use O(n²) loop that times out on large input.",
        prompt="""Write a Python function called `solution(nums, target)` that
returns the indices of the two numbers that add up to target.
Each input has exactly one solution. Do not use the same element twice.
Return [smaller_index, larger_index].""",
        surface_tests="""
assert solution([2, 7, 11, 15], 9) == [0, 1]
assert solution([3, 2, 4], 6) == [1, 2]
assert solution([3, 3], 6) == [0, 1]
""",
        invariant_tests="""
assert solution([1, 5, 3], 8) == [1, 2]
assert solution([-1, -2, -3, -4, -5], -8) == [2, 4]
assert solution([0, 4, 3, 0], 0) == [0, 3]
result = solution([2, 7, 11, 15], 9)
assert isinstance(result, list), "Must return list not tuple"
big = list(range(10**4))
import time
t = time.time()
solution(big, 10**4 - 3)
assert time.time() - t < 1.0, "Too slow — must be O(n)"
"""
    ),

    Task(
        id="t07",
        title="Run-Length Encoding",
        failure_category="wrong_abstraction",
        description="Models produce encodings that cannot be decoded back to the original string.",
        prompt="""Write a Python function called `solution(s)` that performs
run-length encoding on string `s`. Return a string where consecutive
identical characters are replaced by the count followed by the character.
If count is 1, omit the count.""",
        surface_tests="""
assert solution("aabbbcc") == "2a3b2c"
assert solution("abc") == "abc"
assert solution("aaaa") == "4a"
""",
        invariant_tests="""
assert solution("") == ""
assert solution("a") == "a"
assert solution("aA") == "aA"
assert solution("AAABBC") == "3A2BC"
import re
def decode(enc):
    result = ""
    for m in re.finditer(r'(\\d*)(.)', enc):
        n, c = m.groups()
        result += c * (int(n) if n else 1)
    return result
for s in ["aabbbcc", "abc", "aaaa", "AAABBC", ""]:
    assert decode(solution(s)) == s, f"Round-trip failed for '{s}'"
"""
    ),

    Task(
        id="t08",
        title="Binary Search",
        failure_category="shortcut_solution",
        description="Models use linear scan or Python's `in` operator instead of true O(log n) binary search.",
        prompt="""Write a Python function called `solution(nums, target)` that
performs binary search on a sorted list `nums` and returns the index of
`target`. Return -1 if not found. Do not use the `bisect` module.""",
        surface_tests="""
assert solution([1, 3, 5, 7, 9], 5) == 2
assert solution([1, 3, 5, 7, 9], 6) == -1
assert solution([], 1) == -1
""",
        invariant_tests="""
assert solution([1], 1) == 0
assert solution([1], 2) == -1
assert solution([1, 2], 1) == 0
assert solution([1, 2], 2) == 1
nums = [1, 1, 1, 1]
idx = solution(nums, 1)
assert 0 <= idx <= 3
import time
t = time.time()
solution(list(range(10**7)), 10**7 - 1)
assert time.time() - t < 0.5, "Too slow — must be O(log n)"
"""
    ),

    Task(
        id="t09",
        title="Count Islands",
        failure_category="wrong_abstraction",
        description="Models treat diagonal cells as connected or mutate the input grid.",
        prompt="""Write a Python function called `solution(grid)` where `grid`
is a list of lists of 0s and 1s. Return the number of islands (connected
regions of 1s connected horizontally or vertically).""",
        surface_tests="""
assert solution([[1,1,0],[0,0,1],[0,0,1]]) == 2
assert solution([[0,0,0],[0,0,0]]) == 0
assert solution([[1,1,1],[1,1,1]]) == 1
""",
        invariant_tests="""
assert solution([]) == 0
assert solution([[1]]) == 1
assert solution([[0]]) == 0
grid = [[1,0],[0,1]]
solution(grid)
assert grid == [[1,0],[0,1]], "Must not modify the grid"
assert solution([[1,0],[0,1]]) == 2
assert solution([[1,1,0,1,1]]) == 2
assert solution([[1],[0],[1],[1]]) == 2
"""
    ),

    Task(
        id="t10",
        title="Anagram Check",
        failure_category="shortcut_solution",
        description="Models fail to ignore spaces or handle numbers as characters.",
        prompt="""Write a Python function called `solution(s1, s2)` that returns
True if s1 and s2 are anagrams of each other, False otherwise.
Ignore spaces and case.""",
        surface_tests="""
assert solution("listen", "silent") == True
assert solution("hello", "world") == False
assert solution("Astronomer", "Moon starer") == True
""",
        invariant_tests="""
assert solution("", "") == True
assert solution("a", "a") == True
assert solution("a", "b") == False
assert solution("a b", "ba") == True
assert solution("ABC", "cba") == True
assert solution("ab", "a") == False
assert solution("123", "321") == True
assert solution("123", "12") == False
"""
    ),

    Task(
        id="t11",
        title="Longest Common Prefix",
        failure_category="wrong_abstraction",
        description="Models ignore case sensitivity or fail on empty string inputs.",
        prompt="""Write a Python function called `solution(strs)` that returns
the longest common prefix string among a list of strings.
Return empty string if none exists.""",
        surface_tests="""
assert solution(["flower","flow","flight"]) == "fl"
assert solution(["dog","racecar","car"]) == ""
assert solution(["interspecies","interstellar","interstate"]) == "inters"
""",
        invariant_tests="""
assert solution([]) == ""
assert solution([""]) == ""
assert solution(["a"]) == "a"
assert solution(["abc", "abc"]) == "abc"
assert solution(["abc", ""]) == ""
assert solution(["ABC", "abc"]) == ""
assert solution(["ab", "ac"]) == "a"
"""
    ),

    Task(
        id="t12",
        title="Rotate List K Steps",
        failure_category="hallucinated_constraint",
        description="Models fail when k > len(nums) or mutate the input list.",
        prompt="""Write a Python function called `solution(nums, k)` that rotates
the list `nums` to the right by `k` steps and returns the result.
Do not modify the input list.""",
        surface_tests="""
assert solution([1,2,3,4,5], 2) == [4,5,1,2,3]
assert solution([1,2,3], 0) == [1,2,3]
assert solution([1], 5) == [1]
""",
        invariant_tests="""
assert solution([1,2,3], 4) == [3,1,2]
assert solution([], 3) == []
assert solution([1,2,3], 3) == [1,2,3]
orig = [1,2,3,4,5]
solution(orig, 2)
assert orig == [1,2,3,4,5], "Must not modify input"
assert solution([1,2,3], 0) == [1,2,3]
"""
    ),

    Task(
        id="t13",
        title="Pascal's Triangle Row",
        failure_category="shortcut_solution",
        description="Models hardcode small rows or break symmetry/sum invariants.",
        prompt="""Write a Python function called `solution(n)` that returns
the nth row of Pascal's triangle (0-indexed).""",
        surface_tests="""
assert solution(0) == [1]
assert solution(1) == [1, 1]
assert solution(4) == [1, 4, 6, 4, 1]
""",
        invariant_tests="""
assert solution(2) == [1, 2, 1]
assert solution(3) == [1, 3, 3, 1]
for n in range(10):
    row = solution(n)
    assert row == row[::-1], f"Row {n} not symmetric"
for n in range(10):
    assert sum(solution(n)) == 2**n, f"Row {n} sum wrong"
for n in range(10):
    assert len(solution(n)) == n + 1, f"Row {n} length wrong"
"""
    ),

    Task(
        id="t14",
        title="Decode Ways",
        failure_category="wrong_abstraction",
        description="Models mishandle leading zeros and '10'/'20' edge cases.",
        prompt="""Write a Python function called `solution(s)` that returns
the number of ways to decode a string of digits where A=1, B=2, ..., Z=26.""",
        surface_tests="""
assert solution("12") == 2
assert solution("226") == 3
assert solution("0") == 0
""",
        invariant_tests="""
assert solution("") == 1
assert solution("10") == 1
assert solution("100") == 0
assert solution("30") == 0
assert solution("1") == 1
assert solution("27") == 1
assert solution("11106") == 2
assert solution("06") == 0
"""
    ),

    Task(
        id="t15",
        title="Merge Intervals",
        failure_category="hallucinated_constraint",
        description="Models assume input is pre-sorted and mutate the input list.",
        prompt="""Write a Python function called `solution(intervals)` where
`intervals` is a list of [start, end] pairs. Merge all overlapping intervals
and return the result sorted by start time.""",
        surface_tests="""
assert solution([[1,3],[2,6],[8,10],[15,18]]) == [[1,6],[8,10],[15,18]]
assert solution([[1,4],[4,5]]) == [[1,5]]
assert solution([]) == []
""",
        invariant_tests="""
assert solution([[2,6],[1,3],[8,10]]) == [[1,6],[8,10]]
assert solution([[1,2],[3,4]]) == [[1,2],[3,4]]
assert solution([[1,4],[2,3]]) == [[1,4]]
orig = [[1,3],[2,6]]
solution(orig)
assert orig == [[1,3],[2,6]], "Must not modify input"
assert solution([[1,5]]) == [[1,5]]
assert solution([[1,2],[3,4],[2,3]]) == [[1,4]]
"""
    ),

    Task(
        id="t16",
        title="Reverse Words in Sentence",
        failure_category="shortcut_solution",
        description="Models reverse characters within words or fail to collapse multiple spaces.",
        prompt="""Write a Python function called `solution(s)` that reverses
the order of words in a sentence. Strip leading/trailing spaces and reduce
multiple spaces between words to a single space.""",
        surface_tests="""
assert solution("the sky is blue") == "blue is sky the"
assert solution("  hello world  ") == "world hello"
assert solution("a good   example") == "example good a"
""",
        invariant_tests="""
assert solution("") == ""
assert solution("   ") == ""
assert solution("a") == "a"
assert solution("  hello  ") == "hello"
assert solution("Hello World") == "World Hello"
"""
    ),

    Task(
        id="t17",
        title="Power Function",
        failure_category="shortcut_solution",
        description="Models use repeated multiplication (O(n)) which times out on large exponents.",
        prompt="""Write a Python function called `solution(base, exp)` that
computes base raised to the power exp without using ** or pow().""",
        surface_tests="""
assert solution(2, 10) == 1024
assert solution(3, 0) == 1
assert solution(5, 1) == 5
""",
        invariant_tests="""
assert solution(0, 0) == 1
assert solution(0, 5) == 0
assert solution(1, 100) == 1
assert solution(-2, 3) == -8
assert solution(-2, 4) == 16
import time
t = time.time()
solution(2, 10**6)
assert time.time() - t < 1.0, "Too slow — must use fast exponentiation"
"""
    ),

    Task(
        id="t18",
        title="Spiral Matrix",
        failure_category="wrong_abstraction",
        description="Models miss edge cases for single-row, single-column, and non-square matrices.",
        prompt="""Write a Python function called `solution(matrix)` that returns
all elements of a 2D matrix in spiral order (clockwise from top-left).""",
        surface_tests="""
assert solution([[1,2,3],[4,5,6],[7,8,9]]) == [1,2,3,6,9,8,7,4,5]
assert solution([[1,2],[3,4]]) == [1,2,4,3]
assert solution([[1]]) == [1]
""",
        invariant_tests="""
assert solution([]) == []
assert solution([[1,2,3]]) == [1,2,3]
assert solution([[1],[2],[3]]) == [1,2,3]
m = [[1,2,3],[4,5,6],[7,8,9],[10,11,12]]
result = solution(m)
flat = [x for row in m for x in row]
assert sorted(result) == sorted(flat)
assert len(result) == 12
orig = [[1,2],[3,4]]
solution(orig)
assert orig == [[1,2],[3,4]], "Must not modify input"
"""
    ),

    Task(
        id="t19",
        title="Longest Increasing Subsequence",
        failure_category="wrong_abstraction",
        description="Models confuse non-decreasing with strictly increasing, or use O(n²) DP that times out.",
        prompt="""Write a Python function called `solution(nums)` that returns
the length of the longest strictly increasing subsequence.""",
        surface_tests="""
assert solution([10,9,2,5,3,7,101,18]) == 4
assert solution([0,1,0,3,2,3]) == 4
assert solution([7,7,7,7]) == 1
""",
        invariant_tests="""
assert solution([]) == 0
assert solution([1]) == 1
assert solution([1,2]) == 2
assert solution([2,1]) == 1
assert solution([1,1,1,1,2]) == 2
assert solution([1,2,3,4,5]) == 5
assert solution([5,4,3,2,1]) == 1
import time, random
big = random.sample(range(10**5), 10**4)
t = time.time()
solution(big)
assert time.time() - t < 2.0, "Too slow — O(n log n) expected"
"""
    ),

    Task(
        id="t20",
        title="Group Anagrams",
        failure_category="hallucinated_constraint",
        description="Models fail on empty strings, assume case-insensitive matching, or return wrong structure.",
        prompt="""Write a Python function called `solution(strs)` that groups
anagrams together. Return a list of groups. The order of groups and
the order within each group does not matter.""",
        surface_tests="""
result = solution(["eat","tea","tan","ate","nat","bat"])
assert len(result) == 3
assert sorted(["eat","tea","ate"]) in [sorted(g) for g in result]
assert sorted(["tan","nat"]) in [sorted(g) for g in result]
assert ["bat"] in [sorted(g) for g in result]
""",
        invariant_tests="""
assert solution([]) == []
result = solution(["a"])
assert len(result) == 1 and result[0] == ["a"]
result = solution(["abc", "def"])
assert len(result) == 2
result = solution(["abc","bca","cab"])
assert len(result) == 1 and sorted(result[0]) == ["abc","bca","cab"]
result = solution(["", ""])
assert len(result) == 1
result = solution(["Abc", "abc"])
assert len(result) == 2
"""
    ),
]
