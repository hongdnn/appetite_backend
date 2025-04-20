import os

import torch
from torchvision import transforms
from PIL import Image
from model import FoodModel
from src.pytorch_model.food_dataset import get_metadata, FOOD_DATASET_PATH


def load_model(model_path, num_classes):
    model = FoodModel(num_classes)  # Ensure this matches your model definition
    model.load_state_dict(torch.load(model_path, map_location=torch.device('mps')))
    model.eval()
    return model


def preprocess_image(image_path):
    transform = transforms.Compose([
        transforms.Resize((224, 224)),  # Adjust based on model input size
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    image = Image.open(image_path).convert('RGB')
    return transform(image).unsqueeze(0)  # Add batch dimension


def predict(model, image_tensor, food_metadata, ingredient_metadata):
    with torch.no_grad():
        output = model(image_tensor)
        print("Raw output logits:", output.squeeze().tolist())
        probabilities = torch.sigmoid(output).squeeze().tolist()
        print("Probabilities:", probabilities)

        # Find the index of the highest probability for food
        max_food_idx = probabilities[:len(food_metadata)].index(max(probabilities[:len(food_metadata)]))
        food_result = food_metadata[max_food_idx]

        # Convert to binary array
        binary_result = (torch.sigmoid(output) > 0.5).int().squeeze().tolist()

        # Extract actual ingredient labels
        ingredient_results = [ingredient_metadata[i] for i, val in enumerate(binary_result[len(food_metadata):]) if val == 1]

    return binary_result, food_result, ingredient_results

def load_food_metadata():
    food = get_metadata("classes.txt")
    ingredients = get_metadata("ingredients.txt")
    total_metadata = food + ingredients
    return food, ingredients, total_metadata

if __name__ == "__main__":
    test_image = preprocess_image(os.path.join(FOOD_DATASET_PATH, "test/pho.jpg"))
    food_data, ingredient_data, all_metadata = load_food_metadata()

    current_dir = os.path.dirname(os.path.abspath(__file__))
    food_model_path = os.path.join(current_dir, "food_model.pth")
    food_model = load_model(food_model_path, len(all_metadata))

    binary_output, food_output, ingredient_output = predict(food_model, test_image, food_data, ingredient_data)
    print("Binary Output:", binary_output)
    print("Predicted Food:", food_output)
    print("Predicted Ingredients:", ingredient_output)
