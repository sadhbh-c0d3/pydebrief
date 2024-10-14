
def interpolate(points, steps: int):
    """Linear interpolation

    Insert additional points inbetween existing points by using
    linear interpolation.
    """
    it = iter(points)
    prev = next(it)
    yield prev
    for cur in it:
        grad = 1.0 / float(steps + 1)
        ax = 1.0
        bx = 0.0
        for step in range(steps):
            ax -= grad
            bx += grad
            value = tuple(a*ax + b*bx for (a,b) in zip(prev, cur))
            yield value
        yield cur
        prev = cur
