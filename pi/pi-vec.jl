function compute_π(rng, trials)
    points = rand(rng, 2, trials)
    inside = sum(sum(points.^2,1) .<= 1.0)
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
