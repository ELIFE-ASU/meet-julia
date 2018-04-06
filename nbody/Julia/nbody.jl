using JSON

mutable struct Body
    name::String
    mass::Float64
    x::Float64
    y::Float64
    z::Float64
    vx::Float64
    vy::Float64
    vz::Float64
    Body() = new("", 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
end

function read_bodies(filename)
    bodies = Body[]
    open(filename, "r") do handle
        json = JSON.parse(handle)
        unitmass = if haskey(json, "unitmass")
            json["unitmass"]
        else
            1.0
        end
        for (key, value) in json
            if key != "unitmass"
                body = Body()
                body.name = key
                body.mass = unitmass * value["mass"]
                body.x, body.y, body.z = value["position"]
                body.vx, body.vy, body.vz = value["velocity"]
                push!(bodies, body)
            end
        end
    end
    bodies
end

function offset_momentum!(bodies)
    px, py, pz = 0.0, 0.0, 0.0
    for i in 1:length(bodies)
        b = bodies[i]
        px += b.mass * b.vx
        py += b.mass * b.vy
        pz += b.mass * b.vz
    end
    sun_index = findfirst(b -> b.name == "Sun", bodies)
    if sun_index != length(bodies)
        b = bodies[sun_index]
        b.vx = -px / b.mass
        b.vy = -py / b.mass
        b.vz = -pz / b.mass
    end
end

function energy(bodies)
    E = 0.0
    for i in 1:length(bodies)
        E += kinetic_energy(bodies[i])
        for j in (i+1):length(bodies)
            E += potential_energy(bodies[i], bodies[j])
        end
    end
    E
end

kinetic_energy(body) = 0.5 * body.mass * (body.vx^2 + body.vy^2 + body.vz^2)

function potential_energy(a, b)
    dx = a.x - b.x
    dy = a.y - b.y
    dz = a.z - b.z
    -a.mass * b.mass / sqrt(dx^2 + dy^2 + dz^2)
end

function advance!(bodies, dt)
    const N = length(bodies)
    for i in 1:N
        for j in (i+1):N
            dx = bodies[i].x - bodies[j].x
            dy = bodies[i].y - bodies[j].y
            dz = bodies[i].z - bodies[j].z
            d2 = dx^2 + dy^2 + dz^2
            ds = sqrt(d2)
            magnitude = dt / (d2*d2)
            magnitude *= ds

            bodies[i].vx -= bodies[j].mass * magnitude * dx
            bodies[i].vy -= bodies[j].mass * magnitude * dy
            bodies[i].vz -= bodies[j].mass * magnitude * dz

            bodies[j].vx += bodies[i].mass * magnitude * dx
            bodies[j].vy += bodies[i].mass * magnitude * dy
            bodies[j].vz += bodies[i].mass * magnitude * dz
        end
    end

    for i in 1:N
        bodies[i].x += dt * bodies[i].vx
        bodies[i].y += dt * bodies[i].vy
        bodies[i].z += dt * bodies[i].vz
    end
end

function main(filename, time_steps)
    bodies = read_bodies(filename)

    offset_momentum!(bodies)

    @printf "Initial Energy: %.9f\n" energy(bodies)
    duration = @elapsed for _ in 1:time_steps
        advance!(bodies, 0.01)
    end
    @printf "Final Energy:   %.9f\n" energy(bodies)
    @printf "Elapsed: %fs\n\n" duration

    @printf "Initial Energy: %.9f\n" energy(bodies)
    duration = @elapsed for _ in 1:time_steps
        advance!(bodies, 0.01)
    end
    @printf "Final Energy:   %.9f\n" energy(bodies)
    @printf "Elapsed: %fs\n" duration
end

if length(ARGS) < 2
    error("usage: julia nbody.jl <json-file> <time-steps>")
end

const filename = ARGS[1]
const time_steps = parse(Int, ARGS[2])

main(filename, time_steps)
