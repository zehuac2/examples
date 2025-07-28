from typing import List


def _longest_increasing_subsequence(values: List[int], i: int, j: int) -> int:
    """
    Helper function for longest increasing subsequence calculation.

    Args:
        values: List of integers
        i: Current index
        j: Next index to check

    Returns:
        Length of longest increasing subsequence
    """
    if j > len(values) - 1:
        return 0

    if values[i] >= values[j]:
        return _longest_increasing_subsequence(values, i, j + 1)

    return max(
        _longest_increasing_subsequence(values, i, j + 1),
        1 + _longest_increasing_subsequence(values, j, j + 1)
    )


def longest_increasing_subsequence_recursive(values: List[int]) -> int:
    """
    Calculate the longest increasing subsequence using recursive approach.

    Args:
        values: List of integers

    Returns:
        Length of the longest increasing subsequence
    """
    if len(values) < 2:
        return len(values)
    return _longest_increasing_subsequence(values, 0, 1)
