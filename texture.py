from PIL import Image
import os

def slice_image(image_path, output_dir, out_prefix):
    # Open the image file
    image = Image.open(image_path)
    width, height = image.size
    
    # Ensure output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Slice every 16 pixels and save
    slice_number = 0
    for top in range(0, height, 16):
        for left in range(0, width, 16):
            box = (left, top, left + 16, top + 16)
            region = image.crop(box)
            region.save(os.path.join(output_dir, f"{out_prefix}_{slice_number}.png"))
            slice_number += 1
    
    print(f"Successfully sliced {slice_number} images into {output_dir}")

# Example usage
image_path = input("Enter image path: ")  # Replace with your image path
out_prefix = input("Enter out prefix: ")
output_dir = "output_slices"
slice_image(image_path, output_dir, out_prefix)