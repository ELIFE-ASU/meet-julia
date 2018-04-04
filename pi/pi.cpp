#include <chrono>
#include <iostream>
#include <random>
#include <stdexcept>

template <typename RNG>
auto compute_pi(RNG &rng, int const trials) -> double
{
    auto static dist = std::uniform_real_distribution<double>(0.0, 1.0);
    auto inside = 0;
    for (auto i = 0; i < trials; ++i)
    {
        auto const x = dist(rng);
        auto const y = dist(rng);
        inside += (x*x + y*y <= 1.0);
    }
    return 4.0 * inside / trials;
}

auto main(int argc, char **argv) -> int
{
    using namespace std::chrono;
    if (argc < 2)
    {
        std::cerr << "must provide number of trials" << std::endl;
        return 1;
    }

    auto const trials = std::stoi(argv[1]);
    std::mt19937 rng(2018); 

    auto start = steady_clock::now();
    compute_pi(rng, trials);
    auto stop = steady_clock::now();
    auto duration = 1e-9*duration_cast<nanoseconds>(stop - start).count();
    std::cout << "First invocation:  " << duration << "s" << std::endl;

    start = steady_clock::now();
    auto pi = compute_pi(rng, trials);
    stop = steady_clock::now();
    duration = 1e-9*duration_cast<nanoseconds>(stop - start).count();
    std::cout << "Second invocation: " << duration << "s" << std::endl;

    std::cout << "π ≈ " << pi << std::endl;
}
