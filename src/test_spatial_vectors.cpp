#include "spatial_vectors.h"

int test_spatial_vectors(){
    // Test initializing with an initializer list.
    MotionVector vel{1., 2., 3., 4., 5., 6.};
    ForceVector force{1., 2., 3., 4., 5., 6.};

    // Test indexing.
    assert(vel[0] == 1.0);
    assert(force[1] == 2.0);

    // Test multiplication.
    double power = vel*force;

    return 0;
}

int main(){
    return test_spatial_vectors();
}