struct BNet
    number_of_nodes::Int
    weights::Array{Float64,2}
    thresholds::Vector{Float64}
    BNet(ws, ts) = new(size(ws,1), ws, ts)
end

load(::Type{BNet}, wfile, tfile) = BNet(readdlm(wfile), vec(readdlm(tfile)))

Base.size(net) = net.number_of_nodes

volume(net) = 1 << size(net)

function fire!(net, state, next_state)
    temp = net.weights * state
    for i in 1:length(state)
        next_state[i] = if temp[i] > net.thresholds[i]
            1
        elseif temp[i] < net.thresholds[i]
            0
        else
            state[i]
        end
    end
    next_state
end

fire(net, state) = fire!(net, state, similar(state))

function encode(state)
    const N = length(state)
    code = 0
    for i in 1:N
        code = 2code + state[N - i + 1]
    end
    code + 1
end

function transitions(net)
    const N, V = size(net), volume(net)
    trans = Array{Int}(V)
    state = zeros(Int, N)
    next_state = fire(net, state)

    code, next_code = 1, encode(next_state)
    trans[code] = next_code

    while code < V
        for i in 1:N
            if state[i] == 0
                state[i] += 1
                state[1:i-1] = 0
                break
            end
        end
        code += 1

        fire!(net, state, next_state)
        next_code = encode(next_state)
        trans[code] = next_code
    end

    trans
end

function attractors(net)
    const V = volume(net)
    const trans = transitions(net)
    seen = zeros(Bool, V)
    basins = fill(-1, V)
    basin_number = 0

    attractors = Vector{Int}[]
    state_stack = Int[]
    cycle = Int[]
    for initial_state in trans
        if seen[initial_state]
            continue
        end

        state = initial_state
        in_cycle = false
        terminus = next_state = trans[state]
        seen[state] = true

        while !seen[next_state]
            push!(state_stack, state)
            state = next_state
            terminus = next_state = trans[state]
            seen[state] = true
        end

        basin = basins[next_state]
        if basins[next_state] == -1
            basin = basin_number
            basin_number += 1
            push!(cycle, state)
            in_cycle = (terminus != state)
        end

        basins[state] = basin
        while !isempty(state_stack)
            state = pop!(state_stack)
            basins[state] = basin
            if in_cycle
                push!(cycle, state)
                in_cycle = (terminus != state)
            end
        end

        if !isempty(cycle)
            push!(attractors, cycle)
            cycle = Int[]
        end
    end
    attractors
end

function main(wfile, tfile)
    const net = load(BNet, wfile, tfile)

    duration = @elapsed begin
        attrs = attractors(net)
    end
    println("First Invocation:  $(duration)s\n")
    
    duration = @elapsed begin
        attrs = attractors(net)
    end
    w = ceil(log2(length(attrs)))
    for (i, attr) in enumerate(attrs)
        print("Attractor $i: ")
        for state in attr
            print("$(state-1) ")
        end
        println()
    end
    println("Second Invocation: $(duration)s")
end

main(ARGS[1], ARGS[2])
