from collections import deque


def slidemin(data, k):
    """Linear time algorithm for computing sliding window minimum values."""
    minq = deque()
    for i in range(len(data)):
        if minq and minq[0] == i - k:
            minq.popleft()
        while minq and data[minq[-1]] >= data[i]:
            minq.pop()
        minq.append(i)
        if i >= k - 1:
            yield data[minq[0]]


print(list(slidemin([9, 3, 3, 5, 6, 2, 4, 5, 6], 3)))
