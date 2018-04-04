function compute_π(rng, trials)
    inside = 0.0
    for _ in 1:trials
        x, y = rand(rng), rand(rng)
        inside += (x^2 + y^2 <= 1.0)
    end
    4inside/trials
end

if isempty(ARGS)
    error("must provide number of trials")
end

trials = parse(Int, ARGS[1])

rng = MersenneTwister(2018)

@time compute_π(rng, trials)
@time π = compute_π(rng, trials)

println("π ≈ $π")
