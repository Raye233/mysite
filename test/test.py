from typing import List
from collections import Counter, defaultdict


class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        counter = Counter(nums)
        for i in range(len(nums)):
            diff = target - nums[i]
            if diff in counter:
                print(counter[diff])
                return [i, counter[diff]]


if __name__ == '__main__':
    s = Solution()
    nums = [2, 6, 7, 11, 15]
    target = 9
    print(s.twoSum(nums, target))
