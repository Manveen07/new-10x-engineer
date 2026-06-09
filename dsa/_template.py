"""LeetCode #1 — Two Sum (Easy)

Pattern: hash map — single pass, complement lookup.
Time: O(n)  Space: O(n)
Solved: YYYY-MM-DD, no AI, ~XX min
"""


class Solution:
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        seen: dict[int, int] = {}
        for i, n in enumerate(nums):
            if target - n in seen:
                return [seen[target - n], i]
            seen[n] = i
        return []


if __name__ == "__main__":
    s = Solution()
    assert s.twoSum([2, 7, 11, 15], 9) == [0, 1]
    assert s.twoSum([3, 2, 4], 6) == [1, 2]
    print("ok")
