import os
from PIL import Image
import pillow_heif

input_dir = "ml_image_dataset"
output_dir = "real_world_data"

os.makedirs(output_dir, exist_ok=True)

for class_folder in os.listdir(input_dir):
    class_path = os.path.join(input_dir, class_folder)
    output_class_path = os.path.join(output_dir, class_folder)
    os.makedirs(output_class_path, exist_ok=True)

    for file_name in os.listdir(class_path):
        file_path = os.path.join(class_path, file_name)
        if file_name.lower().endswith(".heic"):
            heif_file = pillow_heif.read_heif(file_path)
            image = Image.frombytes(
                heif_file.mode,
                heif_file.size,
                heif_file.data,
                "raw",
                heif_file.mode,
                heif_file.stride,
            )
            jpg_file = os.path.splitext(file_name)[0] + ".jpg"
            image.save(os.path.join(output_class_path, jpg_file), format="JPEG")
        else:
            dst = os.path.join(output_class_path, file_name)
            if not os.path.exists(dst):
                os.system(f'copy "{file_path}" "{dst}"')
