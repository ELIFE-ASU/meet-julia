#include <json/json.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

char *strdup(char const *str)
{
    char *dst = malloc(strlen(str)+1);
    strcpy(dst, str);
    return dst;
}

typedef struct body
{
    char *name;
    double mass;
    double x, y, z;
    double vx, vy, vz;
} body;

void body_free(body *b)
{
    if (b)
    {
        free(b->name);
    }
}

int set_mass(body *b, struct json_object *json)
{
    if (json_object_is_type(json, json_type_double))
    {
        b->mass = json_object_get_double(json);
        return 0;
    }
    else
    {
        fprintf(stderr, "error: mass must be a double\n");
        return 1;
    }
}

int set_position(body *b, struct json_object *json)
{
    if (json_object_is_type(json, json_type_array))
    {
        struct json_object *position = json_object_array_get_idx(json, 0);
        if (position)
        {
            if (json_object_is_type(position, json_type_double))
            {
                b->x = json_object_get_double(position);
            }
            else
            {
                fprintf(stderr, "error: x position must be a double\n");
                return 1;
            }
        }
        else
        {
            fprintf(stderr, "error: too few positions provided\n");
            return 1;
        }

        position = json_object_array_get_idx(json, 1);
        if (position)
        {
            if (json_object_is_type(position, json_type_double))
            {
                b->y = json_object_get_double(position);
            }
            else
            {
                fprintf(stderr, "error: y position must be a double\n");
                return 1;
            }
        }
        else
        {
            fprintf(stderr, "error: too few positions provided\n");
            return 1;
        }

        position = json_object_array_get_idx(json, 2);
        if (position)
        {
            if (json_object_is_type(position, json_type_double))
            {
                b->z = json_object_get_double(position);
            }
            else
            {
                fprintf(stderr, "error: y position must be a double\n");
                return 1;
            }
        }
        else
        {
            fprintf(stderr, "error: too few positions provided\n");
            return 1;
        }

        position = json_object_array_get_idx(json, 3);
        if (position)
        {
            fprintf(stderr, "error: too many positions provided\n");
            return 1;
        }

        return 0;
    }
    else
    {
        fprintf(stderr, "error: position must be an array\n");
        return 1;
    }
}

int set_velocity(body *b, struct json_object *json)
{
    if (json_object_is_type(json, json_type_array))
    {
        struct json_object *velocity = json_object_array_get_idx(json, 0);
        if (velocity)
        {
            if (json_object_is_type(velocity, json_type_double))
            {
                b->vx = json_object_get_double(velocity);
            }
            else
            {
                fprintf(stderr, "error: x velocity must be a double\n");
                return 1;
            }
        }
        else
        {
            fprintf(stderr, "error: too few velocities provided\n");
            return 1;
        }

        velocity = json_object_array_get_idx(json, 1);
        if (velocity)
        {
            if (json_object_is_type(velocity, json_type_double))
            {
                b->vy = json_object_get_double(velocity);
            }
            else
            {
                fprintf(stderr, "error: y velocity must be a double\n");
                return 1;
            }
        }
        else
        {
            fprintf(stderr, "error: too few velocities provided\n");
            return 1;
        }

        velocity = json_object_array_get_idx(json, 2);
        if (velocity)
        {
            if (json_object_is_type(velocity, json_type_double))
            {
                b->vz = json_object_get_double(velocity);
            }
            else
            {
                fprintf(stderr, "error: y velocity must be a double\n");
                return 1;
            }
        }
        else
        {
            fprintf(stderr, "error: too few velocities provided\n");
            return 1;
        }

        velocity = json_object_array_get_idx(json, 3);
        if (velocity)
        {
            fprintf(stderr, "error: too many velocities provided\n");
            return 1;
        }

        return 0;
    }
    else
    {
        fprintf(stderr, "error: velocity must be an array\n");
        return 1;
    }
}

int add_body(body *b, char const *name, struct json_object *json)
{
    int ret = 0;
    b->name = strdup(name);
    int mass_seen = 0, position_seen, velocity_seen = 0;
    json_object_object_foreach(json, key, value) {
        if (strcmp(key, "mass") == 0)
        {
            mass_seen = 1;
            if (set_mass(b, value))
            {
                ret = -1;
            }
        }
        else if (strcmp(key, "position") == 0)
        {
            position_seen = 1;
            if (set_position(b, value))
            {
                ret = -2;
            }
        }
        else if (strcmp(key, "velocity") == 0)
        {
            velocity_seen = 1;
            if (set_velocity(b, value))
            {
                ret = -3;
            }
        }
        else
        {
            fprintf(stderr, "error: unrecognized key (%s) in body (%s)\n",
                    key, name);
            ret = -4;
        }
    }
    if (!mass_seen)
    {
        fprintf(stderr, "error: no mass provided for body (%s)\n", name);
        ret = 1;
    }
    if (!position_seen)
    {
        fprintf(stderr, "error: no position provided for body (%s)\n", name);
        ret = 2;
    }
    if (!velocity_seen)
    {
        fprintf(stderr, "error: no velocity provided for body (%s)\n", name);
        ret = 3;
    }
    return ret;
}

