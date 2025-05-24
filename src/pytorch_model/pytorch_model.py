import os
from PIL import Image
from pytorch_model.model import FoodModel
import torch
from src.pytorch_model.food_dataset import get_metadata
from torchvision import transforms

def load_model(model_path, num_classes):
    device = torch.device('cuda' if torch.cuda.is_available() else 
                          'mps' if torch.backends.mps.is_available() else 
                          'cpu')
    
    model = FoodModel(num_classes)
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.to(device)
    model.eval()
    
    return model, device

def load_food_metadata():
    food = get_metadata("classes.txt")
    ingredients = get_metadata("ingredients.txt")
    total_metadata = food + ingredients
    return food, ingredients, total_metadata

def preprocess_image(image: Image):
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    return transform(image).unsqueeze(0)

class FoodImageModel:
    _instance = None
    _food_metadata = None
    _ingredient_metadata = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls._create_instance()
        return cls._instance
    
    @classmethod
    def get_device(cls):
        if cls._device is None:
            cls.get_instance()
        return cls._device

    @classmethod
    def _create_instance(cls):
        food_metadata, ingredient_metadata, all_metadata = load_food_metadata()
        current_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(current_dir, "food_model.pth")
        model, device = load_model(model_path, len(all_metadata))

        # Store metadata
        cls._food_metadata = food_metadata
        cls._ingredient_metadata = ingredient_metadata
        cls._device = device

        return model

    @classmethod
    def predict_food(cls, image_tensor):
        model = cls.get_instance()
        device = cls.get_device()
        image_tensor = image_tensor.to(device)

        food_metadata = cls._food_metadata

        with torch.no_grad():
            output = model(image_tensor)
            probabilities = torch.sigmoid(output).squeeze().tolist()

            food_probs = probabilities[:len(food_metadata)]
            max_prob = max(food_probs)
            max_idx = food_probs.index(max_prob)
            food_result = food_metadata[max_idx]

        return food_result, max_prob
