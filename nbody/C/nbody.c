#include <json/json.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char *strdup(char const *str)
{
    char *dst = malloc(strlen(str)+1);
    strcpy(dst, str);
    return dst;
}

typedef struct bodies
{
    size_t number_of_bodies;
    double unitmass;
    char **name;
    double *mass;
    double *x, *y, *z;
    double *vx, *vy, *vz;
} bodies;

bodies *bodies_alloc(size_t n)
{
    size_t const bytes = sizeof(bodies) + 7*n*sizeof(double) + n*sizeof(char*); 
    bodies *b = calloc(bytes, sizeof(char));
    if (b)
    {
        b->number_of_bodies = n;
        b->unitmass = 1.0;
        b->name = (char**)(b + 1);
        b->mass = (double*)(b->name + n);
        b->x = b->mass + n;
        b->y = b->x + n;
        b->z = b->y + n;
        b->vx = b->z + n;
        b->vy = b->vx + n;
        b->vz = b->vy + n;
    }
    return b;
}

void bodies_free(bodies *b)
{
    if (b)
    {
        for (size_t i = 0; i < b->number_of_bodies; ++i)
        {
            free(b->name[i]);
        }
        free(b);
    }
}

int bodies_add_mass(bodies *b, struct json_object *json, size_t i)
{
    if (json_object_is_type(json, json_type_double))
    {
        b->mass[i] = b->unitmass * json_object_get_double(json);
        return 0;
    }
    else
    {
        fprintf(stderr, "error: mass must be a double\n");
        return 1;
    }
}

int bodies_add_position(bodies *b, struct json_object *json, size_t i)
{
    if (json_object_is_type(json, json_type_array))
    {
        struct json_object *position = json_object_array_get_idx(json, 0);
        if (position)
        {
            if (json_object_is_type(position, json_type_double))
            {
                b->x[i] = json_object_get_double(position);
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
                b->y[i] = json_object_get_double(position);
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
                b->z[i] = json_object_get_double(position);
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

int bodies_add_velocity(bodies *b, struct json_object *json, size_t i)
{
    if (json_object_is_type(json, json_type_array))
    {
        struct json_object *velocity = json_object_array_get_idx(json, 0);
        if (velocity)
        {
            if (json_object_is_type(velocity, json_type_double))
            {
                b->vx[i] = json_object_get_double(velocity);
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
                b->vy[i] = json_object_get_double(velocity);
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
                b->vz[i] = json_object_get_double(velocity);
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

int bodies_add(bodies *b, char const *name, struct json_object *json, size_t i)
{
    int ret = 0;
    b->name[i] = strdup(name);
    int mass_seen = 0, position_seen, velocity_seen = 0;
    json_object_object_foreach(json, key, value) {
        if (strcmp(key, "mass") == 0)
        {
            mass_seen = 1;
            if (bodies_add_mass(b, value, i))
            {
                ret = -1;
            }
        }
        else if (strcmp(key, "position") == 0)
        {
            position_seen = 1;
            if (bodies_add_position(b, value, i))
            {
                ret = -2;
            }
        }
        else if (strcmp(key, "velocity") == 0)
        {
            velocity_seen = 1;
            if (bodies_add_velocity(b, value, i))
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

bodies *bodies_read(char const *filename)
{
    struct json_object *json = json_object_from_file(filename);
    if (!json)
    {
        exit(1);
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
                return NULL;
            }
        }
    }

    bodies *b = bodies_alloc(number_of_bodies);
    if (b)
    {
        b->unitmass = unitmass;

        size_t index = 0;
        json_object_object_foreach(json, key, value)
        {
            if (strcmp(key, "unitmass") != 0)
            {
                if (bodies_add(b, key, value, index))
                {
                    free(b);
                    b = NULL;
                    break;
                }
                index += 1;
            }
        }
    }

    json_object_put(json);

    return b;
}

void bodies_print(bodies *b)
{
    if (!b)
    {
        printf("No bodies provide.\n");
    }

    if (b->number_of_bodies == 1)
    {
        printf("System has %d body:\n", b->number_of_bodies);
    }
    else
    {
        printf("System has %d bodies:\n", b->number_of_bodies);
    }

    for (size_t i = 0; i < b->number_of_bodies; ++i)
    {
        printf("%s:\n", b->name[i]);
        printf("  mass:     %le\n", b->mass[i]);
        printf("  position: [%le, %le, %le]\n", b->x[i], b->y[i], b->z[i]);
        printf("  velocity: [%le, %le, %le]\n", b->vx[i], b->vy[i], b->vz[i]);
    }
}

int main()
{
    bodies *b = bodies_read("data.json");
    if (b)
    {
        bodies_print(b);
    }
    bodies_free(b);
}
