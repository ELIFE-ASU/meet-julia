# -*- coding: utf-8 -*-
import numpy as np
import sys, time

def compute_pi(rng, trials):
    points = rng.rand(2,trials)
    inside = np.sum(np.sum(points**2, 0) <= 1.0)
    return (4.0 * inside) / trials

if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise RuntimeError("must provide number of trials")
    trials = int(sys.argv[1])

    rng = np.random.RandomState(2018)

    start = time.time()
    compute_pi(rng, trials)
    stop = time.time()
    print("First invocation:  {}s".format(stop-start))

    start = time.time()
    pi = compute_pi(rng, trials)
    stop = time.time()
    print("First invocation:  {}s".format(stop-start))

    print("π ≈ {}".format(pi))

