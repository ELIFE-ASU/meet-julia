# -*- coding: utf-8 -*-
import random, sys, time

def compute_pi(trials):
    inside = 0.0
    for _ in range(trials):
        x, y = random.random(), random.random()
        inside += float(x*x + y*y <= 1.0)
    return 4.0 * inside / trials

if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise RuntimeError("must provide number of trials")

    trials = int(sys.argv[1])

    random.seed(2018)

    start = time.time()
    compute_pi(trials)
    stop = time.time()
    print("First invocation:  {}s".format(stop-start))

    start = time.time()
    pi = compute_pi(trials)
    stop = time.time()
    print("First invocation:  {}s".format(stop-start))

    print("π ≈ {}".format(pi))

