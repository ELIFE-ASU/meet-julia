import os, sys, time, numpy as np

def encode(state):
    code = 0
    for bit in state[::-1]:
        code = 2*code + bit
    return code

class BNet(object):
    def __init__(self, wfile, tfile):
        self.weights = np.loadtxt(wfile)
        self.thresholds = np.loadtxt(tfile)
        self.number_of_nodes = len(self.weights)

    def fire(self, state, next_state=None):
        if next_state is None:
            next_state = np.empty(state.shape, dtype=np.int)
        temp = np.dot(self.weights, state)
        for i in range(len(state)):
            if temp[i] > self.thresholds[i]:
                next_state[i] = 1
            elif temp[i] < self.thresholds[i]:
                next_state[i] = 0
            else:
                next_state[i] = state[i]
        return next_state

    def size(self):
        return self.number_of_nodes

    def volume(self):
        return (1 << self.size())

    def transitions(self):
        N, V = self.size(), self.volume()
        trans = np.empty(V, dtype=np.int)
        state = np.zeros(N, dtype=np.int)
        next_state = self.fire(state)

        code, next_code = 0, encode(next_state)
        trans[code] = next_code

        while code < V - 1:
            for i in range(N):
                if state[i] == 0:
                    state[i] += 1
                    state[0:i] = 0
                    break
            code += 1

            self.fire(state, next_state)
            next_code = encode(next_state)
            trans[code] = next_code

        return trans

    def attractors(self):
        V = self.volume()
        trans = self.transitions()
        seen = np.zeros(V, dtype=np.bool)
        basins = np.full(V, -1, dtype=np.int)
        basin_number = 0

        attractors = []
        state_stack = []
        cycle = []
        for initial_state in trans:
            if seen[initial_state]:
                continue

            state = initial_state
            in_cycle = False
            terminus = next_state = trans[state]
            seen[state] = True

            while not seen[next_state]:
                state_stack.append(state)
                state = next_state
                terminus = next_state = trans[state]
                seen[state] = True

            basin = basins[next_state]
            if basins[next_state] == -1:
                basin = basin_number
                basin_number += 1
                cycle.append(state)
                in_cycle = (terminus != state)

            basins[state] = basin
            while len(state_stack) != 0:
                state = state_stack.pop()
                basins[state] = basin
                if in_cycle:
                    cycle.append(state)
                    in_cycle = (terminus != state)

            if len(cycle) != 0:
                attractors.append(cycle)
                cycle = []

        return attractors

def main(wfile, tfile):
    net = BNet(wfile, tfile)

    start = time.time()
    attractors = net.attractors()
    stop = time.time()
    print('First Invocation:  {}s\n'.format(stop - start))

    start = time.time()
    attractors = net.attractors()
    stop = time.time()
    for (i, attractor) in enumerate(attractors):
        sys.stdout.write('Attractor {}: '.format(i))
        for state in attractor:
            sys.stdout.write('{} '.format(state))
        sys.stdout.write('\n')
    print('Second Invocation: {}s\n'.format(stop - start))

if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.stderr.write('error: python attractors.py <weights> <thresholds>\n')
        os.exit(1)

    main(sys.argv[1], sys.argv[2])
