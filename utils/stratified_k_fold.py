import os
import shutil
from sklearn.model_selection import StratifiedKFold

# Source dataset (Dataset Kaggle)
source_dir = "images"

# Output directory
output_dir = input("Folder name: ")

# Target categories
target_categories = [
    'plastic_water_bottles',
    'aluminum_soda_cans',
    'cardboard_boxes',
]

# Number of folds
K = 5

# ============================
# STEP 1 — LOAD ALL IMAGES
# ============================
all_images = []
all_labels = []

for class_name in target_categories:
    class_path = os.path.join(source_dir, class_name, "real_world")

    if not os.path.exists(class_path):
        print(f"[SKIP] Missing real_world in {class_name}")
        continue

    imgs = [
        f for f in os.listdir(class_path)
        if os.path.isfile(os.path.join(class_path, f))
    ]

    for img in imgs:
        all_images.append(os.path.join(class_path, img))
        all_labels.append(class_name)   # label for stratification

print(f"Total images loaded: {len(all_images)}")


# ============================
# STEP 2 — STRATIFIED K-FOLD
# ============================
skf = StratifiedKFold(n_splits=K, shuffle=True, random_state=42)

for fold_idx, (train_idx, test_idx) in enumerate(skf.split(all_images, all_labels), start=1):
    
    print(f"\n[PROCESS] Fold {fold_idx}")

    fold_dir = os.path.join(output_dir, f"fold_{fold_idx}")
    train_dir = os.path.join(fold_dir, "train")
    test_dir  = os.path.join(fold_dir, "test")

    # Create folders for all classes
    for class_name in target_categories:
        os.makedirs(os.path.join(train_dir, class_name), exist_ok=True)
        os.makedirs(os.path.join(test_dir, class_name), exist_ok=True)

    # Copy train images
    for i in train_idx:
        img_path = all_images[i]
        class_name = all_labels[i]
        shutil.copy(img_path, os.path.join(train_dir, class_name))

    # Copy test images
    for i in test_idx:
        img_path = all_images[i]
        class_name = all_labels[i]
        shutil.copy(img_path, os.path.join(test_dir, class_name))

    print(f"[OK] Fold {fold_idx}: Train={len(train_idx)}, Test={len(test_idx)}")

print("\n[DONE] Stratified K-Fold dataset created!")
