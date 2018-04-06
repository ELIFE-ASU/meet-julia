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
                body = Body(key, unitmass * value["mass"],
                            value["position"]..., value["velocity"]...)
                push!(bodies, body)
            end
        end
    end
    bodies
end

function offset_momentum!(bodies)
    px, py, pz = 0.0, 0.0, 0.0
    for b in bodies
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
    for i in 1:length(bodies)
        a = bodies[i]
        for j in (i+1):length(bodies)
            b = bodies[j]

            dx = a.x - b.x
            dy = a.y - b.y
            dz = a.z - b.z
            d2 = dx^2 + dy^2 + dz^2
            ds = sqrt(d2)
            magnitude = dt / (d2*d2)
            magnitude *= ds

            a.vx -= b.mass * magnitude * dx
            a.vy -= b.mass * magnitude * dy
            a.vz -= b.mass * magnitude * dz

            b.vx += a.mass * magnitude * dx
            b.vy += a.mass * magnitude * dy
            b.vz += a.mass * magnitude * dz
        end
    end

    for b in bodies
        b.x += dt * b.vx
        b.y += dt * b.vy
        b.z += dt * b.vz
    end
end

function main(filename, time_steps)
    bodies = read_bodies(filename)

    offset_momentum!(bodies)
    for body in bodies
        println(body)
    end

    @printf "Initial Energy: %.9f\n" energy(bodies)
    duration = @elapsed for _ in 1:time_steps
        advance!(bodies, 0.01)
    end
    @printf "Final Energy:   %.9f\n" energy(bodies)
    @printf "Elapsed: %fs\n\n" duration
end

if length(ARGS) < 2
    error("usage: julia nbody.jl <json-file> <time-steps>")
end

const filename = ARGS[1]
const time_steps = parse(Int, ARGS[2])

main(filename, time_steps)
