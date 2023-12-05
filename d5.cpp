// g++ d5.cpp -I. -o exec -O3 -fopenmp

#include <array>
#include <vector>
#include <cstdint>
#include <iostream>
#include <omp.h>

#include "d5.hpp"

using std::vector;
using std::array;


int64_t applyMap(int64_t value, int64_t destination, int64_t start, int64_t diff)
{
    if (start <= value && value < start + diff)
    {
        return destination + value - start;
    }
    else
    {
        return -1;
    }
}
int64_t applyMapsToSeed(int64_t seed, const vector<vector<vector<int64_t>>>& mappings) {
    for (const vector<vector<int64_t>>& mapping : mappings) {
        for (const vector<int64_t>& entry : mapping) {
            int64_t start = entry[0];
            int64_t destination = entry[1];
            int64_t diff = entry[2];

            int64_t value = applyMap(seed, start, destination, diff);
            if (value != -1) {
                seed = value;
                break;
            }
        }
    }
    return seed;
}

int64_t applyMapsToRange(int64_t seedStart, int64_t seedDiff, const std::vector<std::vector<std::vector<int64_t>>>& mappings) {
    int64_t minimum = -1;  // Assuming -1 as an initial placeholder for minimum

    for (int64_t seed = seedStart; seed < seedStart + seedDiff; seed++) {
        int64_t result = applyMapsToSeed(seed, mappings);

        if (minimum == -1) {
            minimum = result;
        } else {
            minimum = std::min(result, minimum);
        }
    }
    return minimum;
}

int main()
{

    int64_t *minimums = new int64_t[seedsRanges.size()/2];

    int64_t minimum = INT64_MAX;

    #pragma omp parallel for schedule(dynamic)
    for (size_t k = 0; k < seedsRanges.size()/2; k++)
    {
        int64_t value = applyMapsToRange(seedsRanges[k*2], seedsRanges[k*2+1], parsedMappings);
        minimums[k] = value;
    }

    for (size_t k = 0; k < seedsRanges.size()/2; k++)
    {
        minimum = std::min(minimum, minimums[k]);
    }
    std::cout << "Part 2: " << minimum << std::endl;

    delete minimums;

    return 0;
}