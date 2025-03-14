# Sliding window for minimum

Computing the minimum values of a sliding window is not as easy as
computing, e.g., the sum. When computing the sum, we simply need a
single accumulated variable
`acc = acc - data[win] + data[win + k]`.

However, when we want to compute the minimum value, we need to know
which next minimum value to keep when a small value disappears out of
the window. Recomputing this value every iteration is more expensive
than necessary; It would take $\Omega(n \cdot k)$, where $n$ is the
number of elements and $k$ the size of the window. There is, however, a
way of computing all min-values in $O(n)$ *amortized* time (left as an
exercise to the student).

The trick is to use a *double-ended queue*. In this queue, we keep a
(necessarily increasing) list of potential minimum values. To understand
the algorithm, consider the following list:
`data = [10, 5, 3, 5, 7, 4, 2]`, with $k = 3$.

Let `Q = []` be an empty double-ended queue [^1] , and let us
start reading values from `data`. First we read 10, which we
will put into the queue. Second, we read 5. Notice that 10 is now not
relevant anymore, since 10 will never be the minimum value. We will pop
*from the right* until the queue is empty, or until the right-most value
is higher than what we are currently looking at. The queue, after having
read $10, 5$ is `Q = [5]`.

We still haven't read $k=3$ values yet, so we read another one, and see
3. Again, we have that $5$ is not relevant, so we remove it from the
queue. After having read $10, 5, 3$, we have `Q = [3]`.

Since we have seen $k=3$ values, we can output $3$. The window is now at
$$[\underbracket[0.1pt][0.1pt]{ 10, 5, 3}, 5, 7, 4, 2].$$ At this point,
we are ready to move the window one step to the right, i.e., we want to
discard 10 and introduce 5. Since the left-most value in `data`
is 10, and 10 is not in the queue, we do not pop anything from the
queue. However, the value we include in the window might at some point
in the future become the minimum value (after 3 has been discarded some
time in the future), so we include 5 in the queue.

At $[10, \underbracket[0.1pt][0.1pt]{ 5, 3, 5 }, 7, 4, 2]$ with
`Q = [3, 5]`, we again output the minimum value; it is the
first value in the queue. Moving the window one step to the right means
we discard a value 5. However, the leftmost value in the queue is 3,
which means that the value we discard is irrelevant. On the right hand
side, we include 7. This might in the future become the minimum value,
so we need to include it in the queue.

The state is now $[10, 5, \underbracket[0.1pt][0.1pt]{ 3, 5, 7}, 4, 2]$
with `Q = [3, 5, 7]`, and we again output a value: the leftmost
value in the queue, 3. Thus far, our output has been
`output = [3, 3, 3]`.

Finally, something interesting happens, we are ready to discard the
value 3. Moving the window one step to the right means we discard a
value that is the leftmost value in the queue, which means we need to
pop it off. The queue is then `Q = [5, 7]`, but we also need to
include the new value, which happens to be 4.

When the queue is `Q = [5, 7]`, and the new value is 4, we can
notice that neither 5 nor 7 will ever be the minimum value, because (a)
4 is smaller than them both and (b) 4 will outlive them. The procedure
is to look at the rightmost value, and since $7 > 4$, we pop off 7, and
repeat. The rightmost value is $5 > 4$ and we will pop off 5, and we are
left with an empty queue, and therefore the state is:

$$[10, 5 ,3, \underbracket[0.1pt][0.1pt]{ 5, 7, 4 },  2],$$ with
`Q = [4]` and we output the leftmost value in the queue: 4.

The final state is
$[10, 5 ,3 ,5, \underbracket[0.1pt][0.1pt]{ 7, 4 , 2 }]$, with
`Q = [2]` at which point we output 2. The total output is
`output = [3, 3, 3, 4, 2]`.

# Code

``` python
def slidemin(data, k):
    """Linear time algorithm for computing sliding
       window minimum values."""
    minq = deque()              # from collections
    for i in range(len(data)):
        if minq and minq[0] == i - k:
            minq.popleft()
        while minq and data[minq[-1]] >= data[i]:
            minq.pop()
        minq.append(i)
        if i >= k - 1:
            yield data[minq[0]]
```

[^1]: A double-ended queue is one we can read and write, push and pop,
    from both left and right side in $O(1)$ time.
