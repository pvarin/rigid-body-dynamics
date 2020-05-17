import os
from xml.etree.ElementTree import ElementTree
from rigid_body_dynamics.rigid_body_mechanism import RigidBodyMechanism

# TODO: add validation
def parse_model_from_sdf(path):
    root = ElementTree()
    sdf = tree.parse(path)
    model = sdf.find('model')
    mechanism = RigidBodyMechanism()
    
    for frame in model.findall('frame'):
        pose = frame.find('pose')
        relative_to = frame.
        mechanism.add_frame()
    

    

def validate_required(num_elements, spec):

def validate_attribute(attribute, spec):
    pass

def validate_element(element, spec):
    assert element.tag in spec, 'tag {} is not in the SDF spec'.format(element.tag)
    for attrib_name, attrib_value in element.attrib.items():
        assert attrib_name in spec[element.tag]['attributes']
        
        validate_attribute(attrib_value, spec[element.tag]['attributes'][attrib_name])
        
    for child in attrib
    if element.tag == 'sdf':
        assert 'version'
        valid_children = ['world', 'model', 'actor', 'light']
        for children in element.getchildren():
            assert
    
    
if __name__ == "__main__":
    cassie_path = os.path.join('cassie', 'cassie.sdf')
    tree = parse_sdf(cassie_path)
    import pdb; pdb.set_trace()
    