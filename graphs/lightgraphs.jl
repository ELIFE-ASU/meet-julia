using LightGraphs

function betweenness_centrality(c::Int, n::Int, k::Int)
    bc, elapsed = 0.0, 0.0
    for i in 1:c
        graph = barabasi_albert(n, k)
        elapsed += @elapsed begin
            bc += mean(LightGraphs.betweenness_centrality(graph))
            #  bc += mean(parallelbetweenness_centrality(graph))
        end
    end
    bc /= c
    elapsed /= c
    println("Betweenness Centrality:  $bc ($(elapsed)s/call)")
end

function clustering_coefficient(c::Int, n::Int, k::Int)
    cc, elapsed = 0.0, 0.0
    for i in 1:c
        graph = barabasi_albert(n, k)
        elapsed += @elapsed begin
            cc += mean(local_clustering_coefficient(graph))
        end
    end
    cc /= c
    elapsed /= c
    println("Average Clustering Coefficient:  $cc ($(elapsed)s/call)")
end

function main()
    n = parse(Int, ARGS[1])
    k = parse(Int, ARGS[2])
    if length(ARGS) >= 3
        srand(parse(Int, ARGS[3]))
    end

    betweenness_centrality(5, n, k)
    clustering_coefficient(10, n, k)
end

main()
