#include <Eigen/Dense>

// The dimension of a spatial vector.
constexpr int kSpatialDim = 6;

// Alias for 6D Eigen vectors.
template <typename T>
using Vector6 = Eigen::Matrix<T, kSpatialDim, 1>;

/*
 * class SpatialVector
 * Base class for spatial vectors, e.g. MotionVectors and ForceVectors. A thin
 * wrapper around a six dimensional Eigen vector.
 */
template <typename T>
class SpatialVector {
 public:
  SpatialVector(const Vector6<T>& data) : _data(data) {}
  SpatialVector(std::initializer_list<T> init_list) {
    assert(init_list.size() == _data.RowsAtCompileTime);
    int i=0;
    for (const auto& val : init_list){
        _data(i) = val;
        i++;
    }
  }
  
  const Vector6<T>& data() const { return _data; }
  T& operator[](int idx) { return _data[idx]; }
  friend std::ostream& operator<<(std::ostream& os, const SpatialVector& vec) {
    os << vec.data();
    return os;
  }

 protected:
  Vector6<T> _data;
};

/*
 * class MotionVector
 * A spatial motion vector type. E.g. spatial velocities, spatial accelerations.
 */
template <typename T>
class MotionVector : public SpatialVector<T> {
 public:
  MotionVector(const Vector6<T>& data) : SpatialVector<T>(data) {}
  MotionVector(std::initializer_list<T> init_list) : SpatialVector<T>(init_list) {}

  T& operator[](int idx) { return this->_data[idx]; }
  const T& operator[](int idx) const { return this->_data[idx]; }
};

/*
 * class ForceVector
 * A spatial force vector type. E.g. spatial forces, spatial momenta.
 */
template <typename T>
class ForceVector : public SpatialVector<T> {
 public:
  ForceVector(const Vector6<T>& data) : SpatialVector<T>(data) {}
  ForceVector(std::initializer_list<T> init_list) : SpatialVector<T>(init_list) {}
  T& operator[](int idx) { return this->_data[idx]; }
  const T& operator[](int idx) const { return this->_data[idx]; }
};

template <typename T>
T operator*(const MotionVector<T>& m, const ForceVector<T>& f) {
  return m.data().transpose() * f.data();
}

template <typename T>
T operator*(const ForceVector<T>& f, const MotionVector<T>& m) {
  return m * f;
}