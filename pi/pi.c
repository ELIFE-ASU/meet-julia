#include <stdio.h>
#include <stdlib.h>
#include <time.h>

double random_double()
{
    return (double) rand() / RAND_MAX;
}

double estimate_pi(int const trials)
{
    int inside = 0;
    for (int i = 0; i < trials; ++i)
    {
        double const x = random_double();
        double const y = random_double();
        inside += (x*x + y*y <= 1.0);
    }
    return 4.0 * inside / trials;
}

int main(int argc, char **argv)
{
    if (argc < 2)
    {
        fprintf(stderr, "ERROR: must provide number of trials\n");
        return 1;
    }

    int const trials = atoi(argv[1]);
    srand(2018);

    clock_t start = clock();
    estimate_pi(trials);
    clock_t stop = clock();
    printf("First Invocation:  %lfs\n", ((double)(stop - start))/CLOCKS_PER_SEC);

    start = clock();
    double pi = estimate_pi(trials);
    stop = clock();
    printf("Second Invocation: %lfs\n", ((double)(stop - start))/CLOCKS_PER_SEC);

    printf("π ≈ %lf\n", pi);
}
