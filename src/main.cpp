#include <iostream>
#include <vector>

#include "spatial_vectors.h"

int main() {
  std::cout << "Hello world" << std::endl;  
  MotionVector<double> vel{1., 2., 3., 4., 5., 6.};
  ForceVector<double> force{1., 2., 3., 4., 5., 6.};
  // auto test = data == vel.data();
  std::cout << "Velocity:\n" << vel << std::endl;
  std::cout << vel * force << std::endl;
  std::cout << force * vel << std::endl;

  return 0;
}