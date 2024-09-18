import os
import json

# Function to adjust element to fit within the [0, 0, 0] to [16, 16, 16] space of each chunk
def adjust_element_to_chunk_space(element, chunk_origin):
    adjusted_element = element.copy()
    
    # Offset the "from" and "to" coordinates by the chunk origin
    adjusted_element['from'] = [coord - origin for coord, origin in zip(adjusted_element['from'], chunk_origin)]
    adjusted_element['to'] = [coord - origin for coord, origin in zip(adjusted_element['to'], chunk_origin)]
    
    return adjusted_element

def single_shape(element):
    dest = element["to"]
    origin = element["from"]
    print(f"Block.box({origin[0]}, {origin[1]}, {origin[2]}, {dest[0]}, {dest[1]}, {dest[2]});")

def double_shape(element_0, element_1):
    dest_0 = element_0["to"]
    origin_0 = element_0["from"]
    dest_1 = element_1["to"]
    origin_1 = element_1["from"]
    print(f"Shapes.or(Block.box({origin_0[0]}, {origin_0[1]}, {origin_0[2]}, {dest_0[0]}, {dest_0[1]}, {dest_0[2]}), Block.box({origin_1[0]}, {origin_1[1]}, {origin_1[2]}, {dest_1[0]}, {dest_1[1]}, {dest_1[2]}));")

def multiple_shape(elements):
    code = "Stream.of("
    for idx, elem in enumerate(elements):
        dest = elem["to"]
        origin = elem["from"]
        code += f"Block.box({origin[0]}, {origin[1]}, {origin[2]}, {dest[0]}, {dest[1]}, {dest[2]})"
        if idx != len(elements) - 1:
            code += ','
    code += ").reduce(Shapes::or).get();"
    print(code)

def output_code(elements):
    if len(elements) == 0:
        return
    elif len(elements) == 1:
        single_shape(elements[0])
    elif len(elements) == 2:
        double_shape(elements[0], elements[1])
    else:
        multiple_shape(elements)

def create_shape(file_path):
    with open(file_path) as file:
        model = json.load(file)
        elements = model['elements']
        
        # We assume the file's name contains the chunk's origin coordinates
        # Example: "model_chunk_-16_0_-16.json"
        filename = os.path.basename(file_path)
        # 0 is the index
        chunk_origin = [0, 0, 0]
        
        # Adjust each element to the chunk space (centered)
        adjusted_elements = [adjust_element_to_chunk_space(elem, chunk_origin) for elem in elements]
        
        # Output the voxel shape code
        output_code(adjusted_elements)

models_path = input("Enter path to your models directory: ")

for filename in os.listdir(models_path):
    file_path = os.path.join(models_path, filename)
    if os.path.isfile(file_path):
        create_shape(file_path)