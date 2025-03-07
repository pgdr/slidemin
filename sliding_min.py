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


if __name__ == "__main__":
    import sys

    k, *data = [int(x) for x in input().split()]
    print(" ".join(str(x) for x in slidemin(data, k)))
