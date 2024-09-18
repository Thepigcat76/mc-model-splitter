import json
import os

# Size of each chunk (16x16x16)
CHUNK_SIZE = 16

# Define the ranges for slicing (X: [-16, 0, 16], Y: [0, 16], Z: [-16, 0, 16])
x_ranges = range(-16, 32, CHUNK_SIZE)
y_ranges = range(0, 32, CHUNK_SIZE)
z_ranges = range(-16, 32, CHUNK_SIZE)

# Function to determine if an element should be part of a specific chunk
def is_element_in_chunk(element, x_range, y_range, z_range):
    x_from, y_from, z_from = element['from']
    x_to, y_to, z_to = element['to']

    return not (x_to <= x_range[0] or x_from >= x_range[1] or
                y_to <= y_range[0] or y_from >= y_range[1] or
                z_to <= z_range[0] or z_from >= z_range[1])

# Function to clip the element to the chunk boundaries
def clip_element_to_chunk(element, x_range, y_range, z_range):
    new_from = [
        max(element['from'][0], x_range[0]),
        max(element['from'][1], y_range[0]),
        max(element['from'][2], z_range[0])
    ]
    new_to = [
        min(element['to'][0], x_range[1]),
        min(element['to'][1], y_range[1]),
        min(element['to'][2], z_range[1])
    ]
    return {
        'from': new_from,
        'to': new_to,
        'faces': element['faces']
    }

# Function to adjust element to fit within the [0, 0, 0] to [16, 16, 16] space of each chunk
def adjust_element_to_chunk_space(element, chunk_origin):
    adjusted_element = element.copy()
    
    # Offset the "from" and "to" coordinates by the chunk origin to center it in the chunk space
    adjusted_element['from'] = [coord - chunk_origin[i] for i, coord in enumerate(adjusted_element['from'])]
    adjusted_element['to'] = [coord - chunk_origin[i] for i, coord in enumerate(adjusted_element['to'])]
    
    return adjusted_element

# Function to slice the model into 16x16x16 chunks
def slice_model_into_chunks(model_data):
    sliced_models = []

    for x_start in x_ranges:
        for y_start in y_ranges:
            for z_start in z_ranges:
                chunk_elements = []
                chunk_origin = [x_start, y_start, z_start]  # Define the origin of the current chunk

                for element in model_data['elements']:
                    x_range = (x_start, x_start + CHUNK_SIZE)
                    y_range = (y_start, y_start + CHUNK_SIZE)
                    z_range = (z_start, z_start + CHUNK_SIZE)

                    if is_element_in_chunk(element, x_range, y_range, z_range):
                        clipped_element = clip_element_to_chunk(element, x_range, y_range, z_range)
                        adjusted_element = adjust_element_to_chunk_space(clipped_element, chunk_origin)
                        chunk_elements.append(adjusted_element)

                if chunk_elements:
                    chunk_model = {
                        "credit": model_data["credit"],
                        "elements": chunk_elements
                    }
                    sliced_models.append({
                        "model": chunk_model,
                        "chunk_coords": (x_start, y_start, z_start)
                    })

    return sliced_models

# Save each sliced model as a new JSON file
def save_sliced_models(sliced_elements, prefix):
    output_dir = "sliced"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for idx, chunk_data in enumerate(sliced_elements):
        chunk_model = chunk_data["model"]
        x_start, y_start, z_start = chunk_data["chunk_coords"]
        
        # Filename follows the format: prefix_chunk_x_y_z.json
        filename = os.path.join(output_dir, f"{prefix}_{idx}.json")
        with open(filename, "w") as f:
            json.dump(chunk_model, f, indent=4)
        print(f"Saved {filename}")

# Main logic to slice the model and save each piece
def main():
    model_path = input("Enter model path: ")  # Path to the model file
    out_prefix = input("Enter output prefix: ")  # Prefix for the output files

    with open(model_path) as file:
        sliced_elements = slice_model_into_chunks(json.load(file))
        save_sliced_models(sliced_elements, out_prefix)

if __name__ == "__main__":
    main()