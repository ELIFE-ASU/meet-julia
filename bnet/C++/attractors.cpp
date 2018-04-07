#include <chrono>
#include <cmath>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <iterator>
#include <numeric>
#include <stack>
#include <vector>

auto operator<<(std::ostream &out, std::vector<int> const& v) -> std::ostream&
{
    std::copy(std::begin(v), std::end(v), std::ostream_iterator<int>(out, " "));
    return out;
}

auto encode(std::vector<int> const &state)
{
    auto const N = std::size(state);
    auto code = 0ull;
    for (size_t i = 0; i < N; ++i)
    {
        code = 2*code + state.at(N - i - 1);
    }
    return code;
}

auto count_lines(char const *filename)
{
    auto number_of_lines = 0ull;
    std::string line;
    auto handle = std::ifstream{filename};
    while (std::getline(handle, line))
    {
        number_of_lines += 1;
    }
    return number_of_lines;
}

struct BNet
{
    size_t number_of_nodes;
    std::vector<std::vector<double>> weights;
    std::vector<double> thresholds;

    BNet(size_t n)
    {
        this->number_of_nodes = n;
        this->weights =
            std::vector<std::vector<double>>(n, std::vector<double>(n));
        this->thresholds = std::vector<double>(n);
    }

    BNet(BNet const&) = delete;
    BNet(BNet&&) = default;

    auto operator=(BNet const&) -> BNet& = delete;
    auto operator=(BNet&&) -> BNet& = default;

    auto size() const
    {
        return number_of_nodes;
    }

    auto volume() const
    {
        return static_cast<size_t>(1 << number_of_nodes);
    }

    static auto read(char const *wfile, char const *tfile)
    {
        auto number_of_nodes = count_lines(wfile);

        auto net = BNet{number_of_nodes};

        {
            auto handle = std::ifstream{wfile};
            for (auto &row : net.weights)
            {
                for (auto &weight : row)
                {
                    handle >> weight;
                }
            }
            handle.close();
        }

        {
            auto handle = std::ifstream{tfile};
            for (auto &threshold : net.thresholds)
            {
                handle >> threshold;
            }
            handle.close();
        }

        return net;
    }

    auto fire(std::vector<int> const &state, std::vector<int> &next_state) const
    {
        auto temp = std::vector<double>(std::size(state), 0.0);
        for (auto i = 0ull; i < std::size(state); ++i)
        {
            auto const &row = weights.at(i);
            temp.at(i) = std::inner_product(std::begin(row), std::end(row),
                    std::begin(state), 0.0);
        }
        for (auto i = 0ull; i < std::size(state); ++i)
        {
            if (temp.at(i) > thresholds.at(i))
            {
                next_state.at(i) = 1;
            }
            else if (temp.at(i) < thresholds.at(i))
            {
                next_state.at(i) = 0;
            }
            else
            {
                next_state.at(i) = state.at(i);
            }
        }

        return next_state;
    }

    auto fire(std::vector<int> const &state) const 
    {
        auto next_state = std::vector<int>(std::size(state));
        fire(state, next_state);
        return next_state;
    }

    auto transitions() const
    {
        auto const N = size();
        auto const V = volume();

        auto trans = std::vector<size_t>(V, -1);
        auto state = std::vector<int>(N, 0);
        auto next_state = fire(state);

        auto code = 0ull;
        auto next_code = encode(next_state);
        trans.at(code) = next_code;

        while (code < V - 1)
        {
            for (auto i = 0ull; i < N; ++i)
            {
                if (state.at(i) == 0)
                {
                    ++state.at(i);
                    for (auto j = 0ull; j < i; ++j)
                    {
                        state.at(j) = 0;
                    }
                    break;
                }
            }
            ++code;

            fire(state, next_state);
            next_code = encode(next_state);
            trans.at(code) = next_code;
        }

        return trans;
    }

    auto attractors() const
    {
        size_t const V = volume();

        auto const trans = transitions();

        auto seen = std::vector<bool>(V, false);
        auto basins = std::vector<int>(V, -1);
        auto basin_number = 0;

        auto attractors = std::vector<std::vector<int>>();
        auto state_stack = std::stack<std::size_t>();
        auto cycle = std::vector<int>();
        for (auto initial_state : trans)
        {
            if (seen.at(initial_state))
            {
                continue;
            }

            auto state = initial_state;
            auto in_cycle = false;
            auto next_state = trans.at(state);
            auto terminus = next_state;

            seen.at(state) = true;
            while (!seen.at(next_state))
            {
                state_stack.push(state);
                state = next_state;
                terminus = next_state = trans.at(state);
                seen.at(state) = true;
            }

            auto basin = basins.at(next_state);
            if (basins.at(next_state) == -1)
            {
                basin = basin_number;
                ++basin_number;
                cycle.push_back(state);
                in_cycle = (terminus != state);
            }

            basins.at(state) = basin;
            while (!state_stack.empty())
            {
                state = state_stack.top();
                state_stack.pop();

                basins.at(state) = basin;

                if (in_cycle)
                {
                    cycle.push_back(state);
                    in_cycle = (terminus != state);
                }
            }

            if (!cycle.empty())
            {
                attractors.push_back(cycle);
                cycle = std::vector<int>();
            }
        }

        return attractors;
    }
};

auto operator<<(std::ostream& out, BNet const& net) -> std::ostream&
{
    out << "number of nodes: " << std::size(net) << std::endl;
    out << "weights:" << std::endl;
    for (auto const &row : net.weights)
    {
        out << "  ";
        for (auto const &weight : row)
        {
            out << std::setw(2) << std::right;
            out << weight << '\t';
        }
        out << std::endl;
    }
    out << "thresholds:" << std::endl;
    for (auto const &threshold : net.thresholds)
    {
        out << std::setw(4) << std::setprecision(1) << std::right;
        out << threshold << '\t';
    }
    return out;
}

auto main(int argc, char **argv) -> int
{
    using namespace std::chrono;

    if (argc < 3)
    {
        std::cerr << "usage: attractors <weights> <thresholds>" << std::endl;
        return 1;
    }

    auto net = BNet::read(argv[1], argv[2]);

    auto start = steady_clock::now();
    auto attrs = net.attractors();
    auto stop = steady_clock::now();
    auto duration = 1e-9 * duration_cast<nanoseconds>(stop - start).count();
    std::cout << "First Invocation:  " << duration << "s\n" << std::endl;

    start = steady_clock::now();
    attrs = net.attractors();
    stop = steady_clock::now();
    duration = 1e-9 * duration_cast<nanoseconds>(stop - start).count();
    for (auto i = 0ull; i < std::size(attrs); ++i)
    {
        std::cout << "Attractor " << i << ": " << attrs.at(i) << std::endl;
    }
    std::cout << "Second Invocation: " << duration << "s" << std::endl;
}
