import json
import os
import torch
from torch.utils.data import Dataset, DataLoader, random_split
from torchvision import transforms
from PIL import Image
import numpy as np
from glob import glob
from dotenv import load_dotenv

load_dotenv()

FOOD_DATASET_PATH = os.getenv("FOOD_DATASET_PATH")
FOOD_META = os.path.join(FOOD_DATASET_PATH, "meta")
FOOD_IMAGES = os.path.join(FOOD_DATASET_PATH, "images")

BATCH_SIZE = 8
NUM_EPOCHS = 10
LEARNING_RATE = 0.001
NUM_WORKERS = 4
IMAGE_SIZE = 640

def get_metadata(file: str):
    with open(os.path.join(FOOD_META, file), "r") as f:
        classes = [line.strip() for line in f.readlines()]
    return classes


def load_food_metadata():
    food = get_metadata("classes.txt")
    ingredients = get_metadata("ingredients.txt")
    all_metadata = food + ingredients
    index_map = {item: idx for idx, item in enumerate(all_metadata)}

    map_file_path = os.path.join(FOOD_META, "map.json")
    with open(map_file_path, "r") as f:
        food_ingredient_map = json.load(f)

    # Create multi-label arrays for each food item
    label_arrays = {}

    for food_item, food_ingredients in food_ingredient_map.items():
        # Initialize with zeros
        label_array = np.zeros(len(all_metadata), dtype=np.int32)

        label_array[index_map[food_item]] = 1
        for ingredient in food_ingredients:
            label_array[index_map[ingredient]] = 1
        label_arrays[food_item] = label_array

    return label_arrays, all_metadata


class FoodDataset(Dataset):
    def __init__(self, root_dir, label_arrays, transform=None):
        self.root_dir = root_dir
        self.transform = transform
        self.samples = []

        # Collect all images with their labels
        for food_name, label_array in label_arrays.items():
            food_dir = str(os.path.join(root_dir, food_name))
            if not os.path.exists(food_dir):
                continue

            image_files = glob(os.path.join(food_dir, "*.jpg"))
            for img_path in image_files:
                self.samples.append((img_path, label_array))

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        img_path, label = self.samples[idx]
        image = Image.open(img_path).convert('RGB')

        if self.transform:
            image = self.transform(image)

        return image, torch.tensor(label, dtype=torch.float32)


# Create wrapper datasets to apply different transforms
class TransformDataset(Dataset):
    def __init__(self, dataset, transform):
        self.dataset = dataset
        self.transform = transform

    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, idx):
        image, label = self.dataset[idx]  # image is already a tensor
        print('__getitem__: ', image, label)

        # Ensure transformation is only applied to images, not tensors
        if isinstance(image, Image.Image):
            image = self.transform(image)  # Apply the transform if it's still a PIL image

        return image, label


def prepare_data():
    # Load metadata and create label arrays
    label_arrays, all_metadata = load_food_metadata()

    # Define transformations
    train_transform = transforms.Compose([
        transforms.RandomResizedCrop(IMAGE_SIZE),
        transforms.RandomHorizontalFlip(),
        transforms.ColorJitter(brightness=0.1, contrast=0.1, saturation=0.1),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

    val_transform = transforms.Compose([
        transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

    # Create a single dataset with all foods
    dataset = FoodDataset(
        root_dir=FOOD_IMAGES,
        label_arrays=label_arrays,
        transform=None  # We'll apply transforms after splitting
    )

    # Split dataset into train and validation sets (80/20 ratio)
    dataset_size = len(dataset)
    train_size = int(0.8 * dataset_size)
    val_size = dataset_size - train_size

    train_dataset, val_dataset = random_split(dataset, [train_size, val_size],
                                              generator=torch.Generator().manual_seed(42))



    # Apply appropriate transforms
    train_dataset_transformed = TransformDataset(train_dataset, train_transform)
    val_dataset_transformed = TransformDataset(val_dataset, val_transform)

    # Create dataloaders
    train_loader = DataLoader(
        train_dataset_transformed,
        batch_size=BATCH_SIZE,
        shuffle=True,
        num_workers=NUM_WORKERS,
        pin_memory=True
    )

    val_loader = DataLoader(
        val_dataset_transformed,
        batch_size=BATCH_SIZE,
        shuffle=False,
        num_workers=NUM_WORKERS,
        pin_memory=True
    )

    return train_loader, val_loader, len(all_metadata)