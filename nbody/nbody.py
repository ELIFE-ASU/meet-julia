import json, sys, time
from math import sqrt
import numpy as np
import weave

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

def numpy_positions_get(bodies):
    x,y,z = [],[],[]
    for b in bodies:
        x.append(b.x)
        y.append(b.y)
        z.append(b.z)
    return np.array([x,y,z])

def numpy_velocities_get(bodies):
    vx,vy,vz = [],[],[]
    for b in bodies:
        vx.append(b.vx)
        vy.append(b.vy)
        vz.append(b.vz)
    return np.array([vx,vy,vz])

def numpy_masses_get(bodies):
    m = []
    for b in bodies:
        m.append(b.mass)
    return np.array([m,m,m])

def numpy_positions_set(positions,bodies):
    x,y,z = positions
    for i in range(len(bodies)):
        b = bodies[i]
        b.x = x[i]
        b.y = y[i]
        b.z = z[i]

def numpy_velocities_set(velocities,bodies):
    vx,vy,vz = velocities
    for i in range(len(bodies)):
        b = bodies[i]
        b.vx = vx[i]
        b.vy = vy[i]
        b.vz = vz[i]

def advance_numpy(bodies, dt, n):
    
    positions = numpy_positions_get(bodies)
    velocities = numpy_velocities_get(bodies)
    masses = numpy_masses_get(bodies)
    
    # *_repeat has shape (len(bodies),len(bodies),3)
    positions_repeat = np.tile(positions.transpose(),[len(bodies),1,1])
    velocities_repeat = np.tile(velocities.transpose(),[len(bodies),1,1])
    masses_repeat = np.tile(masses.transpose(),[len(bodies),1,1])
    
    for i in range(n):
        delta_positions = positions_repeat - positions_repeat.transpose((1,0,2))
        d2 = np.sum( delta_positions*delta_positions, axis=-1 )
        ds = np.sqrt(d2)
        magnitude = ds * np.nan_to_num( dt / (d2 * d2) )
        magnitude_repeat = np.tile(magnitude,[3,1,1]).transpose((1,2,0))
        velocities -= np.sum(masses_repeat.transpose((1,0,2)) * magnitude_repeat * delta_positions,axis=0).transpose()
        positions += dt * velocities
        positions_repeat = np.tile(positions.transpose(),[len(bodies),1,1])
    
    #return positions,velocities
    
    numpy_positions_set(positions,bodies)
    numpy_velocities_set(velocities,bodies)

def advance_weave(bodies, dt, n):

    positions = numpy_positions_get(bodies)
    velocities = numpy_velocities_get(bodies)
    masses = numpy_masses_get(bodies)[0]

    nb = len(bodies)

    code = """
    float dx,dy,dz,d2,ds,magnitude;
    
    for (int i=0; i<n; i++){
    
        for (int bodyi=0; bodyi<nb; bodyi++){
            for (int bodyj=bodyi+1; bodyj<nb; bodyj++){
                
                dx = positions(0,bodyi) - positions(0,bodyj);
                dy = positions(1,bodyi) - positions(1,bodyj);
                dz = positions(2,bodyi) - positions(2,bodyj);
                d2 = dx*dx + dy*dy + dz*dz;
                ds = sqrt(d2);
                magnitude = dt / (d2 * d2);
                magnitude *= ds;
                
                velocities(0,bodyi) -= masses(bodyj) * magnitude * dx;
                velocities(1,bodyi) -= masses(bodyj) * magnitude * dy;
                velocities(2,bodyi) -= masses(bodyj) * magnitude * dz;
                
                velocities(0,bodyj) += masses(bodyi) * magnitude * dx;
                velocities(1,bodyj) += masses(bodyi) * magnitude * dy;
                velocities(2,bodyj) += masses(bodyi) * magnitude * dz;
            }
        }
        
        for (int bodyk=0; bodyk<nb; bodyk++){
            for (int dimi=0; dimi<3; dimi++){
                positions(dimi,bodyk) += dt * velocities(dimi,bodyk);
            }
        }
        
    }
    """

    err = weave.inline(code,
        ['n','nb','positions','velocities','masses','dt'],
        type_converters = weave.converters.blitz)

    numpy_positions_set(positions,bodies)
    numpy_velocities_set(velocities,bodies)


def main(filename, timesteps):
    bodies = read_bodies(filename)

    for body in bodies:
        print(body)

    print('Initial Energy: {:.9f}'.format(energy(bodies)))
    start = time.time()
    if False:
        for i in range(timesteps):
            advance(bodies, 0.01)
    elif False:
        advance_numpy(bodies, 0.01, timesteps)
    else:
        advance_weave(bodies, 0.01, timesteps)
    stop = time.time()
    print('Final Energy:   {:.9f}'.format(energy(bodies)))
    print('Elapsed: {}s\n'.format(stop-start))

if __name__ == '__main__':
    if len(sys.argv) < 3:
        raise RuntimeError('usage: python nbody.py <json-file> <time-steps>')
    
    filename = sys.argv[1]
    timesteps = int(sys.argv[2])

    main(filename, timesteps)
