from attr import attrs, attrib
from spatial_types import Frame

@attrs
class Joint:
    """
    The Joint base class.
    """
    _frame_before = attrib()
    _frame_after = attrib()
    _joint_info = attrib()
    
@attrs
class RotaryJointInfo:
    """
    A data structure for rotary joints.
    """
    @classmethod
    def parse_urdf(cls, xml_string):
        xml_string

@attrs
class Link:
    """
    A rigid link in a mechanism.
    """
    _inertia = attrib()
    _base_frame = attrib(factory=Frame)
    _joint_frames = attrib(factory=list)

@attrs
class RigidBodyMechanism:
    _links = attrib()
    _joints = attrib()
    
    def add_link(self):
        pass
    
    def add_revolute_joint(self, link1, link2, joint_info):
        joint = joint_info.cls()
        link1.add_joint(joint)
        link2.add_joint(joint)