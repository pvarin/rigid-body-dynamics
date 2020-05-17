"""
Defines several spatial quantities and the operations between them.
"""
from attr import attrs, attrib


class Frame:
    """
    Creates the notion of a coordinate frame for comparison when doing spatial math.
    """
    num_frames = 0

    @classmethod
    def get_next_frame_id(cls):
        """
        Returns the next unique id.
        """
        frame_id = cls.num_frames
        cls.num_frames += 1
        return frame_id

    def __init__(self, frame_id=None):
        if frame_id is None:
            self._id = self.get_next_frame_id()
        else:
            self._id = frame_id

    def get_id(self):
        """
        Accessor for the frame id.
        """
        return self._id

    def __eq__(self, other):
        return self._id == other._id


class OperatorTypeError(Exception):
    """
    An exception type when an operator is used on incompatible types.
    """
    def __init__(self, cls1, cls2):
        super(OperatorTypeError, self).__init__()
        self.message = "Multiplication is not defined between {} and {}".format(
            cls1, cls2)


@attrs
class SpatialVector:
    """
    The base class of six dimensional spatial vectors.
    """
    _data = attrib(converter=lambda x: x.copy())
    frame = attrib(factory=Frame)

    @property
    def data(self):
        """
        Accessor for the underlying data.
        """
        return self._data

    def angular(self):
        """
        Returns the angular component of the spatial vector.
        """
        # TODO: return the angular type that is appropriate for the specific spatial type
        return self._data[:3]

    def linear(self):
        """
        Returns the linear component of the spatial vector.
        """
        # TODO: return the linear type that is appropriate for the specific spatial type
        return self._data[3:]


class Twist(SpatialVector):
    """
    A twist type for spatial velocities.
    """
    def __mul__(self, other):
        assert self.frame == other.frame, "Frames must match"
        if isinstance(other, Wrench):
            return self._data.dot(other.data())
        if isinstance(other, SpatialInertia):
            return SpatialMomentum(self._data.dot(other.data()),
                                   frame=self.frame)
        raise OperatorTypeError(self.__class__, other.__class__)

    def __add__(self, other):
        assert self.frame == other.frame, "Frames must match"
        assert isinstance(other,
                          Twist), "Addition is only defined between two Twists"
        return Twist(self._data + other.data(), frame=self.frame)


class Wrench(SpatialVector):
    """
    A wrench type for spatial forces.
    """
    def __mul__(self, other):
        assert self.frame == other.frame, "Frames must match"
        if isinstance(other, Twist):
            return self._data.dot(other.data())
        raise OperatorTypeError(self.__class__, other.__class__)

    def __add__(self, other):
        assert self.frame == other.frame, "Frames must match"
        assert isinstance(
            other, Wrench), "Addition is only defined between two Wrenches"
        return Wrench(self._data + other.data(), frame=self.frame)


@attrs
class SpatialInertia:
    """
    A spatial inertia type.
    """
    _data = attrib()
    frame = attrib(factory=Frame)

    def __mul__(self, other):
        assert self.frame == other.frame, "Frames must match"
        if isinstance(other, Twist):
            return SpatialMomentum(data=self._data.dot(other.data()),
                                   frame=self.frame)
        raise OperatorTypeError(self.__class__, other.__class__)

    def __add__(self, other):
        assert self.frame == other.frame, "Frames must match"
        assert isinstance(
            other, SpatialInertia
        ), "Addition is only defined between two SpatialInertias"
        return SpatialInertia(self._data + other.data(), frame=self.frame)


@attrs
class SpatialInverseInertia:
    """
    A spatial inverse inertia type. This type is rarely used but included for completeness.
    """
    _data = attrib()
    frame = attrib(factory=Frame)

    def __mul__(self, other):
        assert self.frame == other.frame, "Frames must match"
        if isinstance(other, Wrench):
            return Twist(data=self._data.dot(other.data()), frame=self.frame)
        raise OperatorTypeError(self.__class__, other.__class__)


class SpatialMomentum(SpatialVector):
    """
    A spatial momentum type. The product of a spatial inertia and a twist.
    """
    def __mul__(self, other):
        assert self.frame == other.frame, "Frames must match"
        raise NotImplementedError

    def __add__(self, other):
        assert self.frame == other.frame, "Frames must match"
        assert isinstance(
            other, SpatialMomentum
        ), "Addition is only defined between two SpatialMomenta"
        return SpatialMomentum(self._data + other.data(), frame=self.frame)

@attrs
class Quaternion:
    """
    A rotation from one frame to another.
    """    
    _data = attrib()
    
    @property
    def data(self):
        return self._data
    
    @property
    def w(self):
        return self._data[0]
    
    @property
    def x(self):
        return self._data[1]
    
    @property
    def y(self):
        return self._data[2]
    
    @property
    def z(self):
        return self._data[3]
    
    @property
    def xyz(self):
        return self.data[1:]
    
    def mat(self):
        w = self.w()
        x = self.x()
        y = self.y()
        z = self.z()
        return np.array(
            [1-2*(y**2 + z**2),     2*(x*y - w*z),    2*(x*z + w*y)],
            [    2*(y*x + w*z), 1-2*(x**2 + z**2),    2*(y*z - w*x)],
            [    2*(z*x - w*y),     2*(z*y + w*x), 1-2*(x**2 + y**2)]
        )
        
    def conj(self):
        data_new = self._data.copy()
        data_new[1:] *= -1
        return Quaternion(data=data_new)
    
    @classmethod
    def identity(cls):
        return cls(data=np.array([1., 0., 0., 0.]))

@attrs
class Transform:
    """
    A transform from one frame into another.
    """
    _translation = attrib()
    _quaternion = attrib()
    _from = attrib()
    _to = attrib()
    
    def translation(self):
        return self._translation
    
    def quaternion(self):
        return self._quaternion
    
    def mat(self):
        return np.blk([[self._quaternion.mat(), _translation.data()[:,np.newaxis]],
                       [         np.zeros(1,3),                               1.0]])