size_t read_bodies(char const *filename, body **b)
{
    struct json_object *json = json_object_from_file(filename);
    if (!json)
    {
        return -1;
    }

    int number_of_bodies = json_object_object_length(json);

    double unitmass = 1.0;
    json_object_object_foreach(json, key, value)
    {
        if (strcmp(key, "unitmass") == 0)
        {
            number_of_bodies -= 1;
            if (json_object_is_type(value, json_type_double))
            {
                unitmass = json_object_get_double(value);
            }
            else
            {
                fprintf(stderr, "unitmass must be a double\n");
                return -1;
            }
        }
    }

    body *bodies = calloc(number_of_bodies, sizeof(body));
    if (bodies)
    {
        size_t index = 0;
        json_object_object_foreach(json, key, value)
        {
            if (strcmp(key, "unitmass") != 0)
            {
                if (add_body(bodies + index, key, value))
                {
                    free(*b);
                    *b = NULL;
                    break;
                }
                bodies[index].mass *= unitmass;
                index += 1;
            }
        }
        *b = bodies;
    }

    json_object_put(json);

    return number_of_bodies;
}

inline static double kinetic_energy(body const *b)
{
    double const vx = b->vx;
    double const vy = b->vy;
    double const vz = b->vz;
    return 0.5 * b->mass * (vx*vx + vy*vy + vz*vz);
}

inline static double potential_energy(body const *a, body const *b)
{
    double const dx = a->x - b->x;
    double const dy = a->y - b->y;
    double const dz = a->z - b->z;
    return -a->mass * b->mass / sqrt(dx*dx + dy*dy + dz*dz);
}

inline static double energy(body const *bodies, size_t number_of_bodies)
{
    double e = 0.0;

    for (size_t i = 0; i < number_of_bodies; ++i)
    {
        e += kinetic_energy(bodies + i);
        for (size_t j = i + 1; j < number_of_bodies; ++j)
        {
            e += potential_energy(bodies + i, bodies + j);
        }
    }

    return e;
}

inline static void offset_momentum(body *bodies, size_t number_of_bodies)
{
    double px = 0.0, py = 0.0, pz = 0.0;
    for (body const *b = bodies; b != bodies + number_of_bodies; ++b)
    {
        px += b->vx * b->mass;
        py += b->vy * b->mass;
        pz += b->vz * b->mass;
    }
    bodies[0].vx = -px / bodies[0].mass;
    bodies[0].vy = -py / bodies[0].mass;
    bodies[0].vz = -pz / bodies[0].mass;
}

inline static void advance(body *bodies, size_t number_of_bodies, double dt)
{
    for (size_t i = 0; i < number_of_bodies; ++i)
    {
        body *a = bodies + i;
        for (size_t j = i + 1; j < number_of_bodies; ++j)
        {
            body *b = bodies + j;

            double const dx = a->x - b->x;
            double const dy = a->y - b->y;
            double const dz = a->z - b->z;

            double const r = sqrt(dx*dx + dy*dy + dz*dz);

            double const magnitude = dt / (r * r * r);

            a->vx -= dx * b->mass * magnitude;
            a->vy -= dy * b->mass * magnitude;
            a->vz -= dz * b->mass * magnitude;

            b->vx += dx * a->mass * magnitude;
            b->vy += dy * a->mass * magnitude;
            b->vz += dz * a->mass * magnitude;
        }
    }

    for (size_t i = 0; i < number_of_bodies; ++i)
    {
        body *a = bodies + i;
        a->x += dt * a->vx;
        a->y += dt * a->vy;
        a->z += dt * a->vz;
    }
}

inline static void simulate(body *bodies, size_t number_of_bodies,
        double number_of_steps, double dt)
{
    printf("Initial energy: %.9lf\n", energy(bodies, number_of_bodies));
    clock_t start = clock();
    for (size_t i = 0; i < number_of_steps; ++i)
    {
        advance(bodies, number_of_bodies, dt);
    }
    clock_t stop = clock();
    printf("Final energy:   %.9lf\n", energy(bodies, number_of_bodies));
    printf("Elapsed: %lfs\n", (double)(stop-start)/CLOCKS_PER_SEC);
}

int main(int argc, char **argv)
{
    double const dt = 0.01;

    if (argc < 3)
    {
        fprintf(stderr, "usage: nbody <filename> <time-steps>\n");
        return 1;
    }
    char const *filename = argv[1];
    int const number_of_steps = atoi(argv[2]);
    if (number_of_steps < 1)
    {
        fprintf(stderr, "error: simulation duration less than 1\n");
        return 2;
    }

    body *bodies = NULL;
    size_t number_of_bodies = read_bodies(filename, &bodies);
    if (!bodies)
    {
        return -1;
    }

    offset_momentum(bodies, number_of_bodies);

    simulate(bodies, number_of_bodies, number_of_steps, dt);
    printf("\n");
    simulate(bodies, number_of_bodies, number_of_steps, dt);

    for (size_t i = 0; i < number_of_bodies; ++i)
    {
        body_free(&bodies[i]);
    }
    free(bodies);

    return 0;
}
