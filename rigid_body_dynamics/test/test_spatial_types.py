"""
Tests for the spatial_types.py file.
"""
import unittest
import numpy as np
from rigid_body_dynamics.spatial_types import (Frame, SpatialVector, Twist)


class TestFrame(unittest.TestCase):
    """
    Tests for the Frame class.
    """
    def test_create_frame(self):
        """
        Test creating frames.
        """
        # New frames should be given new ids.
        frame1 = Frame()
        frame2 = Frame()
        self.assertFalse(frame1 == frame2)

    def test_frame_equality(self):
        """
        Test frame equality operator.
        """
        # Frames with the same id should be equal.
        frame1 = Frame()
        frame2 = Frame(frame1.get_id())
        self.assertTrue(frame1 == frame2)


class TestSpatialVector(unittest.TestCase):
    """
    Tests for the SpatialVector class.
    """
    def test_create_vector(self):
        """
        Test constructor.
        """
        # The frame should be created automatically, and the data should be copied in.
        data = np.random.random(6)
        vector = SpatialVector(data)
        self.assertTrue(isinstance(vector.frame, Frame))
        np.testing.assert_array_equal(data, vector.data())

    def test_data_copy(self):
        """
        Test that data is copied in properly.
        """
        # The constructor should not be passing data by reference.
        data = np.zeros(6)
        copied_data = data.copy()
        vector = SpatialVector(data)
        data[0] += 1.0
        np.testing.assert_array_equal(copied_data, vector.data())
        self.assertFalse(np.allclose(data, vector.data()))


class TestTwist(unittest.TestCase):
    """
    Tests for the Twist class.
    """
    def test_create_twist(self):
        """
        Test construction.
        """
        data = np.arange(6)
        twist = Twist(data)
        self.assertTrue(isinstance(twist.frame, Frame))
        np.testing.assert_array_equal(twist.angular(), data[0:3])
        np.testing.assert_array_equal(twist.linear(), data[3:6])

    def test_add(self):
        """
        Test the addition operation.
        """
        # Twist addition should add the underlying data vectors.
        data1 = np.arange(6)
        data2 = np.ones(6)
        twist1 = Twist(data1)
        twist2 = Twist(data2, twist1.frame)
        twist3 = twist1 + twist2
        self.assertTrue(twist3.frame == twist1.frame)
        np.testing.assert_array_equal(twist3.data(),
                                      twist1.data() + twist2.data())

        # Twists in different frames should not add.
        twist4 = Twist(data1)
        self.assertRaises(AssertionError, lambda: twist1 + twist4)


# TODO(pvarin): finish adding spatial types.

if __name__ == '__main__':
    np.random.seed(1)
    unittest.main()
