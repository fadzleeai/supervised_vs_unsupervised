import os
import shutil
import random

# Source directory
source_dir = "images"

# Output directory
output_dir = "dataset_split"
train_ratio = 0.8

# Target categories
target_categories = ['plastic_water_bottles','aluminum_soda_cans','cardboard_boxes',]

# Create output folders
train_dir = os.path.join(output_dir, "train")
test_dir = os.path.join(output_dir, "test")

os.makedirs(train_dir, exist_ok=True)
os.makedirs(test_dir, exist_ok=True)

# Loop through all folders inside images/
for folder in os.listdir(source_dir):
    folder_path = os.path.join(source_dir, folder)

    if not os.path.isdir(folder_path):
        continue

    # Check if folder name matches any target category
    matched = any(t.lower() in folder.lower() for t in target_categories)
    if not matched:
        print(f"[SKIP] {folder} not in target categories.")
        continue

    print(f"[PROCESS] {folder}")

    # Real world folder
    real_world_path = os.path.join(folder_path, "real_world")
    if not os.path.exists(real_world_path):
        print(f"[SKIP] No real_world folder in {folder}")
        continue

    # Create category directories in train/test
    train_cat_dir = os.path.join(train_dir, folder)
    test_cat_dir = os.path.join(test_dir, folder)

    os.makedirs(train_cat_dir, exist_ok=True)
    os.makedirs(test_cat_dir, exist_ok=True)

    # Collect images
    imgs = [
        f for f in os.listdir(real_world_path)
        if os.path.isfile(os.path.join(real_world_path, f))
    ]

    random.shuffle(imgs)
    split = int(len(imgs) * train_ratio)

    train_imgs = imgs[:split]
    test_imgs = imgs[split:]

    # Copy train images
    for img in train_imgs:
        shutil.copy(
            os.path.join(real_world_path, img),
            os.path.join(train_cat_dir, img)
        )

    # Copy test images
    for img in test_imgs:
        shutil.copy(
            os.path.join(real_world_path, img),
            os.path.join(test_cat_dir, img)
        )

    print(f"[OK] {folder}: Train={len(train_imgs)}, Test={len(test_imgs)}")

print("\n[DONE] Dataset split complete!")