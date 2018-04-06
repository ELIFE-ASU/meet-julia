import json, sys, time
from math import sqrt

class Body(object):
    def __init__(self, name, mass, position, velocity):
        self.name = name
        self.mass = mass
        self.x, self.y, self.z = position
        self.vx, self.vy, self.vz = velocity

def read_bodies(filename):
    bodies = []
    with open(filename, 'r') as handle:
        data = json.load(handle)
        if 'unitmass' in data:
            unitmass = data['unitmass']
        else:
            unitmass = 1.0

        for key, value in data.items():
            if key != 'unitmass':
                body = Body(key, unitmass * value['mass'],
                            value['position'], value['velocity'])
                bodies.append(body)
    return bodies

def kinetic_energy(body):
    return 0.5 * body.mass * (body.vx**2 + body.vy**2 + body.vz**2)

def potential_energy(a, b):
    dx = a.x - b.x
    dy = a.y - b.y
    dz = a.z - b.z
    return -a.mass * b.mass / sqrt(dx**2 + dy**2 + dz**2)

def energy(bodies):
    E = 0.0
    for i in range(len(bodies)):
        E += kinetic_energy(bodies[i])
        for j in range(i+1, len(bodies)):
            E += potential_energy(bodies[i], bodies[j])
    return E

def advance(bodies, dt):
    for i in range(len(bodies)):
        a = bodies[i]
        for j in range(i+1, len(bodies)):
            b = bodies[j]

            dx = a.x - b.x
            dy = a.y - b.y
            dz = a.z - b.z
            d2 = dx**2 + dy**2 + dz**2
            ds = sqrt(d2)
            magnitude = dt / (d2 * d2)
            magnitude *= ds

            a.vx -= b.mass * magnitude * dx
            a.vy -= b.mass * magnitude * dy
            a.vz -= b.mass * magnitude * dz

            b.vx += a.mass * magnitude * dx
            b.vy += a.mass * magnitude * dy
            b.vz += a.mass * magnitude * dz

    for b in bodies:
        b.x += dt * b.vx
        b.y += dt * b.vy
        b.z += dt * b.vz

def main(filename, timesteps):
    bodies = read_bodies(filename)

    for body in bodies:
        print(body)

    print('Initial Energy: {:.9f}'.format(energy(bodies)))
    start = time.time()
    for i in range(timesteps):
        advance(bodies, 0.01)
    stop = time.time()
    print('Final Energy:   {:.9f}'.format(energy(bodies)))
    print('Elapsed: {}s\n'.format(stop-start))

if __name__ == '__main__':
    if len(sys.argv) < 3:
        raise RuntimeError('usage: python nbody.py <json-file> <time-steps>')
    
    filename = sys.argv[1]
    timesteps = int(sys.argv[2])

    main(filename, timesteps)
